# Etapa 4 — Código Seguro e Testes de Segurança

Esta etapa transforma duas decisões da [arquitetura segura](../etapa3/3.4-decisoes-de-arquitetura.md)
em práticas de implementação. Foram escolhidos os dois riscos **críticos** que
envolvem diretamente regras do backend: o acesso entre empresas (R18) e a
fraude de pagamento (R13).

**Forma de realização:** prática. O código e os testes executáveis estão em
[`codigo/etapa-4/`](../../codigo/etapa-4/), escritos em Python usando apenas a
biblioteca padrão. São exemplos ilustrativos, com armazenamento em memória no
lugar do banco de dados, não o sistema completo.

**Testes antes da implementação:** para cada prática, os testes foram derivados
dos critérios de verificação de RS01, RS02, DA01 e DA02 e escritos antes do
código (`test_*.py` antes de `autorizacao.py` e `pagamentos.py`). A ordem pode
ser conferida no histórico de commits do repositório.

## Visão geral

| Prática | Risco | Vulnerabilidade | Requisito | Decisão | Controle no diagrama | Referência OWASP |
| --- | --- | --- | --- | --- | --- | --- |
| P1 — Autorização por empresa e recurso no servidor | R18 | VULN-02 (CWE-639) | RS02 | DA01 | C3 | Authorization Cheat Sheet; API1:2023 BOLA; ASVS 4.0 V4 |
| P2 — Autorização de transação de pagamentos | R13 | VULN-01 (CWE-862) | RS01 | DA02 | C4 (com C2 e C5) | Transaction Authorization Cheat Sheet; ASVS 4.0 V2/V4/V11 |

---

## P1 — Autorização por empresa (tenant) e recurso no servidor

### 1. Risco e requisito relacionados

- **Risco R18 (Crítico):** um usuário de uma empresa consulta ou altera dados
  cadastrais, bancários e contábeis de outra empresa cliente, porque a
  autorização confere apenas o login e não o vínculo com o tenant (IDOR).
- **Requisito RS02:** o backend deve validar, em todas as requisições a
  recursos vinculados a empresas, o vínculo ativo do usuário com o tenant
  proprietário, independentemente do perfil RBAC, respondendo `HTTP 403`
  quando o vínculo não existir.

### 2. Testes de segurança (definidos antes da implementação)

| Teste | Tipo | Entrada ou ação | Resultado seguro esperado |
| --- | --- | --- | --- |
| TS01 | Válido | Administradora da empresa A lê um lançamento da empresa A | Dados retornados; evento `permitido` na auditoria |
| TS02 | Malicioso | A mesma administradora troca o identificador e pede um lançamento da empresa B | `HTTP 403` com mensagem genérica, sem conteúdo do recurso; evento `negado` sem os dados. Um identificador inexistente recebe a mesma resposta |
| TS03 | Malicioso | Usuária da empresa A tenta trocar o contexto da sessão para a empresa B | Negado; a sessão continua presa à empresa A |
| TS04 | Malicioso | Usuária da empresa A tenta alterar e excluir um lançamento de B | Ambas negadas; o lançamento de B continua igual |
| TS05 | Não autorizado | O vínculo da usuária com A é revogado durante uma sessão já aberta | A próxima requisição é negada |
| TS06 | Não autorizado | Usuário com perfil `cliente` tenta excluir um lançamento da própria empresa | Leitura permitida, exclusão negada |

Os testes TS01 e TS02 são o par mínimo pedido no enunciado. TS03 a TS06
cobrem o restante do critério de verificação de DA01.

### 3. Implementação

Arquivo: [`codigo/etapa-4/autorizacao.py`](../../codigo/etapa-4/autorizacao.py).

1. **O tenant pertence à sessão, não à requisição.** A empresa ativa só é
   definida por `selecionar_empresa()`, que exige um vínculo persistido.
   Nenhum `tenant_id` enviado pelo cliente é usado para decidir acesso.
2. **Política única.** Todos os módulos chamam `ServicoAutorizacao.autorizar()`,
   que combina o vínculo ativo (usuário, empresa) e a permissão do perfil para
   a operação. Ser administrador só tem efeito dentro da empresa do vínculo.
3. **O vínculo é consultado em toda requisição.** Por isso uma revogação vale
   imediatamente, mesmo para sessões abertas (TS05).
4. **A consulta já filtra pelo tenant.** `buscar_no_tenant()` equivale a
   `WHERE id = ? AND tenant_id = ?`. O recurso de outra empresa não chega a
   ser carregado.
5. **Recurso inexistente e recurso de outra empresa têm a mesma resposta 403**,
   o que impede descobrir identificadores válidos de outros clientes.
