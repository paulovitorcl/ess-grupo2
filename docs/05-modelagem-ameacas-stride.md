# 5. Modelagem de Ameaças com STRIDE 

Este documento detalha as seis categorias da metodologia **STRIDE** para o
sistema de contabilidade:

- **S — Spoofing (Falsificação de identidade):** um atacante se passa por um
  usuário ou sistema legítimo;
- **T — Tampering (Adulteração de dados):** dados, documentos ou configurações
  são modificados indevidamente;
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

| Fronteira | Componentes e dados | Riscos STRIDE prioritários |
|-----------|---------------------|--------------------------|
| Acesso externo | Web/API, login, MFA, recuperação de senha e RBAC | Falsificação de identidade, adulteração de requisições, repúdio de acesso, exposição por sessão, indisponibilidade por abuso e bypass de autorização |
| Núcleo e persistência | Cadastro, escrituração, fiscal, folha, pagamentos, banco de dados | Adulteração de dados financeiros, negação de alterações, vazamento entre empresas e acesso a funções administrativas |
| Auditoria | Trilha de auditoria e logs de acesso | Adulteração de registros, impossibilidade de provar ações, exposição de logs e perda da evidência |
| Integrações | Bancos, Receita Federal, prefeituras, eSocial e ERP | Falsificação de serviços, adulteração de mensagens, vazamento em trânsito, indisponibilidade de dependências e uso de credenciais com privilégio excessivo |

## 5.2 S — Spoofing (Falsificação de identidade)

Spoofing compromete a autenticação: o sistema aceita uma identidade que o
atacante não tem direito de utilizar. Os cenários abaixo são hipóteses de
ameaça, condicionadas às falhas descritas, e não vulnerabilidades comprovadas
em uma implementação.

### Ameaças

| ID | Ponto/UC | Cenário de ameaça | Impacto |
|----|----------|-------------------|---------|
| S-01 | P1 / UC-01, UC-02 | Um atacante utiliza credenciais vazadas de outros serviços. Se não houver limitação adequada de tentativas e o MFA estiver desabilitado ou puder ser contornado, obtém uma sessão como contador, cliente ou administrador. | Acesso indevido a dados e operações em nome da vítima. |
| S-02 | P1 / UC-02 | Um atacante que conhece a senha e obtém um código MFA da vítima, por exemplo por phishing, reutiliza esse código após seu uso legítimo. Se o servidor aceitar novamente o código dentro de sua validade, o atacante conclui a autenticação. | Superação do segundo fator e falsificação da identidade do usuário. |
| S-03 | P2 / UC-03 | O atacante obtém um token de recuperação para sua própria conta e altera o identificador da conta na confirmação. Se o servidor não vincular o token à conta original, redefine a senha de outro cliente. | Sequestro da conta do cliente sem acesso ao e-mail da vítima. |
| S-04 | P1 / UC-01, UC-05 | Um atacante reutiliza um identificador de sessão roubado que continua válido após logout ou expiração por inatividade, por ausência de invalidação no servidor. | Operações realizadas como usuário legítimo sem apresentar novamente suas credenciais. |
| S-05 | P9 / UC-09, UC-33 a UC-36 | A aplicação aceita um servidor falso como banco, órgão fiscal ou ERP por não validar corretamente o certificado TLS e a identidade do destino. | Envio de informações ao atacante e aceitação de respostas de origem falsa. |
| S-06 | P7, P8, P9 / UC-28, UC-29, UC-35, UC-37 | Um atacante utiliza uma chave privada de certificado digital ou credencial de API obtida indevidamente para se apresentar como a empresa perante um serviço externo. | Transmissões e operações fraudulentas atribuídas à empresa. |

### Controles recomendados

1. **S-01 e S-02:** exigir MFA nos acessos previstos pelo modelo, com preferência
   por autenticadores resistentes a phishing, como WebAuthn/FIDO2; limitar
   tentativas por conta e origem, evitando bloqueios permanentes exploráveis
   para negação de serviço. Vincular o fluxo de autenticação à conta e à sessão,
   limitar a validade dos códigos e rejeitar sua reutilização após sucesso.
2. **S-03:** gerar tokens de recuperação imprevisíveis, de uso único e com
   expiração; associá-los à conta no servidor. Não permitir que um `user_id`
   enviado pelo cliente substitua essa associação. Notificar o titular e
   invalidar as sessões existentes após a recuperação.
3. **S-04:** proteger cookies de sessão com `Secure`, `HttpOnly` e `SameSite`,
   renovar o identificador após autenticação e aplicar expiração e revogação
   efetivas no servidor, inclusive no logout.
4. **S-05:** validar cadeia de confiança, validade do certificado e nome do
   servidor nas conexões TLS; restringir destinos de integração aprovados e
   adotar autenticação mútua quando suportada e exigida pela integração.
