"""Testes da Prática 1 — Autorização por empresa (tenant) e recurso.

Escritos ANTES da implementação (autorizacao.py), a partir de RS02 e do
critério de verificação de DA01. Rastreabilidade: R18 / VULN-02 / RS02 / DA01.

Executar a partir de codigo/etapa-4/:  python3 -m unittest -v
"""

import unittest

from autorizacao import (
    AcessoNegado,
    RegistroAuditoria,
    Recurso,
    Repositorio,
    ServicoAutorizacao,
    ServicoLancamentos,
    Sessao,
)


class TestAutorizacaoPorTenant(unittest.TestCase):
    def setUp(self):
        self.repo = Repositorio()
        self.auditoria = RegistroAuditoria()
        self.authz = ServicoAutorizacao(self.repo, self.auditoria)
        self.lancamentos = ServicoLancamentos(self.repo, self.authz, self.auditoria)

        self.repo.vincular("ana", "empresa-a", "administrador")
        self.repo.vincular("carla", "empresa-a", "cliente")
        self.repo.vincular("bruno", "empresa-b", "contador")

        self.repo.adicionar(Recurso("lanc-a1", "empresa-a", {"historico": "Folha 10/2026", "valor": "15000.00"}))
        self.repo.adicionar(Recurso("lanc-b1", "empresa-b", {"historico": "DARF IRPJ", "valor": "8200.00"}))

    def _sessao(self, usuario, empresa):
        sessao = Sessao(usuario)
        self.authz.selecionar_empresa(sessao, empresa)
        return sessao

    # TS01 — caso válido
    def test_ts01_usuario_vinculado_le_recurso_da_propria_empresa(self):
        sessao = self._sessao("ana", "empresa-a")

        dados = self.lancamentos.ler(sessao, "lanc-a1")

        self.assertEqual(dados["historico"], "Folha 10/2026")
        self.assertEqual(self.auditoria.eventos[-1]["resultado"], "permitido")

    # TS02 — caso malicioso: IDOR trocando o identificador do recurso
    def test_ts02_administrador_de_outra_empresa_nao_le_recurso_alheio(self):
        sessao = self._sessao("ana", "empresa-a")

        with self.assertRaises(AcessoNegado) as ctx:
            self.lancamentos.ler(sessao, "lanc-b1")

        self.assertEqual(ctx.exception.status_http, 403)
        self.assertNotIn("DARF", str(ctx.exception))
        evento = self.auditoria.eventos[-1]
        self.assertEqual(evento["resultado"], "negado")
        self.assertEqual(evento["recurso"], "lanc-b1")
        self.assertNotIn("dados", evento)

        # Recurso inexistente recebe a mesma resposta: não revela o que existe em outra empresa.
        with self.assertRaises(AcessoNegado) as ctx_inexistente:
            self.lancamentos.ler(sessao, "lanc-zz")
        self.assertEqual(str(ctx_inexistente.exception), str(ctx.exception))

    # TS03 — caso malicioso: manipular o contexto de empresa da sessão
    def test_ts03_selecionar_empresa_sem_vinculo_e_negado(self):
        sessao = self._sessao("ana", "empresa-a")

        with self.assertRaises(AcessoNegado):
            self.authz.selecionar_empresa(sessao, "empresa-b")

        self.assertEqual(sessao.tenant_id, "empresa-a")

    # TS04 — caso malicioso: alteração e exclusão cruzadas não persistem
    def test_ts04_alteracao_e_exclusao_em_outra_empresa_nao_persistem(self):
        sessao = self._sessao("ana", "empresa-a")

        with self.assertRaises(AcessoNegado):
            self.lancamentos.alterar(sessao, "lanc-b1", {"valor": "1.00"})
        with self.assertRaises(AcessoNegado):
            self.lancamentos.excluir(sessao, "lanc-b1")

        recurso = self.repo.buscar_no_tenant("lanc-b1", "empresa-b")
        self.assertIsNotNone(recurso)
        self.assertEqual(recurso.dados["valor"], "8200.00")

    # TS05 — caso não autorizado: vínculo revogado durante a sessão
    def test_ts05_vinculo_revogado_bloqueia_sessao_ja_iniciada(self):
        sessao = self._sessao("ana", "empresa-a")
        self.lancamentos.ler(sessao, "lanc-a1")

        self.repo.revogar("ana", "empresa-a")

        with self.assertRaises(AcessoNegado):
            self.lancamentos.ler(sessao, "lanc-a1")

    # TS06 — caso não autorizado: perfil sem permissão para a operação
    def test_ts06_perfil_cliente_nao_exclui_lancamento(self):
        sessao = self._sessao("carla", "empresa-a")

        self.assertEqual(self.lancamentos.ler(sessao, "lanc-a1")["historico"], "Folha 10/2026")
        with self.assertRaises(AcessoNegado):
            self.lancamentos.excluir(sessao, "lanc-a1")

        self.assertIsNotNone(self.repo.buscar_no_tenant("lanc-a1", "empresa-a"))


if __name__ == "__main__":
    unittest.main()