6. **Negar por padrão.** Sem vínculo, sem perfil ou sem permissão explícita, a
   operação é negada.
7. **A auditoria registra a decisão, não os dados.** Cada evento guarda usuário,
   empresa, operação, recurso e resultado, nunca o conteúdo do lançamento (DA03).

Trecho central:

```python
def autorizar(self, sessao, operacao, recurso_id=None):
    perfil = self.repo.perfil_ativo(sessao.usuario_id, sessao.tenant_id) if sessao.tenant_id else None
    if perfil is None or operacao not in PERMISSOES.get(perfil, set()):
        self.negar(sessao, operacao, recurso_id)
    return perfil

def _carregar(self, sessao, operacao, recurso_id):
    self.authz.autorizar(sessao, operacao, recurso_id)
    recurso = self.repo.buscar_no_tenant(recurso_id, sessao.tenant_id)
    if recurso is None:
        self.authz.negar(sessao, operacao, recurso_id)  # mesma resposta para inexistente
    return recurso
```

### 4. Resultado esperado

Um usuário acessa somente recursos das empresas com as quais tem vínculo
ativo, e apenas nas operações que o perfil permite. Trocar identificadores na
URL ou no corpo da requisição não dá acesso a outra empresa, mesmo com perfil
administrativo. Toda negativa vira um evento auditável, que alimenta a regra
de detecção de acessos negados da [Etapa 6](../../roteiros/etapa-6-deteccao-de-intrusoes.md).

