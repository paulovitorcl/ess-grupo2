"""Prática 2 — Autorização de transação no Módulo de Pagamentos.

Implementa RS01 conforme DA02: o criador não aprova a própria ordem, valores
acima da alçada exigem nova validação MFA e a ordem só é enviada ao banco se
o conteúdo for idêntico à versão aprovada (selo HMAC-SHA256 com chave do
cofre de segredos, DA03). Referências: OWASP Transaction Authorization Cheat
Sheet, CWE-862, ASVS 4.0 V2.8, V4.1 e V11.1.

Exemplo ilustrativo em memória: os dicionários substituem o banco de dados.
"""

import hashlib
import hmac
import json
import uuid
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from autorizacao import AcessoNegado

# Campos cujo conteúdo é selado na aprovação e conferido antes do envio.
CAMPOS_PROTEGIDOS = ("tenant_id", "valor", "moeda", "beneficiario_documento", "beneficiario_conta", "obrigacao")
CAMPOS_EDITAVEIS = {"valor", "moeda", "beneficiario_documento", "beneficiario_conta", "obrigacao"}


class PagamentoRecusado(Exception):
    def __init__(self, motivo, status_http=403):
        super().__init__(motivo)
        self.status_http = status_http


@dataclass
class OrdemPagamento:
    id: str
    tenant_id: str
    criador_id: str
    valor: Decimal
    moeda: str
    beneficiario_documento: str
    beneficiario_conta: str
    obrigacao: str
    versao: int = 1
    estado: str = "PENDENTE"  # PENDENTE -> APROVADA -> EXECUTADA


@dataclass(frozen=True)
class Aprovacao:
    ordem_id: str
    versao: int
    aprovador_id: str
    selo: str
    reautenticado: bool


def _valor_valido(valor):
    try:
        decimal = Decimal(str(valor))
    except InvalidOperation:
        raise PagamentoRecusado("Valor inválido", 422)
    if not decimal.is_finite() or decimal <= 0:
        raise PagamentoRecusado("Valor inválido", 422)
    return decimal.quantize(Decimal("0.01"))


def payload_bancario(ordem):
    """Representação canônica enviada ao banco e usada no cálculo do selo."""
    dados = {campo: str(getattr(ordem, campo)) for campo in CAMPOS_PROTEGIDOS}
    dados.update(ordem_id=ordem.id, versao=ordem.versao)
    return dados


class ServicoPagamentos:
    def __init__(self, autorizacao, verificador_mfa, gateway_banco, auditoria, chave_integridade, alcada):
        self.authz = autorizacao
        self.mfa = verificador_mfa
        self.banco = gateway_banco
        self.auditoria = auditoria
        self._chave = chave_integridade  # obtida do Cofre de Segredos, nunca do banco operacional
        self.alcada = alcada
        self._ordens = {}
        self._aprovacoes = {}  # armazenadas separadamente das ordens

    def _selo(self, ordem):
        canonico = json.dumps(payload_bancario(ordem), sort_keys=True, separators=(",", ":"))
        return hmac.new(self._chave, canonico.encode(), hashlib.sha256).hexdigest()

    def _registrar(self, sessao, operacao, ordem_id, resultado):
        self.auditoria.registrar(sessao.usuario_id, sessao.tenant_id, operacao, ordem_id, resultado)

    def _recusar(self, sessao, operacao, ordem_id, motivo, status_http=403):
        self._registrar(sessao, operacao, ordem_id, "recusado")
        raise PagamentoRecusado(motivo, status_http)

    def _ordem_do_tenant(self, sessao, operacao, ordem_id):
        self.authz.autorizar(sessao, operacao, ordem_id)
        ordem = self._ordens.get(ordem_id)
        if ordem is None or ordem.tenant_id != sessao.tenant_id:
            self.authz.negar(sessao, operacao, ordem_id)
        return ordem

    def criar(self, sessao, valor, moeda, beneficiario_documento, beneficiario_conta, obrigacao):
        self.authz.autorizar(sessao, "criar_pagamento")
        ordem = OrdemPagamento(
            id=str(uuid.uuid4()),
            tenant_id=sessao.tenant_id,     # vem da sessão, não da requisição
            criador_id=sessao.usuario_id,   # idem: o cliente não informa quem criou
            valor=_valor_valido(valor),
            moeda=moeda,
            beneficiario_documento=beneficiario_documento,
            beneficiario_conta=beneficiario_conta,
            obrigacao=obrigacao,
        )
        self._ordens[ordem.id] = ordem
        self._registrar(sessao, "criar_pagamento", ordem.id, "permitido")
        return ordem

    def alterar(self, sessao, ordem_id, **campos):
        ordem = self._ordem_do_tenant(sessao, "criar_pagamento", ordem_id)
        if ordem.estado == "EXECUTADA" or not set(campos) <= CAMPOS_EDITAVEIS:
            self._recusar(sessao, "alterar_pagamento", ordem_id, "Alteração não permitida", 409)
        if "valor" in campos:
            campos["valor"] = _valor_valido(campos["valor"])
        for campo, valor in campos.items():
            setattr(ordem, campo, valor)
        # Qualquer mudança gera nova versão e invalida a aprovação anterior.
        ordem.versao += 1
        ordem.estado = "PENDENTE"
        self._aprovacoes.pop(ordem.id, None)
        self._registrar(sessao, "alterar_pagamento", ordem_id, "permitido")

    def aprovar(self, sessao, ordem_id, codigo_mfa=None):
        ordem = self._ordem_do_tenant(sessao, "aprovar_pagamento", ordem_id)
        if ordem.estado != "PENDENTE":
            self._recusar(sessao, "aprovar_pagamento", ordem_id, "Ordem não está pendente", 409)
        if sessao.usuario_id == ordem.criador_id:
            self._recusar(sessao, "aprovar_pagamento", ordem_id, "Segregação de funções: criador não pode aprovar")

        reautenticado = False
        if ordem.valor > self.alcada:
            # O login anterior não basta: exige um novo código TOTP do próprio aprovador.
            if not codigo_mfa or not self.mfa.verificar(sessao.usuario_id, codigo_mfa):
                self._recusar(sessao, "aprovar_pagamento", ordem_id, "Reautenticação MFA obrigatória", 401)
            reautenticado = True

        aprovacao = Aprovacao(ordem.id, ordem.versao, sessao.usuario_id, self._selo(ordem), reautenticado)
        self._aprovacoes[ordem.id] = aprovacao
        ordem.estado = "APROVADA"
        self._registrar(sessao, "aprovar_pagamento", ordem_id, "permitido")
        return aprovacao

    def executar(self, sessao, ordem_id):
        ordem = self._ordem_do_tenant(sessao, "executar_pagamento", ordem_id)
        aprovacao = self._aprovacoes.get(ordem.id)
        if ordem.estado != "APROVADA" or aprovacao is None or aprovacao.versao != ordem.versao:
            self._recusar(sessao, "executar_pagamento", ordem_id, "Ordem sem aprovação válida", 409)

        payload = payload_bancario(ordem)
        if not hmac.compare_digest(self._selo(ordem), aprovacao.selo):
            # Conteúdo diverge do aprovado: não envia e gera alerta para o monitoramento (Etapa 6).
            self._registrar(sessao, "executar_pagamento", ordem_id, "alerta_integridade")
            raise PagamentoRecusado("Dados divergentes da versão aprovada", 409)

        self.banco.enviar(payload)
        ordem.estado = "EXECUTADA"
        self._registrar(sessao, "executar_pagamento", ordem_id, "permitido")