5. **S-06:** manter segredos e chaves privadas em armazenamento protegido, com
   acesso mínimo, rotação e revogação; exigir reautenticação para alterações
   de credenciais e restringir seu uso por empresa, serviço e ambiente.

### Relação com os casos de abuso

- **CA01 → S-01:** uso de credenciais vazadas para assumir uma identidade.
  O sucesso pressupõe MFA ausente ou contornado.
- **CA02 → S-03:** recuperação aplicada à conta errada por falta de vínculo
  entre token e titular. S-03 explicita uma premissa ainda ausente no fluxo do
  CA02: o atacante dispõe de um token válido da própria conta. A relação é
  temática; o caso de abuso precisa incorporar essa premissa para descrever
  a mesma sequência.

## 5.3 T — Tampering (Adulteração de dados)

Tampering compromete a integridade: o atacante modifica dados ou configurações
sem autorização, inclusive usando uma conta legítima. Uma mesma ocorrência
pode também envolver elevação de privilégio e repúdio; aqui o foco é a
alteração indevida e seu efeito no negócio.

### Ameaças

| ID | Ponto/UC | Cenário de ameaça | Impacto |
|----|----------|-------------------|---------|
| T-01 | P3 / UC-04, UC-06 | Um usuário inclui campos como `role` e permissões em uma requisição que os grava sem verificar quais campos e alterações são autorizados. | Adulteração do modelo de acesso e concessão de privilégios indevidos. |
| T-02 | P4 / UC-07, UC-10, UC-11 | Um invasor de conta ou usuário interno altera regime tributário, plano de contas ou dados bancários sem a validação e aprovação exigidas para a mudança. | Cálculos distorcidos e, quando os dados alterados determinam o beneficiário, desvio de pagamentos. |
| T-03 | P5 / UC-13 a UC-17 | Um usuário altera valores de lançamentos, importa registros manipulados ou modifica um período encerrado porque o servidor não verifica as regras contábeis e o estado do período. | Saldos incorretos, conciliações fraudulentas e perda de integridade da escrituração. |
| T-04 | P6, P8 / UC-19 a UC-22, UC-29 a UC-32 | O atacante modifica bases de cálculo, itens de notas ou conteúdo de arquivos fiscais entre a geração, a aprovação e o envio, sem nova validação. | Guias, notas, SPED e relatórios com conteúdo diferente do aprovado. |
| T-05 | P7 / UC-24 a UC-28 | Um usuário modifica rubricas, salários ou verbas após a revisão da folha, e o processamento utiliza a versão modificada sem exigir nova aprovação. | Pagamentos incorretos e transmissão de eventos trabalhistas adulterados. |
| T-06 | P9 / UC-33 a UC-37 | Um atacante altera o endpoint configurado ou mensagens de integração que não têm sua integridade e origem verificadas conforme o protocolo. | Importação de extratos ou dados falsos e sincronização de informações adulteradas. |
| T-07 | P10 / UC-44 | O atacante altera valor, beneficiário ou dados da guia após a aprovação, e o sistema executa o pagamento sem conferir os dados autorizados. | Desvio financeiro ou execução de transação diferente daquela aprovada. |
| T-08 | P11 / UC-38 a UC-41 | Um operador com permissão de escrita modifica ou exclui registros de auditoria ou substitui um arquivo exportado sem que a alteração seja detectada. | Ocultação de fraude, atribuição falsa de autoria e perda de confiabilidade das evidências. |

### Controles recomendados

1. **T-01 e T-02:** validar autorização por campo, operação e empresa no
   servidor; aceitar apenas campos previstos para a operação. Exigir revisão
   independente para mudanças críticas de permissões e dados bancários.
2. **T-03:** validar arquivos e registros importados, conferir totais e regras
   contábeis, usar transações e controlar alterações concorrentes. Bloquear
   gravações em períodos encerrados e exigir fluxo autorizado de reabertura.
3. **T-04 e T-05:** versionar dados e documentos aprovados; qualquer alteração
   relevante deve invalidar a aprovação anterior. Conferir a versão antes de
   processar ou transmitir e usar assinatura digital quando aplicável.
4. **T-06:** proteger o transporte com TLS e validar mensagens conforme o
   contrato da integração, incluindo assinatura ou MAC quando previstos.
   Restringir e auditar alterações de endpoints. Um hash enviado junto do
   arquivo, ambos modificáveis pelo atacante, não comprova sua autenticidade.
5. **T-07:** vincular a aprovação ao valor, beneficiário e demais dados
   significativos da transação; conferir esse vínculo no momento da execução.
   Alterações devem exigir nova aprovação. Aplicar idempotência para impedir
   efeitos financeiros duplicados em reenvios.
6. **T-08:** separar permissões da aplicação e da auditoria, manter registros
   append-only e cópias protegidas; verificar a integridade de exportações por
   assinatura ou referência protegida. Alertar sobre tentativas de alteração
   e falhas de gravação. A auditoria auxilia na detecção e investigação, mas
   não substitui os controles que impedem alterações indevidas.

