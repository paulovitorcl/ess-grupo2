"""Testes da Prática 2 — Autorização de transação (pagamentos).

Escritos ANTES da implementação (pagamentos.py), a partir de RS01 e do
critério de verificação de DA02. Rastreabilidade: R13 / VULN-01 / RS01 / DA02.

Executar a partir de codigo/etapa-4/:  python3 -m unittest -v
"""

import unittest
from decimal import Decimal

from autorizacao import AcessoNegado, RegistroAuditoria, Repositorio, ServicoAutorizacao, Sessao
from pagamentos import PagamentoRecusado, ServicoPagamentos


class MFAFalso:
    """Simula o Serviço de Autenticação: cada código vale uma única vez."""

    def __init__(self, codigos):
        self._codigos = {(u, c) for u, c in codigos}

    def verificar(self, usuario_id, codigo):
        chave = (usuario_id, codigo)
        if chave in self._codigos:
            self._codigos.remove(chave)
            return True
        return False


class BancoFalso:
    """Simula a Camada de Integração com o banco e registra o que foi enviado."""

    def __init__(self):
        self.enviados = []

    def enviar(self, payload):
        self.enviados.append(payload)


DADOS_ORDEM = {
    "valor": "2500.00",
    "moeda": "BRL",
    "beneficiario_documento": "12.345.678/0001-90",
    "beneficiario_conta": "001-1234-56789-0",
    "obrigacao": "NF 4521 — Fornecedor X",
}


class TestAutorizacaoDePagamentos(unittest.TestCase):
    def setUp(self):
        self.repo = Repositorio()
        self.auditoria = RegistroAuditoria()
        self.authz = ServicoAutorizacao(self.repo, self.auditoria)
        self.mfa = MFAFalso([("fernanda", "482913")])
        self.banco = BancoFalso()
        self.pagamentos = ServicoPagamentos(
            self.authz,
            self.mfa,
            self.banco,
            self.auditoria,
            chave_integridade=b"chave-de-teste-vinda-do-cofre",
            alcada=Decimal("10000.00"),
        )

        self.repo.vincular("carlos", "empresa-a", "contador")
        self.repo.vincular("fernanda", "empresa-a", "aprovador_financeiro")
        self.repo.vincular("ana", "empresa-a", "administrador")
        self.repo.vincular("bruno", "empresa-b", "aprovador_financeiro")

    def _sessao(self, usuario, empresa="empresa-a"):
        sessao = Sessao(usuario)
        self.authz.selecionar_empresa(sessao, empresa)
        return sessao

    # TS07 — caso válido: criador e aprovador distintos, abaixo da alçada
    def test_ts07_fluxo_legitimo_envia_exatamente_a_versao_aprovada(self):
        ordem = self.pagamentos.criar(self._sessao("carlos"), **DADOS_ORDEM)
        aprovadora = self._sessao("fernanda")

        self.pagamentos.aprovar(aprovadora, ordem.id)
        self.pagamentos.executar(aprovadora, ordem.id)

        self.assertEqual(len(self.banco.enviados), 1)
        enviado = self.banco.enviados[0]
        self.assertEqual(enviado["valor"], "2500.00")
        self.assertEqual(enviado["beneficiario_conta"], DADOS_ORDEM["beneficiario_conta"])
        self.assertEqual(ordem.estado, "EXECUTADA")

    # TS08 — caso malicioso: o mesmo usuário cria e aprova (mesmo sendo administrador)
    def test_ts08_autoaprovacao_e_recusada(self):
        sessao = self._sessao("ana")
        ordem = self.pagamentos.criar(sessao, **DADOS_ORDEM)

        with self.assertRaises(PagamentoRecusado) as ctx:
            self.pagamentos.aprovar(sessao, ordem.id)
        self.assertEqual(ctx.exception.status_http, 403)

        with self.assertRaises(PagamentoRecusado):
            self.pagamentos.executar(sessao, ordem.id)

        self.assertEqual(ordem.estado, "PENDENTE")
        self.assertEqual(self.banco.enviados, [])

    # TS09 — caso não autorizado: valor acima da alçada exige nova validação MFA
    def test_ts09_acima_da_alcada_exige_reautenticacao_mfa(self):
        ordem = self.pagamentos.criar(self._sessao("carlos"), **{**DADOS_ORDEM, "valor": "48000.00"})
        aprovadora = self._sessao("fernanda")

        with self.assertRaises(PagamentoRecusado) as sem_codigo:
            self.pagamentos.aprovar(aprovadora, ordem.id)
        self.assertEqual(sem_codigo.exception.status_http, 401)
        with self.assertRaises(PagamentoRecusado):
            self.pagamentos.aprovar(aprovadora, ordem.id, codigo_mfa="000000")
        self.assertEqual(ordem.estado, "PENDENTE")

        aprovacao = self.pagamentos.aprovar(aprovadora, ordem.id, codigo_mfa="482913")

        self.assertTrue(aprovacao.reautenticado)
        self.assertEqual(ordem.estado, "APROVADA")

    # TS10 — caso malicioso: beneficiário adulterado diretamente no banco após a aprovação
    def test_ts10_adulteracao_apos_aprovacao_bloqueia_envio(self):
        ordem = self.pagamentos.criar(self._sessao("carlos"), **DADOS_ORDEM)
        aprovadora = self._sessao("fernanda")
        self.pagamentos.aprovar(aprovadora, ordem.id)

        ordem.beneficiario_conta = "999-0000-00000-1"  # escrita fora do fluxo da aplicação

        with self.assertRaises(PagamentoRecusado) as ctx:
            self.pagamentos.executar(aprovadora, ordem.id)

        self.assertEqual(ctx.exception.status_http, 409)
        self.assertEqual(self.banco.enviados, [])
        self.assertEqual(self.auditoria.eventos[-1]["resultado"], "alerta_integridade")

    # TS11 — caso inválido: alteração legítima após aprovação exige nova aprovação
    def test_ts11_alteracao_apos_aprovacao_volta_para_pendente(self):
        criador = self._sessao("carlos")
        aprovadora = self._sessao("fernanda")
        ordem = self.pagamentos.criar(criador, **DADOS_ORDEM)
        self.pagamentos.aprovar(aprovadora, ordem.id)

        self.pagamentos.alterar(criador, ordem.id, valor="2600.00")

        self.assertEqual(ordem.estado, "PENDENTE")
        self.assertEqual(ordem.versao, 2)
        with self.assertRaises(PagamentoRecusado):
            self.pagamentos.executar(aprovadora, ordem.id)
        self.assertEqual(self.banco.enviados, [])

    # TS12 — caso não autorizado: aprovador de outra empresa (reaproveita a Prática 1)
    def test_ts12_aprovador_de_outra_empresa_nao_aprova(self):
        ordem = self.pagamentos.criar(self._sessao("carlos"), **DADOS_ORDEM)

        with self.assertRaises(AcessoNegado):
            self.pagamentos.aprovar(self._sessao("bruno", "empresa-b"), ordem.id)

        self.assertEqual(ordem.estado, "PENDENTE")

    # Validação de entrada da ordem
    def test_valor_invalido_e_recusado_na_criacao(self):
        criador = self._sessao("carlos")
        for valor in ("0", "-10.00", "abc"):
            with self.subTest(valor=valor), self.assertRaises(PagamentoRecusado):
                self.pagamentos.criar(criador, **{**DADOS_ORDEM, "valor": valor})


if __name__ == "__main__":
    unittest.main()
