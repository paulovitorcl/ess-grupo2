"""Prática 1 — Autorização por empresa (tenant) e recurso no servidor.

Implementa RS02 conforme DA01: toda operação sobre um recurso valida, no
backend, o vínculo ativo do usuário com a empresa e a permissão do perfil.
O tenant fica na sessão do servidor; nenhum identificador enviado pelo cliente
concede autoridade. Referências: OWASP Authorization Cheat Sheet, OWASP API1:2023
(BOLA), CWE-639, ASVS 4.0 V4 (Access Control).

Exemplo ilustrativo em memória: o repositório substitui o banco de dados.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone

# Permissões por perfil (RBAC). O perfil só vale dentro da empresa do vínculo.
PERMISSOES = {
    "administrador": {"ler", "alterar", "excluir", "criar_pagamento", "aprovar_pagamento", "executar_pagamento"},
    "contador": {"ler", "alterar", "criar_pagamento"},
    "aprovador_financeiro": {"ler", "aprovar_pagamento", "executar_pagamento"},
    "cliente": {"ler"},
}


class AcessoNegado(Exception):
    """Negação de acesso. A mensagem é genérica para não revelar se o recurso existe."""

    status_http = 403

    def __init__(self):
        super().__init__("Acesso negado")


@dataclass
class Sessao:
    usuario_id: str
    tenant_id: str | None = None  # definido apenas pelo servidor, em selecionar_empresa()


@dataclass
class Recurso:
    id: str
    tenant_id: str
    dados: dict = field(default_factory=dict)


class RegistroAuditoria:
    """Trilha de eventos (C5). Registra quem, onde, o quê e o resultado — nunca o conteúdo do recurso."""

    def __init__(self):
        self.eventos = []

    def registrar(self, usuario, tenant, operacao, recurso, resultado):
        self.eventos.append({
            "momento": datetime.now(timezone.utc).isoformat(),
            "usuario": usuario,
            "tenant": tenant,
            "operacao": operacao,
            "recurso": recurso,
            "resultado": resultado,
        })


class Repositorio:
    def __init__(self):
        self._vinculos = {}  # (usuario_id, tenant_id) -> perfil
        self._recursos = {}

    def vincular(self, usuario_id, tenant_id, perfil):
        self._vinculos[(usuario_id, tenant_id)] = perfil

    def revogar(self, usuario_id, tenant_id):
        self._vinculos.pop((usuario_id, tenant_id), None)

    def perfil_ativo(self, usuario_id, tenant_id):
        return self._vinculos.get((usuario_id, tenant_id))

    def adicionar(self, recurso):
        self._recursos[recurso.id] = recurso

    def buscar_no_tenant(self, recurso_id, tenant_id):
        # Equivale a "SELECT ... WHERE id = ? AND tenant_id = ?": o filtro de tenant
        # faz parte da consulta, e não de uma verificação posterior ao carregamento.
        recurso = self._recursos.get(recurso_id)
        if recurso is None or recurso.tenant_id != tenant_id:
            return None
        return recurso

    def remover(self, recurso_id):
        self._recursos.pop(recurso_id, None)


class ServicoAutorizacao:
    """Política única de autorização (C3), usada por todos os módulos de negócio."""

    def __init__(self, repositorio, auditoria):
        self.repo = repositorio
        self.auditoria = auditoria

    def selecionar_empresa(self, sessao, tenant_id):
        if self.repo.perfil_ativo(sessao.usuario_id, tenant_id) is None:
            self.negar(sessao, "selecionar_empresa", tenant_id, tenant=tenant_id)
        sessao.tenant_id = tenant_id

    def autorizar(self, sessao, operacao, recurso_id=None):
        # O vínculo é consultado a cada requisição: a revogação vale mesmo para sessões abertas.
        perfil = self.repo.perfil_ativo(sessao.usuario_id, sessao.tenant_id) if sessao.tenant_id else None
        if perfil is None or operacao not in PERMISSOES.get(perfil, set()):
            self.negar(sessao, operacao, recurso_id)
        return perfil

    def negar(self, sessao, operacao, recurso_id, tenant=None):
        self.auditoria.registrar(sessao.usuario_id, tenant or sessao.tenant_id, operacao, recurso_id, "negado")
        raise AcessoNegado()


class ServicoLancamentos:
    """Exemplo de módulo do Núcleo de Negócio protegido pela política comum."""

    def __init__(self, repositorio, autorizacao, auditoria):
        self.repo = repositorio
        self.authz = autorizacao
        self.auditoria = auditoria

    def _carregar(self, sessao, operacao, recurso_id):
        self.authz.autorizar(sessao, operacao, recurso_id)
        recurso = self.repo.buscar_no_tenant(recurso_id, sessao.tenant_id)
        if recurso is None:
            # Inexistente ou de outra empresa: mesma resposta 403 (evita enumeração).
            self.authz.negar(sessao, operacao, recurso_id)
        return recurso

    def _permitido(self, sessao, operacao, recurso_id):
        self.auditoria.registrar(sessao.usuario_id, sessao.tenant_id, operacao, recurso_id, "permitido")

    def ler(self, sessao, recurso_id):
        recurso = self._carregar(sessao, "ler", recurso_id)
        self._permitido(sessao, "ler", recurso_id)
        return dict(recurso.dados)

    def alterar(self, sessao, recurso_id, alteracoes):
        recurso = self._carregar(sessao, "alterar", recurso_id)
        recurso.dados.update(alteracoes)
        self._permitido(sessao, "alterar", recurso_id)

    def excluir(self, sessao, recurso_id):
        self._carregar(sessao, "excluir", recurso_id)
        self.repo.remover(recurso_id)
        self._permitido(sessao, "excluir", recurso_id)