### Relação com os casos de abuso

- **CA04 → T-01:** adulteração de papéis e permissões.
- **CA05 → T-02:** troca de dados bancários e desvio de pagamento. T-07 aborda
  uma variante, com alteração após a aprovação, não explicitada no CA05.
- **CA06 → T-05:** ambos envolvem alteração indevida de valores da folha;
  T-05 detalha a variante após revisão, enquanto CA06 também inclui sobrecarga.
- **CA09 → T-08:** modificação de registros para ocultar ou atribuir a fraude
  a outra pessoa.

## 5.4 R — Repudiation (Repúdio)

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

## 5.5 I — Information Disclosure (Divulgação de informação)

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

## 5.6 D — Denial of Service (Negação de serviço)

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

## 5.7 E — Elevation of Privilege (Elevação de Privilégio)

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

## 5.8 Priorização

As prioridades são qualitativas e preliminares. Para ST, considera-se **Alta**
a necessidade de tratar caminhos de tomada de conta ou fraude financeira
direta; **Média** indica cenários que, além da falha descrita, dependem de
acesso adicional a códigos, sessões, mensagens ou registros protegidos.
Essa distinção orienta a ordem inicial de análise, sem reduzir a gravidade
do impacto. Não foram estimadas probabilidades nem medido o risco residual.
As classificações devem ser revistas conforme a implementação e a exposição
real; por exemplo, um armazenamento de sessões ou logs exposto eleva a urgência.
As linhas de RI e DE mantêm as prioridades propostas nas respectivas análises.

| Prioridade | Risco STRIDE | Justificativa |
|------------|------------|---------------|
| Alta | S-01, S-03, S-06 | Permitem tomada de conta por credenciais, recuperação indevida ou uso de identidade empresarial comprometida, com possibilidade de operações externas. |
| Média | S-02, S-04, S-05 | Exigem também obter um código ou sessão da vítima, ou conseguir intermediar/redirecionar uma conexão; o impacto potencial permanece elevado. |
| Alta | T-01, T-02, T-03, T-04, T-05, T-07 | Afetam permissões, valores, obrigações ou pagamentos por operações de negócio expostas ao usuário. |
| Média | T-06, T-08 | Pressupõem acesso à configuração ou às mensagens de integração, ou permissão de escrita sobre evidências; tornam-se urgentes se esses acessos estiverem expostos. |
| Alta | E-02, E-03, E-06 | Podem permitir fraude entre empresas, alteração fiscal ou pagamento indevido. |
| Alta | I-02, I-04, I-06 | Envolvem dados pessoais, bancários, trabalhistas e credenciais de terceiros. |
| Alta | R-03, R-05, R-07 | Sem evidência confiável, incidentes financeiros e fiscais não podem ser investigados. |
| Média/Alta | D-03, D-04, D-06 | Indisponibilidade em fechamento, folha ou transmissão pode causar perda de prazo. |
| Média | D-01, D-02, D-05, D-07 | Devem ser tratados com limites e filas antes de afetarem o restante da plataforma. |

## 5.9 Critérios de verificação

- **S-01 e S-02:** uma senha correta não libera operações protegidas antes do
  MFA; códigos usados, expirados ou pertencentes a outra conta são rejeitados,
  e concluir o desafio em uma sessão não autentica outra sessão pendente.
- **S-03:** um token da conta A não redefine a senha da conta B; tokens
  expirados ou já utilizados são rejeitados sem alterar a senha.
- **S-04:** uma sessão encerrada ou expirada não permite novas operações.
- **S-05:** conexões com certificado expirado, cadeia não confiável ou nome
  de servidor incompatível são rejeitadas.
- **S-06:** usuários sem permissão não conseguem acessar chaves privadas nem
  acionar operações com elas; a revogação é validada em ambiente de teste do
  provedor, considerando também tokens derivados e os prazos do protocolo.
- **T-01 e T-02:** alterações de campos protegidos sem autorização são negadas
  e não modificam os registros; mudanças críticas exigem a aprovação prevista.
- **T-03:** importações inconsistentes e gravações em períodos encerrados são
  rejeitadas sem deixar alterações parciais.
- **T-04, T-05 e T-07:** alterar dados após a aprovação impede a execução ou
  transmissão até nova aprovação da versão modificada.
- **T-06:** mensagens que falham nas verificações de integridade previstas
  pelo protocolo são rejeitadas e não atualizam dados de negócio; alterações
  de endpoint por um usuário sem permissão não são persistidas.
- **T-08:** a conta da aplicação não consegue editar ou excluir a trilha;
  adulterações em exportações são detectadas pela verificação de integridade.
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

## 5.10 Referências de apoio para ST

- OWASP. [Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html).
- OWASP. [Multifactor Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html).
- OWASP. [Forgot Password Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html).
- OWASP. [Transaction Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html).
- OWASP. [Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html).
