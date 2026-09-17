# 3. Usuários Ativos e Pontos de Interação

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
