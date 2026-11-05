# 3. Usuários, Ativos e Pontos de Interação

Sistema de contabilidade que presta serviços contábeis, fiscais, de folha de
pagamento e pagamentos, com integrações externas (bancos, Receita Federal,
prefeituras, ERP dos clientes).

## 3.1 Usuários (atores) do sistema

| Ator | Papel | Principais ações |
|------|-------|------------------|
| **Contador** | Usuário operacional interno | Cadastra empresas, faz lançamentos, apura impostos, processa folha, emite guias/notas, gera relatórios |
| **Cliente** | Empresa/pessoa atendida | Consulta documentos, cadastra dados bancários, emite NF-e/NFS-e, autoriza pagamentos |
| **Administrador** | Gestão de acesso e configuração | Cria/desativa contas, define perfis (RBAC), configura e renova credenciais de API |
| **Auditor** | Compliance / controle | Consulta trilha de auditoria, exporta logs |
| **Funcionário (do cliente)** | Destinatário de dados trabalhistas | Acessa o próprio holerite |

## 3.2 Atores externos (sistemas integrados)

| Ator externo | Interação |
|--------------|-----------|
| **Bancos (Open Finance)** | Importação de extratos, conciliação, pagamento de guias/boletos |
| **Receita Federal** | Validação de CNPJ, transmissão de SPED |
| **Prefeituras** | Transmissão de NFS-e |
| **eSocial** | Transmissão de eventos de folha |
| **ERP do cliente** | Sincronização de dados contábeis/fiscais |

## 3.3 Pontos de interação (entry points)

Locais onde dados entram ou saem do sistema — superfície de ataque relevante
para a análise STRIDE.

| # | Ponto de interação | Atores | Direção |
|---|--------------------|--------|---------|
| P1 | Tela/API de **login e MFA** | Contador, Cliente, Admin, Auditor | Entrada |
| P2 | **Recuperação de senha** | Cliente, Contador | Entrada |
| P3 | **Gestão de contas e perfis (RBAC)** | Administrador | Entrada |
| P4 | **Cadastros** (empresa, sócios, plano de contas, dados bancários) | Contador, Cliente | Entrada |
| P5 | **Escrituração** (lançamentos manuais e importação em lote OFX/planilha) | Contador | Entrada |
| P6 | **Apuração fiscal e geração de SPED/guias** | Contador | Entrada/Saída |
| P7 | **Folha de pagamento e holerites** | Contador, Funcionário | Entrada/Saída |
| P8 | **Emissão/exportação de documentos** (NF-e, relatórios, PDF/XML) | Cliente, Contador | Saída |
| P9 | **APIs de integração externa** (bancos, Receita, prefeitura, eSocial, ERP) | Sistemas externos | Entrada/Saída |
| P10 | **Pagamentos** (boletos, autorização de pagamento) | Contador, Cliente | Entrada/Saída |
| P11 | **Auditoria/Logs** (consulta e exportação) | Auditor, Administrador | Saída |

## 3.4 Ativos e informações protegidas

Ativos são os recursos cujo acesso, alteração, destruição ou indisponibilidade
indevidos causariam prejuízo aos clientes, aos funcionários ou ao escritório
contábil. A coluna **Propriedade crítica** indica o que mais importa proteger:
**C** = confidencialidade, **I** = integridade, **D** = disponibilidade.

### Dados e informações

| ID | Ativo | Exemplos | Propriedade crítica | Criticidade | Prejuízo se comprometido |
|----|-------|----------|---------------------|-------------|--------------------------|
| A01 | **Credenciais e sessões** | Senhas (hash), segredos MFA, tokens de sessão e de recuperação de senha | C, I | **Muito alta** | Invasão de contas e operações fraudulentas em nome de terceiros |
| A02 | **Certificado digital (e-CNPJ A1)** | Chave privada usada para assinar SPED, NF-e e eventos do eSocial | C, I | **Muito alta** | Assinatura de documentos fiscais falsos com validade jurídica em nome do cliente |
| A03 | **Dados bancários e de pagamento** | Conta/PIX de beneficiários, guias, boletos, autorizações de pagamento | I, C | **Muito alta** | Desvio de valores por troca de beneficiário ou alteração de guia |
| A04 | **Escrituração contábil** | Lançamentos D/C, saldos, conciliações, períodos encerrados | I | **Alta** | Balanços e apurações incorretos, ocultação de fraude |
| A05 | **Dados fiscais e obrigações** | Bases de cálculo, SPED, DARF/DAS, NF-e/NFS-e | I, D | **Alta** | Multas, autuações, perda de prazos legais |
| A06 | **Folha de pagamento e holerites** | Salários, CPF, rubricas, dados de dependentes, eventos eSocial | C, I | **Alta** | Exposição de dados pessoais (LGPD) e pagamentos incorretos |
| A07 | **Dados cadastrais e pessoais** | CNPJ/CPF, quadro societário, endereços, contatos | C | **Alta** | Violação de privacidade (LGPD), fraude de identidade |
| A08 | **Matriz de permissões (RBAC)** | Perfis, papéis e vínculos usuário↔empresa | I | **Muito alta** | Elevação de privilégio e acesso a dados de outros clientes |
| A09 | **Trilha de auditoria e logs** | Quem/quando/o quê de cada lançamento, alteração e acesso | I, D | **Alta** | Perda de não-repúdio e de evidências de fraude |
| A10 | **Credenciais de integração** | Chaves de API, tokens OAuth do Open Finance, segredos de webhooks | C | **Muito alta** | Acesso a extratos, falsificação de mensagens de integração |
| A11 | **Documentos exportados** | Relatórios, PDF/XML de notas e demonstrativos | C | **Média** | Vazamento de informações financeiras dos clientes |

### Componentes e infraestrutura

| ID | Ativo | Função | Propriedade crítica | Criticidade |
|----|-------|--------|---------------------|-------------|
| A12 | **Aplicação Web / API** | Ponto único de acesso de todos os perfis (P1–P11) | D, I | **Muito alta** |
| A13 | **Serviço de autenticação e autorização** | Login, MFA, sessões e verificação RBAC | I, D | **Muito alta** |
| A14 | **Banco de dados** | Armazena A03–A08 de todos os clientes | C, I, D | **Muito alta** |
| A15 | **Camada de integração** | Comunicação com bancos, Receita, prefeituras, eSocial e ERP | I, D | **Alta** |
| A16 | **Backups** | Cópias do banco e dos documentos | C, D | **Alta** |
| A17 | **Serviços externos** (bancos, Receita Federal, prefeituras, eSocial, ERP) | Dependências fora do controle do sistema | D | **Alta** |

### Ativos mais importantes

Os ativos de criticidade **muito alta** concentram o maior potencial de dano e
orientam a análise STRIDE e a priorização de riscos da Etapa 2:

1. **Credenciais, sessões e RBAC (A01, A08, A13)** — controlam quem pode fazer
   o quê; se comprometidos, todos os demais ativos ficam expostos.
2. **Certificado digital (A02)** — permite agir legalmente em nome do cliente
   perante Receita, prefeituras e eSocial.
3. **Dados bancários e de pagamento (A03)** — alvo direto de fraude financeira.
4. **Banco de dados (A14)** — concentra dados contábeis, fiscais e pessoais de
   todos os clientes; um único vazamento afeta muitas empresas.
5. **Credenciais de integração (A10)** — dão acesso a sistemas de terceiros
   (bancos, governo) com a identidade do escritório.