### 5. Referências OWASP

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): negar por padrão, validar permissões em toda requisição e no servidor.
- [OWASP API Security Top 10 — API1:2023 Broken Object Level Authorization](https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/).
- [OWASP Insecure Direct Object Reference Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html).
- OWASP ASVS 4.0, capítulo V4 (*Access Control*), em especial 4.1.1, 4.1.3, 4.1.5 e 4.2.1.
- [CWE-639 — Authorization Bypass Through User-Controlled Key](https://cwe.mitre.org/data/definitions/639.html).

---

## P2 — Autorização de transação no Módulo de Pagamentos

### 1. Risco e requisito relacionados

- **Risco R13 (Crítico):** um pagamento não autorizado é executado ou tem o
  valor ou o beneficiário alterado depois da aprovação. Hoje o mesmo usuário
  cria e autoriza, os dados executados não são comparados com os aprovados e
  não existe reautenticação por limite de valor.
- **Requisito RS01:** o backend deve exigir que o aprovador seja diferente do
  criador, exigir reautenticação MFA acima da alçada e garantir que os dados
  transmitidos ao banco correspondam integralmente aos aprovados.

### 2. Testes de segurança (definidos antes da implementação)

| Teste | Tipo | Entrada ou ação | Resultado seguro esperado |
| --- | --- | --- | --- |
| TS07 | Válido | Contador cria uma ordem de R$ 2.500,00; outra usuária, aprovadora financeira, aprova e executa | O banco recebe exatamente uma ordem, idêntica à versão aprovada; estado `EXECUTADA` |
| TS08 | Malicioso | A administradora cria uma ordem e tenta aprová-la e executá-la sozinha | `HTTP 403` (segregação de funções); ordem continua `PENDENTE`; nada enviado ao banco |
| TS09 | Não autorizado | Ordem de R$ 48.000,00 (acima da alçada de R$ 10.000,00) aprovada sem código MFA e depois com código errado | `HTTP 401` nos dois casos; só aprova com um código TOTP válido do próprio aprovador |
| TS10 | Malicioso | Depois da aprovação, a conta do beneficiário é alterada direto no armazenamento, fora do fluxo da aplicação | Execução bloqueada com `HTTP 409`; nada enviado ao banco; evento `alerta_integridade` |
| TS11 | Inválido | O criador altera o valor de uma ordem já aprovada pelo fluxo normal | Nova versão (v2), estado volta a `PENDENTE`; a execução é recusada até uma nova aprovação |
| TS12 | Não autorizado | Aprovador da empresa B tenta aprovar uma ordem da empresa A | Negado pela política da P1 (`AcessoNegado`) |
| — | Inválido | Ordem criada com valor `0`, `-10.00` ou `abc` | Recusada na criação (`HTTP 422`) |

O par mínimo do enunciado é TS07 (válido) e TS08 (malicioso).

### 3. Implementação

Arquivo: [`codigo/etapa-4/pagamentos.py`](../../codigo/etapa-4/pagamentos.py).

1. **Identidades vêm do servidor.** Empresa e criador da ordem são tirados da
   sessão. O cliente não informa quem criou nem a qual empresa a ordem pertence.
2. **Segregação de funções.** `aprovar()` recusa quando
   `sessao.usuario_id == ordem.criador_id`, qualquer que seja o perfil.
3. **Reautenticação acima da alçada.** Para `valor > alcada`, a aprovação
   exige um novo código TOTP do aprovador, verificado pelo Serviço de
   Autenticação (C2), e o código é consumido uma única vez. O login anterior
   não conta. A aprovação registra `reautenticado=True`.
4. **Selo da versão aprovada.** Na aprovação calcula-se um
   **HMAC-SHA256** da representação canônica (JSON ordenado) dos campos
   protegidos: empresa, valor, moeda, documento e conta do beneficiário,
   obrigação, id e versão. A chave vem do Cofre de Segredos (DA03), então
   quem tem acesso só ao banco operacional não consegue recalcular o selo
   depois de adulterar a ordem.
5. **Conferência antes do envio.** `executar()` exige estado `APROVADA`,
   aprovação da mesma versão e recalcula o selo sobre o payload que será
   enviado. A comparação usa `hmac.compare_digest`, que tem tempo constante.
   Se houver divergência, nada é enviado e um alerta vai para a auditoria e o
   monitoramento.
6. **Alterar é invalidar.** Qualquer alteração gera nova versão, descarta a
   aprovação anterior e volta a ordem para `PENDENTE`. Só os campos de uma
   lista permitida podem ser alterados.
7. **Validação de entrada.** O valor é convertido para `Decimal` com duas
   casas e precisa ser finito e positivo.
8. **Reuso da P1.** Todas as operações passam por `ServicoAutorizacao` e pela
   busca restrita ao tenant, o que impede aprovar ordens de outra empresa.

Trecho central:

```python
def aprovar(self, sessao, ordem_id, codigo_mfa=None):
    ordem = self._ordem_do_tenant(sessao, "aprovar_pagamento", ordem_id)
    if sessao.usuario_id == ordem.criador_id:
        self._recusar(sessao, "aprovar_pagamento", ordem_id, "Segregação de funções: criador não pode aprovar")
    if ordem.valor > self.alcada:
        if not codigo_mfa or not self.mfa.verificar(sessao.usuario_id, codigo_mfa):
            self._recusar(sessao, "aprovar_pagamento", ordem_id, "Reautenticação MFA obrigatória", 401)
    aprovacao = Aprovacao(ordem.id, ordem.versao, sessao.usuario_id, self._selo(ordem), ...)

def executar(self, sessao, ordem_id):
    ...
    if not hmac.compare_digest(self._selo(ordem), aprovacao.selo):
        self._registrar(sessao, "executar_pagamento", ordem_id, "alerta_integridade")
        raise PagamentoRecusado("Dados divergentes da versão aprovada", 409)
    self.banco.enviar(payload)
```

### 4. Resultado esperado

Uma pessoa sozinha não consegue criar e aprovar a mesma ordem. Pagamentos
acima da alçada só são aprovados com um segundo fator recente do aprovador.
O banco só recebe uma ordem idêntica à versão aprovada, e qualquer adulteração
posterior, pela aplicação ou direto no armazenamento, impede o envio e gera
alerta. Nenhuma tentativa recusada chega à Camada de Integração.

### 5. Referências OWASP

- [OWASP Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html): "what you see is what you sign", autorização por transação, proteção contra alteração entre aprovação e execução.
- [OWASP Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html): reautenticação para operações sensíveis.
- [OWASP Business Logic Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Business_Logic_Security_Cheat_Sheet.html): segregação de funções e transições de estado válidas.
- OWASP ASVS 4.0: V4.1 (controle de acesso no servidor), V2.8 (OTP de uso único), V11.1 (lógica de negócio em ordem sequencial, sem pular etapas).
- [CWE-862 — Missing Authorization](https://cwe.mitre.org/data/definitions/862.html).

---

## Execução e evidência

```bash
cd codigo/etapa-4
python3 -m unittest -v
```

Resultado: **13 testes executados, 13 aprovados**. A saída completa está em
[`evidencias/etapa-4/saida-testes.txt`](../../evidencias/etapa-4/saida-testes.txt).

## Limitações

- Exemplos em memória: em produção, o filtro de tenant deve estar na camada
  de acesso a dados (ou em *row-level security* do banco), e aprovações e
  auditoria devem ficar em armazenamentos com permissões separadas (DA03).
- O MFA é simulado nos testes. A implementação real do TOTP e do limite de
  tentativas (RS03) pertence ao Serviço de Autenticação e não foi codificada
  nesta etapa.
- Idempotência do envio ao banco (R26) e conciliação em caso de falha após o
  envio estão previstas em DA02/DA03, mas não foram implementadas aqui.
- Os testes verificam a lógica de autorização. Eles não substituem a
  verificação dinâmica (Etapa 5) nem a revisão de código no pipeline (Etapa 7).
