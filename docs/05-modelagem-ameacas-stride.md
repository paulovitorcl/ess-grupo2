# 5. Modelagem de Ameaças com STRIDE 

Este documento detalha as categorias **RIDE** da metodologia STRIDE para o
sistema de contabilidade:

- **R — Repudiation (Repúdio):** um ator nega ter executado uma ação ou o
  sistema não consegue provar sua autoria;
- **I — Information Disclosure (Divulgação de informação):** dados são
  acessados ou enviados a quem não deveria recebê-los;
- **D — Denial of Service (Negação de serviço):** uma função ou recurso fica
  indisponível para usuários legítimos;
- **E — Elevation of Privilege (Elevação de privilégio):** um ator obtém
  permissões superiores às que lhe foram concedidas.

As ameaças foram derivadas dos atores, pontos de interação e fluxos descritos
em [3. Usuários Ativos e Pontos de Interação](./03-usuarios-e-pontos-de-interacao.md)
e [4. Visão Geral da Arquitetura e Fluxo](./04-visao-geral-arquitetura-fluxo.md).
Os identificadores `UC-01` a `UC-45` seguem a relação de casos de uso do
[README](../README.md).

## 5.1 Escopo e fronteiras de confiança

| Fronteira | Componentes e dados | Riscos RIDE prioritários |
|-----------|---------------------|--------------------------|
| Acesso externo | Web/API, login, MFA, recuperação de senha e RBAC | Repúdio de acesso, exposição por sessão, indisponibilidade por abuso e bypass de autorização |
| Núcleo e persistência | Cadastro, escrituração, fiscal, folha, pagamentos, banco de dados | Negação de alterações, vazamento entre empresas e acesso a funções administrativas |
| Auditoria | Trilha de auditoria e logs de acesso | Impossibilidade de provar ações, exposição de logs e perda da evidência |
| Integrações | Bancos, Receita Federal, prefeituras, eSocial e ERP | Vazamento em trânsito, indisponibilidade de dependências e uso de credenciais com privilégio excessivo |

## 5.2 S — Spoofing (Falsificação de identidade)

> **TODO:** preencher futuramente a modelagem de ameaças de falsificação de
> identidade, seus impactos e controles de mitigação.

## 5.3 R — Repudiation (Repúdio)

### Ameaças

| ID | Ponto/UC | Cenário de ameaça | Impacto |
|----|----------|-------------------|---------|
| R-01 | P1 / UC-01, UC-02 | Um usuário nega um login ou uma validação MFA porque o sistema registra apenas sucesso/erro, sem usuário, horário, IP, dispositivo e identificador da sessão. | Dificulta investigar invasões e responsabilizar o autor de acessos indevidos. |
| R-02 | P3 / UC-04, UC-06 | Um administrador nega ter criado uma conta, desativado um usuário ou alterado um perfil RBAC quando não existe trilha de antes/depois e aprovação da mudança. | Permissões indevidas podem permanecer sem autoria comprovável. |
| R-03 | P5, P6 / UC-13, UC-16, UC-17, UC-19, UC-22 | Um contador nega um lançamento, estorno, reabertura de período ou retificação fiscal. | Perda da capacidade de reconstruir a contabilidade e contestar uma obrigação incorreta. |
| R-04 | P7 / UC-25, UC-27, UC-28 | O responsável nega o processamento da folha, uma alteração trabalhista ou a transmissão ao eSocial. | Conflitos trabalhistas e dificuldade de comprovar o evento enviado ao governo. |
| R-05 | P8, P10 / UC-29, UC-30, UC-44 | Um usuário nega a emissão/cancelamento de uma nota ou a autorização de um pagamento. | Risco financeiro, fiscal e de desvio de recursos. |
| R-06 | P9 / UC-33 a UC-37 | O sistema não consegue provar qual credencial, integração ou operador enviou/recebeu um documento externo. | Falha na atribuição de transmissões e impossibilidade de auditar alterações entre sistemas. |
| R-07 | P11 / UC-38 a UC-41 | O próprio operador com acesso aos logs altera ou exclui evidências; a exportação não registra quem a realizou. | A trilha deixa de ter valor probatório e incidentes podem ser ocultados. |

### Controles recomendados

1. Registrar eventos de segurança e negócio com `actor_id`, empresa/tenant,
   ação, objeto afetado, data/hora em UTC, resultado, IP, dispositivo/sessão e
   correlação da requisição.
2. Guardar o valor anterior e o novo valor nas mudanças relevantes, além da
   origem (interface, API ou integração) e do protocolo retornado por serviços
   externos.
3. Tornar os logs append-only, com controle de acesso separado do ambiente de
   produção, retenção definida e cópias protegidas contra exclusão e alteração.
4. Exigir reautenticação/MFA e, para pagamentos, aprovação segregada; registrar
   a aprovação e a identidade dos envolvidos.
5. Alertar para exclusão, falha de gravação ou alteração de logs. A operação
   não deve ser considerada concluída quando a evidência obrigatória não puder
   ser persistida.

## 5.4 I — Information Disclosure (Divulgação de informação)

### Ameaças

| ID | Ponto/UC | Cenário de ameaça | Impacto |
|----|----------|-------------------|---------|
| I-01 | P1, P2 / UC-01, UC-03 | Mensagens de login e recuperação informam se um e-mail existe; tokens, sessões ou códigos MFA aparecem em logs ou respostas. | Facilita enumeração de contas e sequestro de identidade. |
| I-02 | P4 / UC-07 a UC-11 | CPF, CNPJ, dados societários e bancários são retornados para outro usuário, tenant ou integração por falha de autorização. | Violação de privacidade e exposição de dados financeiros. |
| I-03 | P5, P6 / UC-13 a UC-23 | Consultas, relatórios, livros e arquivos fiscais permitem acesso excessivo ou são exportados sem proteção. | Divulgação de dados contábeis e fiscais da empresa. |
| I-04 | P7 / UC-24 a UC-28 | Um funcionário acessa o holerite de outro, ou dados de folha/eSocial ficam visíveis em URLs, downloads ou logs. | Exposição de salários, documentos pessoais e informações trabalhistas. |
| I-05 | P8 / UC-29 a UC-32 | Links de PDF/XML, notas e relatórios são previsíveis, públicos ou entregues ao destinatário errado. | Exfiltração de documentos fiscais e dados de clientes. |
| I-06 | P9 / UC-33 a UC-37 | Chaves de API, certificados, extratos e respostas de serviços externos são transmitidos sem proteção ou armazenados em texto claro. | Comprometimento de integrações e vazamento em cadeia. |
| I-07 | P11 / UC-38 a UC-41 | Logs e exportações contêm valores, CPFs, tokens, payloads ou metadados de acesso em excesso. | Um recurso de auditoria torna-se fonte concentrada de vazamento. |
| I-08 | P10 / UC-42 a UC-45 | Notificações e boletos exibem dados de cobrança para destinatário incorreto ou permitem observação por terceiros. | Fraude, exposição financeira e phishing direcionado. |

### Controles recomendados

1. Aplicar autorização no servidor em toda leitura e download, validando
   simultaneamente usuário, tenant, objeto e finalidade; não confiar em IDs
   enviados pelo cliente.
2. Usar respostas uniformes para login/recuperação, tokens de uso único com
   expiração curta, cookies `Secure`/`HttpOnly`/`SameSite` e URLs de download
   assinadas e temporárias.
3. Criptografar dados sensíveis em trânsito e em repouso, armazenar segredos em
   cofre de credenciais e nunca registrar senha, token, certificado ou payload
   sensível em logs.
4. Minimizar dados retornados, mascarar CPF/dados bancários, limitar
   exportações e aplicar expiração, revogação e rastreabilidade aos arquivos.
5. Separar chaves por ambiente e integração, restringir escopos e revisar
   periodicamente retenção, acesso e compartilhamento conforme a LGPD.

## 5.5 D — Denial of Service (Negação de serviço)

### Ameaças

| ID | Ponto/UC | Cenário de ameaça | Impacto |
|----|----------|-------------------|---------|
| D-01 | P1, P2 / UC-01 a UC-03 | Tentativas automatizadas de login/MFA ou solicitações de recuperação provocam lockout e exaurem SMS, e-mail ou recursos de autenticação. | Usuários legítimos não conseguem acessar o sistema. |
| D-02 | P5 / UC-14 | Arquivo OFX/planilha muito grande, malformado ou repetido consome CPU, memória e espaço. | Importações e demais funções ficam lentas ou indisponíveis. |
| D-03 | P6 / UC-19 a UC-21 | Muitas apurações, gerações de SPED ou relatórios pesados são executadas simultaneamente. | Saturação do processamento e atraso de obrigações fiscais. |
| D-04 | P7 / UC-25, UC-28 | Processamento de folha em lote ou reenvio repetido ao eSocial ocupa filas e trabalhadores. | Folha e transmissões vencem o prazo. |
| D-05 | P8 / UC-31, UC-32 | Consultas e exportações sem paginação geram relatórios caros ou downloads concorrentes. | Degradação para todos os tenants e possível esgotamento de armazenamento. |
| D-06 | P9 / UC-33 a UC-36 | Dependência externa indisponível, timeout sem limite ou fila de integração sem backoff bloqueia requisições e acumula mensagens. | Operações bancárias, fiscais e sincronizações deixam de ser concluídas. |
| D-07 | P10 / UC-44 | Requisições duplicadas ou repetidas de pagamento ocupam o provedor e podem manter transações em estado inconsistente. | Indisponibilidade e risco de pagamentos duplicados. |

### Controles recomendados

1. Aplicar rate limiting por IP, conta, tenant e operação; usar backoff,
   limites de tentativas e filas separadas para autenticação, integrações e
   tarefas de negócio.
2. Validar tamanho, formato, quantidade de registros e tempo máximo de
   processamento de arquivos e relatórios; executar tarefas pesadas de forma
   assíncrona, com quota por tenant.
3. Definir timeout, retry limitado com jitter, circuit breaker e dead-letter
   queue para integrações. Não manter uma requisição síncrona aberta esperando
   uma dependência externa.
4. Usar idempotência e chave de deduplicação em pagamentos, transmissões e
   reprocessamentos.
5. Monitorar filas, latência, erros, uso de CPU/memória/armazenamento e
   disponibilidade das dependências, com alertas e procedimento de recuperação.

## 5.6 E — Elevation of Privilege (Elevação de Privilégio)

### Ameaças

| ID | Ponto/UC | Cenário de ameaça | Impacto |
|----|----------|-------------------|---------|
| E-01 | P3 / UC-04, UC-06 | Um administrador ou usuário manipula `role`, `user_id`, tenant ou permissões no cliente/API e obtém funções de outro perfil. | Acesso administrativo e alteração do modelo de autorização. |
| E-02 | P4, P5 / UC-07 a UC-18 | Falha de isolamento multi-tenant permite consultar ou alterar empresa, lançamento ou plano de contas usando outro identificador. | Acesso cruzado entre clientes e fraude contábil. |
| E-03 | P6 / UC-20 a UC-22 | Perfil operacional consegue retificar apuração, reabrir período ou emitir obrigação sem a aprovação exigida. | Alteração de obrigações fiscais e descumprimento de segregação de funções. |
| E-04 | P7, P8 / UC-26, UC-30 a UC-32 | Funcionário ou cliente acessa holerites, notas, cancelamentos ou relatórios de outro usuário/empresa. | Exposição de dados e execução de operações restritas. |
| E-05 | P9 / UC-37 | Usuário com permissão de configuração altera endpoint, escopo ou segredo e obtém acesso amplo às integrações. | Comprometimento de bancos, governo ou ERP do cliente. |
| E-06 | P10 / UC-44 | O mesmo ator cadastra beneficiário, altera valor e aprova o pagamento sem revisão independente. | Desvio financeiro com privilégio acumulado. |
| E-07 | P11 / UC-39, UC-41 | Usuário de auditoria acessa logs de outro tenant ou exporta evidências sem necessidade de negócio. | Privilégio indevido sobre dados e evidências sensíveis. |

### Controles recomendados

1. Implementar RBAC no servidor com deny-by-default, menor privilégio e
   validação de tenant em cada endpoint, consulta e comando; nunca aceitar o
   papel informado pelo cliente como autoridade.
2. Separar permissões de leitura, alteração, aprovação, configuração de
   credenciais e administração; exigir aprovação independente para pagamentos,
   retificações, cancelamentos e reabertura de períodos.
3. Revalidar autorização em cada etapa de uma operação e invalidar sessões e
   tokens quando perfil, vínculo ou empresa forem alterados.
4. Restringir credenciais de integração por escopo, serviço e ambiente;
   proteger alterações com MFA/reautenticação, revisão e trilha de auditoria.
5. Testar sistematicamente IDOR, acesso horizontal (outro usuário/tenant) e
   acesso vertical (perfil superior), incluindo operações de exportação e
   tarefas assíncronas.

## 5.7 Priorização

| Prioridade | Risco RIDE | Justificativa |
|------------|------------|---------------|
| Alta | E-02, E-03, E-06 | Podem permitir fraude entre empresas, alteração fiscal ou pagamento indevido. |
| Alta | I-02, I-04, I-06 | Envolvem dados pessoais, bancários, trabalhistas e credenciais de terceiros. |
| Alta | R-03, R-05, R-07 | Sem evidência confiável, incidentes financeiros e fiscais não podem ser investigados. |
| Média/Alta | D-03, D-04, D-06 | Indisponibilidade em fechamento, folha ou transmissão pode causar perda de prazo. |
| Média | D-01, D-02, D-05, D-07 | Devem ser tratados com limites e filas antes de afetarem o restante da plataforma. |

## 5.8 Critérios de verificação

- Cada ação de criação, alteração, exclusão, exportação, transmissão e
  aprovação possui evento de auditoria consultável e protegido contra alteração.
- Um usuário não acessa dados, arquivos ou operações de outro tenant mesmo
  quando altera IDs, parâmetros, URLs ou mensagens da requisição.
- Dados sensíveis não aparecem em mensagens de erro, URLs, logs ou respostas
  além do mínimo necessário.
- Operações custosas possuem limites, execução assíncrona, observabilidade e
  comportamento definido quando uma dependência externa falha.
- Mudanças de privilégio, credenciais, pagamentos e obrigações fiscais exigem
  autorização compatível com o risco e ficam registradas.
