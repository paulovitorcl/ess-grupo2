# 6. Casos de abuso

### CA01 - Credential Stuffing e Ataque de Força Bruta para Invasão de Conta Contábil

**Ator**: Atacante externo

**Objetivo**: Invadir contas de contadores ou clientes para acessar dados financeiros ou realizar operações não autorizadas

**Condições necessárias**:

- O sistema disponibiliza interface de autenticação por e-mail e senha sem limite adequado de tentativas de login ou CAPTCHA
- O atacante possui listas de credenciais vazadas em outros serviços

**Fluxo de abuso**

1- O atacante automatiza um script de credential stuffing contra a tela de login \
2- O sistema processa múltiplas tentativas por segundo sem bloquear a origem\
3- O atacante identifica um par de e-mail e senha válido e obtém a sessão do usuário\
4- O atacante navega pelo painel da empresa associada à conta comprometida\
5- O usuário legítimo tem sua conta acessada sem seu consentimento

**Impacto esperado**: Acesso não autorizado a dados contábeis sensíveis, representação fraudulenta do usuário e violação de confidencialidade

**Categorias STRIDE relacionadas**: Spoofing, Repudiation, Information Disclosure e Denial of Service.

---

### CA02 - Burlar ou Bloquear a Autenticação de Dois Fatores (MFA)

**Ator**: Atacante externo

**Objetivo**: Superar a verificação de segundo fator para concluir o login ou esgotar a cota de envios de código da vítima

**Condições necessárias**:

- O sistema exige autenticação em duas etapas via SMS/E-mail/App para acesso às contas
- O atacante possui as credenciais primárias do usuário (usuário e senha)

**Fluxo de abuso**

1- O atacante realiza o login primário e é solicitado a inserir o código MFA\
2- O atacante dispara requisições massivas de envio de código para esgotar a cota de envio do usuário ou utiliza técnicas de phishing/SIM swap\
3- O atacante intercepta ou força a validação do código de verificação\
4- O sistema aceita a validação forjada ou o usuário legítimo fica bloqueado sem receber seu código\
5- O atacante obtém acesso total ao sistema de contabilidade

**Impacto esperado**: Bypassing do controle de acesso, bloqueio do usuário legítimo e exposição do sistema a acessos indevidos

**Categorias STRIDE relacionadas**: Spoofing e Denial of Service.

---

### CA03 - Sequestro de Conta via Manipulação do Token de Recuperação de Senha

**Ator**: Atacante externo

**Objetivo**: Alterar a senha de um cliente ou administrador para assumir o controle permanente da conta

**Condições necessárias**:

- O sistema disponibiliza funcionalidade de recuperação de senha via link/token
- O fluxo de recuperação apresenta identificadores previsíveis (`user_id`) ou validação fraca de token

**Fluxo de abuso**

1- O atacante solicita a redefinição de senha informando o e-mail da vítima\
2- O atacante intercepta a requisição de redefinição e altera o parâmetro de identificação para o ID da conta alvo\
3- O sistema gera o link/token de redefinição associando-o ou aplicando-o à conta da vítima\
4- O atacante define uma nova senha para a conta da vítima sem possuir acesso ao e-mail dela\
5- O atacante realiza login com a nova senha e expulsa o usuário legítimo da plataforma

**Impacto esperado**: Perda total de controle da conta do cliente ou administrador, vazamento de informações e escalada de privilégios

**Categorias STRIDE relacionadas**: Spoofing, Information Disclosure e Elevation of Privilege.

---

### CA04 - Criação Fraudulenta de Contas Privilegiadas sem Rastro de Auditoria

**Ator**: Usuário mal-intencionado ou conta administrativa comprometida

**Objetivo**: Criar contas fictícias com permissões administrativas para manter acesso persistente ou desativar contas de auditores

**Condições necessárias**:

- O sistema possui interface para gerenciamento, criação e desativação de contas
- Ausência de checagem estrita de autorização no endpoint ou falha na gravação do log de autoria

**Fluxo de abuso**

1- O atacante acessa a funcionalidade de gerenciamento de usuários \
2- O atacante envia uma requisição para criar uma nova conta de usuário atribuindo perfil de administrador\
3- O sistema cria a conta sem exigir aprovação dupla ou reautenticação\
4- O atacante desativa a conta de administradores ou auditores legítimos para impedir a revogação de seu acesso\
5- O atacante passa a operar no sistema com controle total sem que sua ação fique vinculada à conta de origem

**Impacto esperado**: Persistência de acessos não autorizados, negação de repúdio para ações administrativas e bloqueio de usuários legítimos

**Categorias STRIDE relacionadas**: Repudiation e Elevation of Privilege.

---

### CA05 - Hijacking de Sessão Ativa por Falha na Expiração por Inatividade

**Ator**: Atacante local / físico ou atacante em rede compartilhada

**Objetivo**: Assumir uma sessão contábil abandonada em um terminal para realizar operações não autorizadas

**Condições necessárias**:

- O usuário legítimo deixa a estação de trabalho logada no sistema de contabilidade 
- O sistema falha em encerrar a sessão no lado do servidor ou valida tokens expirados

**Fluxo de abuso**

1- O usuário legítimo se afasta da estação de trabalho deixando a sessão aberta\
2- O sistema falha em invalidar os tokens de acesso ou prorroga a sessão indefinidamente\
3- O atacante se aproxima do terminal ou reutiliza os tokens capturados no navegador\
4- O atacante executa transações contábeis e consultas em nome do usuário logado\
5- O usuário retorna sem perceber que sua sessão foi utilizada por terceiros

**Impacto esperado**: Usurpação de identidade do usuário, realização de lançamentos e consultas não autorizadas

**Categorias STRIDE relacionadas**: Spoofing.

---

### CA06 - Escalada de Privilégios por Manipulação de Matriz de Permissões (RBAC)

**Ator**: Usuário operacional mal-intencionado

**Objetivo**: Alterar a atribuição de papéis e permissões para conceder a si próprio privilégios de gestão financeira

**Condições necessárias**:

- O sistema utiliza controle de acesso baseado em papéis (RBAC) para restringir funcionalidades 
- As requisições de alteração de permissão não validam adequadamente se o solicitante possui papel de administrador

**Fluxo de abuso**

1- O atacante com perfil comum intercepta a requisição de atualização do seu perfil de usuário \
2- O atacante adiciona parâmetros de permissões administrativas (ex.: `role=admin` ou `permissions=all`)\
3- O sistema processa a alteração sem validar os privilégios do autor da requisição\
4- As novas permissões são salvas e aplicadas à conta do atacante\
5- O atacante passa a acessar módulos restritos, como escrituração, relatórios e pagamentos

**Impacto esperado**: Quebra da política de segurança RBAC, acesso irrestrito a dados sensíveis e execução de ações não autorizadas

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

---

### CA07 - Fraude Fiscal por Alteração do Regime Tributário no Cadastro da Empresa

**Ator**: Usuário interno malicioso ou consultor contábil não autorizado

**Objetivo**: Modificar o regime tributário ou CNPJ de uma empresa para adulterar a apuração de impostos e sonegar tributos

**Condições necessárias**:

- O sistema permite o cadastro e edição das informações cadastrais das empresas 
- O fluxo não exige validação prévia de documentos fiscais oficiais para alteração de regime tributário

**Fluxo de abuso**

1- O atacante acessa a tela de cadastro e edição de empresas \
2- O atacante altera o regime tributário da empresa de Lucro Real para Simples Nacional ou altera o CNPJ cadastrado\
3- O sistema salva as novas informações sem exigir confirmação documental ou log de alteração com assinatura\
4- A apuração subsequente de impostos calcula tributos com base nas regras do regime incorreto\
5- A empresa passa a emitir impostos com valores defasados ou incorretos perante a Receita Federal

**Impacto esperado**: Apuração fiscal fraudulenta, sonegação involuntária de impostos, multas pesadas e exposição de dados cadastrais

**Categorias STRIDE relacionadas**: Tampering, Repudiation, Information Disclosure.

---

### CA08 - Injeção de Sócios Fictícios e Exposição de Dados Pessoais (CPF)

**Ator**: Atacante interno ou usuário com privilégio de edição

**Objetivo**: Vincular CPFs de terceiros a empresas fraudulentas para lavar dinheiro ou expor dados pessoais dos sócios

**Condições necessárias**:

- O sistema permite o vínculo e atualização do quadro de sócios e responsáveis legais por CPF 
- Ausência de validação cruzada dos dados do sócio com a base oficial no momento do vínculo

**Fluxo de abuso**

1- O atacante acessa o módulo de vinculação de sócios da empresa \
2- O atacante insere o CPF e dados de uma pessoa física alheia sem autorização\
3- O sistema registra o vínculo sem validar o consentimento ou a autenticidade do documento\
4- O atacante utiliza a empresa para operações irregulares responsabilizando o sócio fictício\
5- Dados sensíveis do sócio legítimo ficam expostos na plataforma para usuários não autorizados

**Impacto esperado**: Fraude societária, vazamento de dados pessoais (LGPD) e responsabilização indevida de terceiros

**Categorias STRIDE relacionadas**: Tampering e Information Disclosure.

---

### CA09 - Interceptação e Adulteração da Resposta de Validação de CNPJ (MITM)

**Ator**: Atacante em posição de rede (Man-in-the-Middle) ou servidor forjado

**Objetivo**: Simular a validação positiva de um CNPJ inapto ou suspenso para liberar cadastros irregulares

**Condições necessárias**:

- O sistema realiza requisições externas para validação de CNPJ junto ao servidor da Receita Federal
- A comunicação não utiliza validação rigorosa de certificado SSL/TLS (certificate pinning)

**Fluxo de abuso**

1- O usuário aciona a consulta de validação de CNPJ na Receita Federal \
2- O atacante intercepta a comunicação entre o sistema de contabilidade e a API externa\
3- O atacante altera a resposta HTTP substituindo a situação "Inapta/Baixada" por "Ativa"\
4- O sistema recebe a resposta adulterada e aprova o cadastro da empresa irregular\
5- O atacante opera no sistema com uma empresa fantasma aprovada pelo mecanismo

**Impacto esperado**: Ingressão de empresas fraudulentas no sistema, bypass de verificações de conformidade e exposição de dados de tráfego

**Categorias STRIDE relacionadas**: Spoofing e Tampering e Information Disclosure.

---

### CA10 - Sabotagem da Estrutura Contábil por Adulteração do Plano de Contas

**Ator**: Usuário não autorizado com privilégios mal configurados

**Objetivo**: Alterar a hierarquia e natureza das contas contábeis para desorganizar os balancetes e mascarar lançamentos

**Condições necessárias**:

- O sistema permite a configuração e personalização do plano de contas da empresa 
- Falha na restrição de privilégios para edição de contas sintéticas e analíticas

**Fluxo de abuso**

1- O atacante acessa a tela de configuração do plano de contas \
2- O atacante altera a classificação de contas de despesas para contas do ativo ou deleta contas essenciais\
3- O sistema salva a nova estrutura sem gerar log detalhado da alteração nem exigir aprovação do contador chefe\
4- Os novos lançamentos contábeis são direcionados para contas incorretas\
5- Os relatórios e balancetes gerados ficam completamente distorcidos e incoerentes

**Impacto esperado**: Perda de integridade da contabilidade, inviabilização de auditorias e distorção de demonstrações financeiras

**Categorias STRIDE relacionadas**: Tampering e Repudiation e Elevation of Privilege.

---

### CA11 - Desvio de Pagamentos por Troca de Dados Bancários Cadastrais

**Ator**: Atacante interno ou invasor de conta

**Objetivo**: Substituir a conta bancária ou chave Pix de um cliente/fornecedor para desviar transferências financeiras

**Condições necessárias**:

- O sistema permite o cadastro e atualização de dados bancários
- O sistema não exige confirmação por MFA ou notificação ao titular antes da alteração dos dados bancários

**Fluxo de abuso**

1- O atacante acessa a funcionalidade de atualização de dados bancários\
2- O atacante insere os dados de sua própria conta bancária ou chave Pix no cadastro da vítima\
3- O sistema salva a nova conta bancária sem exigir aprovação por um segundo usuário\
4- As rotinas automatizadas de pagamento utilizam os novos dados bancários adulterados\
5- O pagamento de guias, reembolsos ou fornecedores é transferido para a conta do atacante

**Impacto esperado**: Prejuízo financeiro direto, fraude em pagamentos e vazamento de dados bancários

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA12 - Inativação Prematura de Empresa para Ocultação de Passivos Tributários

**Ator**: Usuário com permissão indevida ou administrador cooptado

**Objetivo**: Inativar o cadastro de uma empresa com pendências fiscais para travar o processamento de obrigações e ocultar dívidas

**Condições necessárias**:

- O sistema possui funcionalidade de inativação de empresas encerradas
- Falha na validação de dependências (se existem obrigações fiscais pendentes) antes de permitir a inativação

**Fluxo de abuso**

1- O atacante aciona o módulo de inativação de empresas \
2- O atacante seleciona uma empresa ativa com tributos e apurações pendentes e solicita sua inativação\
3- O sistema altera o status da empresa sem validar pendências fiscais ou exigir assinatura do contador\
4- As rotinas de apuração automática ignoram a empresa inativada\
5- As obrigações fiscais vencem sem envio ao governo, gerando multas para a empresa legítima

**Impacto esperado**: Ocultação fraudulenta de passivos, geração de multas regulatórias e quebra de compliance

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

---

### CA13 - Lançamento Contábil Fraudulento para Encobertamento de Saída de Caixa

**Ator**: Funcionário contábil mal-intencionado

**Objetivo**: Inserir lançamentos fictícios de débito e crédito para equilibrar o balanço após desvio de recursos

**Condições necessárias**:

- O sistema disponibiliza funcionalidade de lançamento manual de débito e crédito
- Permissões de escrita atribuídas a usuários com perfil de consulta ou falta de limite de alçada para lançamentos

**Fluxo de abuso**

1- O atacante acessa a tela de escrituração e registro de lançamentos \
2- O atacante insere um lançamento manual criando uma despesa fictícia contra a conta de caixa/banco\
3- O sistema aceita o lançamento sem exigir documento comprobatório anexado\
4- As demonstrações financeiras passam a refletir uma despesa falsa equilibrando as contas\
5- O atacante nega ter realizado o lançamento devido à ausência de trilha rígida de auditoria na sessão

**Impacto esperado**: Fraude contábil, adulteração de resultados e exposição financeira não autorizada

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure e Elevation of Privilege.

---

### CA14 - Injeção de Arquivo Lote Adulterado e Negação de Serviço por Carga Volumosa

**Ator**: Atacante externo ou interno com acesso à carga de arquivos

**Objetivo**: Injetar milhares de lançamentos falsos ou travar a aplicação com um arquivo malformado/volumoso

**Condições necessárias**:

- O sistema permite a importação de lançamentos contábeis em lote através de arquivos CSV/Excel/OFX 
- Ausência de validação de tamanho máximo de arquivo e sanitização de dados no upload

**Fluxo de abuso**

1- O atacante prepara um arquivo de lote contendo lançamentos adulterados ou milhões de linhas nulas/inválidas\
2- O atacante faz o upload do arquivo no módulo de importação em lote \
3- O sistema inicia o processamento síncrono do arquivo sem limitar recursos de CPU e memória\
4- O processamento consome os recursos do servidor, tornando o sistema lento ou inacessível para outros usuários\
5- Lançamentos adulterados presentes no arquivo são gravados na base de dados

**Impacto esperado**: Indisponibilidade do serviço (DoS), corrupção da base contábil por carga maliciosa e vazamento de dados financeiros no arquivo

**Categorias STRIDE relacionadas**: Tampering, Repudiation, Information Disclosure e Denial of Service.

---

### CA15 - Manipulação de Matches da Conciliação Bancária para Ocultação de Divergências

**Ator**: Contador ou assistente financeiro mal-intencionado

**Objetivo**: Forçar o vínculo (match) entre lançamentos contábeis e extratos bancários divergentes para ocultar desfalques

**Condições necessárias**:

- O sistema possui interface para conciliação bancária de lançamentos versus extratos 
- O algoritmo permite aprovação manual de divergências sem necessidade de justificativa formal ou trava

**Fluxo de abuso**

1- O atacante acessa a funcionalidade de conciliação bancária \
2- O atacante identifica lançamentos no extrato bancário sem correspondência nos livros contábeis\
3- O atacante vincula manualmente um lançamento fictício de valor diferente para fechar a conciliação\
4- O sistema registra a conciliação como "concluída com sucesso"\
5- As divergências de caixa ficam mascaradas e os relatórios financeiros passam a exibir saldos irreais

**Impacto esperado**: Ocultação de desvios financeiros, falsificação de saldos em balancetes e exposição de dados de extratos

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA16 - Estorno Indevido de Lançamentos para Alteração de Resultados Fiscais

**Ator**: Usuário com perfil operacional contábil

**Objetivo**: Estornar receitas legítimas já contabilizadas para reduzir artificialmente o faturamento e o imposto devido

**Condições necessárias**:

- O sistema permite o estorno e ajuste de lançamentos contábeis previamente realizados 
- Ausência de controle de permissão estrita ou falta de gravação do valor original antes do estorno

**Fluxo de abuso**

1- O atacante navega até a lista de lançamentos contábeis da empresa \
2- O atacante seleciona lançamentos de receita de alto valor e aciona a opção de estorno\
3- O sistema executa o estorno anulando o saldo sem exigir motivo justificado ou aprovação do supervisor\
4- A base de cálculo de impostos do período é reduzida drasticamente\
5- Ao ser questionado, o atacante tenta negar a autoria alegando falha do sistema

**Impacto esperado**: Sonegação fiscal, distorção de balancetes e quebra da imutabilidade contábil

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

---

### CA17 - Reabertura Não Autorizada de Período Fechado para Adulteração Histórica

**Ator**: Usuário sem privilégio elevado ou atacante com sessão capturada

**Objetivo**: Desbloquear um período contábil e fiscal encerrado para inserir lançamentos retroativos fraudulentos

**Condições necessárias**:

- O sistema disponibiliza o bloqueio e encerramento de períodos contábeis
- A verificação de permissão para reabertura de período é realizada apenas no front-end

**Fluxo de abuso**

1- O atacante acessa a funcionalidade de gestão de períodos contábeis \
2- O atacante burla a validação da interface e envia uma requisição direta à API solicitando a reabertura do período encerrado\
3- O sistema reabre o período sem verificar se o usuário possui perfil de contador chefe/administrador\
4- O atacante insere lançamentos contábeis com datas retroativas alterando o resultado de exercícios passados\
5- O atacante encerra novamente o período contábil

**Impacto esperado**: Alteração ilegal de demonstrações financeiras já publicadas, perda de confiabilidade nas demonstrações e fraudes societárias

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

---

### CA18 - Exfiltração de Livro-Razão entre Empresas por Vulnerabilidade IDOR

**Ator**: Cliente ou usuário externo autenticado

**Objetivo**: Visualizar e baixar a escrituração completa (Razão/Diário) de outras empresas cadastradas na plataforma

**Condições necessárias**:

- O sistema disponibiliza consulta ao Livro-Razão e Diário das empresas
- O sistema recebe o identificador da empresa (`company_id`) no parâmetro da URL sem validar se o usuário pertence a ela

**Fluxo de abuso**

1- O atacante faz login no sistema com a sua conta de cliente\
2- O atacante acessa a consulta do Livro-Razão e captura a requisição HTTP\
3- O atacante altera o parâmetro `company_id=101` para `company_id=102` (pertencente a um concorrente)\
4- O sistema processa a consulta sem validar o escopo de permissão tenant/empresa\
5- O atacante visualiza toda a movimentação financeira, fornecedores e clientes do concorrente

**Impacto esperado**: Vazamento massivo de segredos de negócio e dados financeiros, violando a privacidade das empresas clientes

**Categorias STRIDE relacionadas**: Information Disclosure e Elevation of Privilege.

---

### CA19 - Adulteração da Memória de Cálculo Fiscal e Exaustão de Processamento

**Ator**: Atacante interno ou usuário disparando apurações concorrentes

**Objetivo**: Alterar as alíquotas de apuração de impostos ou travar o módulo fiscal através de apurações massivas

**Condições necessárias**:

- O sistema realiza o cálculo automático e apuração dos impostos incidentes no período 
- Parâmetros de cálculo expostos na requisição e ausência de limite para requisições síncronas de apuração

**Fluxo de abuso**

1- O atacante intercepta a requisição de acionamento da apuração de impostos \
2- O atacante altera os parâmetros de alíquota ou envia solicitações de apuração para múltiplos períodos simultaneamente\
3- O sistema efetua os cálculos com os parâmetros manipulados ou consome todos os recursos de CPU para processar as requisições concorrentes\
4- As guias fiscais são geradas com valores zerados ou o serviço de cálculo fica indisponível\
5- Os usuários não conseguem apurar os impostos no dia do encerramento fiscal

**Impacto esperado**: Geração de guias fiscais incorretas, indisponibilidade do módulo fiscal e penalidades por atraso

**Categorias STRIDE relacionadas**: Tampering, Repudiation, Information Disclosure e Denial of Service.

---

### CA20 - Adulteração do Código de Barras e Dados de Pagamento de Guias Fiscais

**Ator**: Atacante em rede ou usuário interno mal-intencionado

**Objetivo**: Alterar a linha digitável e favorecido da guia DARF/DAS para desviar pagamentos de impostos para contas de terceiros

**Condições necessárias**:

- O sistema gera e disponibiliza a emissão das guias de recolhimento DARF/DAS em PDF/HTML 
- As guias são geradas sem validação de integridade ou assinatura digital no documento

**Fluxo de abuso**

1- O usuário solicita a emissão da guia DARF/DAS para pagamento \
2- O atacante intercepta a geração do PDF/guia e altera o código de barras e a conta favorecida registrada\
3- O sistema entrega a guia contendo o código de barras alterado ao cliente\
4- O cliente realiza o pagamento da guia acreditando estar quitando tributos federais/municipais\
5- O valor é depositado na conta do atacante e a Receita Federal aponta inadimplência da empresa

**Impacto esperado**: Desvio de recursos financeiros, não quitação de obrigações tributárias e aplicação de multas pelo fisco

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA21 - Injeção de Dados Falsos e Negação de Serviço na Geração do Arquivo SPED

**Ator**: Atacante interno ou usuário disparando gerações volumosas

**Objetivo**: Alterar os registros contábeis no arquivo SPED entregue à Receita Federal ou causar colapso do servidor

**Condições necessárias**:

- O sistema compila a base de dados contábil e fiscal para gerar a estrutura de arquivo do SPED 
- O processo de geração é computacionalmente pesado e síncrono

**Fluxo de abuso**

1- O atacante altera registros de blocos do SPED na base de dados ou aciona a geração do arquivo para anos inteiros simultaneamente \
2- O sistema inicia o processamento de compilação dos registros sem sanitização ou controle de concorrência\
3- O arquivo gerado contém inconsistências propositais ou o processo consome 100% da memória do servidor\
4- O sistema cai para todos os usuários impedindo o envio do SPED no prazo limite\
5- Se gerado com alterações, o arquivo é rejeitado pelo validador da Receita Federal

**Impacto esperado**: Indisponibilidade do sistema, rejeição da escrituração digital pelo fisco e multas severas por atraso

**Categorias STRIDE relacionadas**: Tampering, Information Disclosure e Denial of Service.

---

### CA22 - Retificação Fraudulenta Não Autorizada de Apurações Fiscais

**Ator**: Usuário com acesso operacional sem perfil de gestão

**Objetivo**: Retificar a apuração de impostos já entregue ao governo para cancelar débitos fiscais de forma ilegítima

**Condições necessárias**:

- O sistema permite a validação e envio de retificação de apurações fiscais 
- Falha no controle de permissão (RBAC) que permite a usuários comuns acionar a retificação

**Fluxo de abuso**

1- O atacante acessa o módulo de retificação de apuração\
2- O atacante submete uma retificação alterando a apuração original e reduzindo o imposto devido a zero\
3- O sistema envia a retificação sem exigir aprovação e sem assinar digitalmente a operação com o certificado da empresa\
4- A apuração retificada substitui a apuração legítima na base do sistema e do governo\
5- O fisco identifica a incoerência entre a nota fiscal emitida e a apuração retificada e abre processo de fiscalização

**Impacto esperado**: Autuação fiscal por fraude, cancelamento indevido de impostos e falta de rastreabilidade do responsável

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

---

### CA23 - Espionagem e Mapeamento da Agenda Fiscal de Empresas Clientes

**Ator**: Concorrente ou usuário autenticado sem acesso à empresa

**Objetivo**: Visualizar prazos, volumes de obrigações e pendências fiscais de empresas concorrentes

**Condições necessárias**:

- O sistema possui interface para consulta do calendário de obrigações e vencimentos 
- O endpoint de consulta do calendário não filtra adequadamente o escopo de empresas vinculadas ao usuário

**Fluxo de abuso**

1- O atacante acessa o calendário de obrigações no painel \
2- O atacante manipula os filtros da requisição para listar obrigações de CNPJs de terceiros\
3- O sistema retorna a lista completa de obrigações, prazos e impostos a vencer das outras empresas\
4- O atacante mapeia a saúde financeira e a rotina operacional do concorrente\
5- As informações extraídas são utilizadas para concorrência desleal ou chantagem

**Impacto esperado**: Vazamento de informações estratégicas e violação de confidencialidade fiscal

**Categorias STRIDE relacionadas**: Information Disclosure.

---

### CA24 - Adulteração da Tabela de Cálculo Salarial para Fraude em Benefícios

**Ator**: Contador mal-intencionado

**Objetivo**: Alterar as fórmulas de cálculo de encargos (INSS/FGTS) para inflar salários líquidos ou reduzir recolhimentos

**Condições necessárias**:

- O sistema realiza o cálculo automatizado de salários, descontos e encargos trabalhistas 
- Parâmetros e tabelas de alíquotas do cálculo podem ser modificados sem log imutável de alteração

**Fluxo de abuso**

1- O atacante acessa a tela de parâmetros de cálculo da folha \
2- O atacante altera a alíquota do INSS de um funcionário específico para 0% e aumenta o valor de horas extras\
3- O sistema executa a rotina de cálculo salarial utilizando as regras adulteradas\
4- O funcionário cumplicitado recebe um valor líquido maior enquanto a empresa recolhe menos encargos que o devido\
5- A fraude é descoberta posteriormente em auditoria trabalhista

**Impacto esperado**: Fraude em pagamentos de salários, passivos trabalhistas com o governo e perda de integridade dos cálculos

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA25 - Indisponibilidade e Alteração Massiva no Processamento da Folha de Pagamento

**Ator**: Atacante interno ou usuário autenticado

**Objetivo**: Adulterar a folha de pagamento de todos os funcionários e travar o processamento no dia de fechamento

**Condições necessárias**:

- O sistema realiza o processamento em lote da folha de pagamento mensal 
- Ausência de limite de execuções concorrentes e falta de controle de integridade dos dados processados

**Fluxo de abuso**

1- O atacante acessa o módulo de processamento da folha \
2- O atacante altera verbas de múltiplos funcionários e aciona repetidamente a rotina de processamento\
3- O servidor entra em sobrecarga ao tentar reprocessar a folha de pagamento de todas as empresas\
4- A base de dados grava valores salariais incorretos para os colaboradores\
5- A empresa fica impossibilitada de emitir e pagar a folha no prazo regulamentar

**Impacto esperado**: Pagamento incorreto de salários, atraso na folha de pagamento e indisponibilidade do sistema (DoS)

**Categorias STRIDE relacionadas**: Tampering, Repudiation, Information Disclosure e Denial of Service.

---

### CA26 - Exfiltração de Holerites e Salários de Terceiros via Parâmetro IDOR

**Ator**: Funcionário comum ou usuário sem privilégio

**Objetivo**: Acessar, visualizar e fazer o download de holerites e salários de qualquer colaborador da empresa

**Condições necessárias**:

- O sistema gera e permite a visualização/download de holerites individuais 
- A requisição para buscar o holerite utiliza o ID do funcionário (`employee_id`) sem validar se pertence ao usuário logado

**Fluxo de abuso**

1- O funcionário realiza o login e acessa a funcionalidade de visualização de holerite \
2- O funcionário altera o parâmetro `employee_id=50` para `employee_id=01` (ID da diretoria)\
3- O sistema não valida o privilégio do solicitante e retorna o documento do diretor\
4- O funcionário faz o download do holerite obtendo dados sobre o salário, CPF e descontos da diretoria\
5- O funcionário divulga os salários internamente

**Impacto esperado**: Vazamento grave de dados pessoais e financeiros (LGPD), quebra de confidencialidade e problemas de clima organizacional

**Categorias STRIDE relacionadas**: Information Disclosure e Elevation of Privilege.

---

### CA27 - Lançamento Fraudulento de Verbas Rescisórias Fictícias

**Ator**: Operador de RH ou contador malicioso

**Objetivo**: Simular o lançamento de férias ou verbas rescisórias para gerar pagamentos indevidos a favorecidos

**Condições necessárias**:

- O sistema permite o lançamento manual de eventos trabalhistas como férias, 13º e rescisões 
- Falha na exigência de anexação de avisos prévios ou documentos homologados para autorizar o lançamento

**Fluxo de abuso**

1- O atacante acessa a funcionalidade de lançamentos trabalhistas \
2- O atacante cadastra uma rescisão fictícia para um colaborador ativo com valores calculados em duplicidade\
3- O sistema registra o lançamento sem exigir aprovação superior ou conferência com a gestão de RH\
4- Os valores rescisórios são incluídos no lote de pagamento da empresa\
5- O valor é transferido e o atacante tenta apagar os registros do lançamento no sistema

**Impacto esperado**: Desvio de verbas trabalhistas da empresa, erros em rescisões e inconsistências perante os órgãos de controle

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

---

### CA28 - Transmissão de Eventos Trabalhistas Falsos e Falsificação de Certificado no eSocial

**Ator**: Atacante externo com credenciais de API ou usuário interno

**Objetivo**: Transmitir dados trabalhistas adulterados ao eSocial comprometendo a regularidade fiscal da empresa

**Condições necessárias**:

- O sistema realiza a transmissão automatizada de eventos (S-1000, S-1200, S-2200) ao eSocial 
- Armazenamento inseguro do certificado digital ou falta de verificação do remetente

**Fluxo de abuso**

1- O atacante obtém acesso ao módulo de transmissão do eSocial \
2- O atacante modifica a carga útil (payload) do evento trabalhista alterando dados de admissão ou salários\
3- O sistema assina o evento com o certificado digital da empresa e envia ao eSocial\
4- O governo aceita a transmissão e gera um recibo oficial com base nos dados adulterados\
5- A empresa passa a ter inconsistências trabalhistas na base do governo sem que a diretoria saiba

**Impacto esperado**: Aplicação de multas graves pelo Ministério do Trabalho, inconsistência no eSocial e comprometimento da identidade da empresa (Spoofing)

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Repudiation, Information Disclosure e Elevation of Privilege.

---

### CA29 - Emissão Fraudulenta de Notas Fiscais com Uso Indevido de Certificado Digital

**Ator**: Atacante com credenciais comprometidas ou usuário mal-intencionado

**Objetivo**: Emitir notas fiscais frias de alto valor utilizando a empresa da vítima para lavagem de dinheiro ou fraude fiscal

**Condições necessárias**:

- O sistema disponibiliza funcionalidade para emissão direta de NF-e e NFS-e 
- O certificado digital da empresa fica armazenado na plataforma sem exigência de PIN/reautenticação por emissão

**Fluxo de abuso**

1- O atacante acessa a conta do cliente no sistema de contabilidade \
2- O atacante navega até o módulo de emissão de notas fiscais\
3- O atacante insere dados de tomadores fictícios e valores milionários de prestação de serviço\
4- O sistema utiliza o certificado digital armazenado para assinar e emitir as notas fiscais na SEFAZ/Prefeitura\
5- O atacante utiliza as notas emitidas para comprovar faturamento falso em terceiros

**Impacto esperado**: Atribuição de impostos indevidos (ISS/PIS/COFINS) para a empresa vítima, bloqueio do certificado e penalidades criminais

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Repudiation e Elevation of Privilege.

---

### CA30 - Cancelamento Injustificado de Notas Fiscais e Sonegação de Faturamento

**Ator**: Usuário operacional mal-intencionado ou atacante invasor

**Objetivo**: Cancelar notas fiscais emitidas legitimamente para ocultar faturamento e sonegar impostos

**Condições necessárias**:

- O sistema permite o cancelamento e emissão de carta de correção de notas fiscais 
- Falha na restrição de privilégios para cancelamento de nota sem dupla aprovação

**Fluxo de abuso**

1- O atacante acessa o painel de notas fiscais emitidas \
2- O atacante seleciona notas fiscais de vendas concluídas e aciona o pedido de cancelamento\
3- O sistema envia a solicitação de cancelamento à SEFAZ sem exigir reautenticação ou justificativa auditada\
4- A SEFAZ homologa o cancelamento da nota fiscal\
5- A receita da empresa é ocultada no sistema contábil provocando divergência na apuração fiscal

**Impacto esperado**: Sonegação de impostos, incongruência fiscal junto à Receita e cancelamento indevido de vendas legítimas

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

---

### CA31 - Manipulação de Parâmetros de Relatórios e Negação de Serviço por Consultas Pesadas

**Ator**: Usuário mal-intencionado ou atacante externo

**Objetivo**: Gerar relatórios financeiros com dados manipulados ou derrubar o servidor enviando requisições complexas

**Condições necessárias**:

- O sistema disponibiliza a geração de demonstrações financeiras (DRE, Balancete, Balanço Patrimonial) 
- Permite alteração de filtros de consolidação e executa rotinas pesadas de agregação em tempo real

**Fluxo de abuso**

1- O atacante acessa o módulo de relatórios contábeis \
2- O atacante modifica os parâmetros da requisição para omitir contas de despesas ou injeta requisições com intervalos de anos\
3- O sistema tenta processar a consolidação massiva de dados sem limitar o tempo de execução (timeout)\
4- O banco de dados trava devido ao alto consumo de memória e CPU\
5- O relatório é gerado com dados distorcidos ou o sistema fica fora do ar para todos os contadores

**Impacto esperado**: Indisponibilidade da plataforma (DoS), distorção de relatórios gerenciais e acesso a relatórios sem a devida autorização

**Categorias STRIDE relacionadas**: Tampering, Information Disclosure, Denial of Service e Elevation of Privilege.

---

### CA32 - Exfiltração Massiva de Documentos Fiscais e Contábeis (PDF/XML)

**Ator**: Usuário com acesso ao painel ou atacante via IDOR

**Objetivo**: Baixar em lote todos os XMLs de notas e PDFs contábeis de empresas para comercializar ou espionar

**Condições necessárias**:

- O sistema permite a exportação de documentos em formatos PDF e XML 
- Ausência de mecanismo de controle de taxa de download (rate limit) e validação de tenant no download de arquivos

**Fluxo de abuso**

1- O atacante acessa a funcionalidade de exportação de documentos\
2- O atacante desenvolve um script para iterar sobre os links de download dos arquivos XML e PDF\
3- O sistema disponibiliza os arquivos sem registrar o log de quem realizou o download de cada documento\
4- O atacante baixa centenas de milhares de arquivos contendo dados fiscais, salários e segredos comerciais\
5- O atacante exfiltra o pacote completo de dados sem ser bloqueado

**Impacto esperado**: Vazamento massivo de dados sensíveis (LGPD), espionagem industrial e impossibilidade de rastrear quem vazou os documentos

**Categorias STRIDE relacionadas**: Repudiation, Information Disclosure e Elevation of Privilege.

---

### CA33 - Falsificação de Servidor Bancário e Injeção de Extratos Fictícios no Open Finance

**Ator**: Atacante Man-in-the-Middle ou servidor forjado

**Objetivo**: Injetar extratos bancários falsificados via Open Finance para forjar a saúde financeira da empresa

**Condições necessárias**:

- O sistema se conecta a APIs de instituições financeiras para importar extratos via Open Finance 
- Falha na validação rigorosa de certificados mTLS ou endpoints do provedor de Open Finance

**Fluxo de abuso**

1- O sistema aciona a rotina automatizada de busca de extratos bancários \
2- O atacante intercepta a conexão e se passa pela instituição bancária (Spoofing)\
3- O atacante envia uma resposta JSON contendo saldos e transações bancárias fictícias\
4- O sistema salva os extratos falsos e ajusta o saldo da empresa na plataforma\
5- A empresa aparenta possuir liquidez financeira irreal no sistema contábil

**Impacto esperado**: Falsificação de dados bancários, erro na conciliação, vazamento de tokens de acesso bancário e falhas na integração

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Information Disclosure e Denial of Service.

---

### CA34 - Injeção de Respostas Falsas na Consulta Cadastral da Receita Federal

**Ator**: Atacante em rede (MITM)

**Objetivo**: Alterar o status retornado pela Receita Federal para fazer uma empresa inapta parecer regularizada

**Condições necessárias**:

- O sistema realiza consultas automatizadas à API da Receita Federal para checar a situação do CNPJ
- Ausência de validação da assinatura digital das respostas da API externa

**Fluxo de abuso**

1- O sistema dispara a consulta periódica da situação cadastral da empresa \
2- O atacante intercepta o tráfego de rede entre o sistema contábil e o webservice da Receita Federal\
3- O atacante modifica a resposta alterando o status de "SUSPENSA/INAPTA" para "ATIVA"\
4- O sistema atualiza o cadastro da empresa liberando a emissão de notas fiscais e obrigações\
5- A empresa continua operando irregularmente no sistema sem ter sua pendência resolvida

**Impacto esperado**: Operação contábil de empresas irregulares, burla de verificações de conformidade e indisponibilidade do serviço se a API for inundada

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Information Disclosure e Denial of Service.

---

### CA35 - Interceptação e Adulteração de NFS-e na Transmissão para a Prefeitura

**Ator**: Atacante em rede ou usuário interno

**Objetivo**: Modificar os dados da nota fiscal de serviço no momento do envio à prefeitura para sonegar imposto municipal (ISS)

**Condições necessárias**:

- O sistema possui integração de envio de NFS-e para os webservices das prefeituras 
- Falha na criptografia de ponta a ponta ou validação do canal de transmissão

**Fluxo de abuso**

1- O usuário solicita o envio da NFS-e para a prefeitura \
2- O atacante intercepta a mensagem SOAP/REST enviada ao servidor municipal\
3- O atacante altera o valor da nota fiscal de serviço reduzindo a base de cálculo do ISS\
4- A prefeitura recebe o documento com o valor menor e gera o cupom de tributação reduzido\
5- O sistema contábil grava o valor original gerando inconsistência entre o sistema e a prefeitura

**Impacto esperado**: Sonegação de tributos municipais, rejeição da transmissão e acúmulo de notas na fila de envio

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Repudiation, Information Disclosure e Denial of Service.

---

### CA36 - Injeção de Dados Maliciosos e Roubo de Sessão na Sincronização com ERP

**Ator**: Atacante com acesso ao ERP do cliente ou atacante em rede

**Objetivo**: Injetar registros contábeis adulterados através da sincronização de APIs entre o ERP e o sistema contábil

**Condições necessárias**:

- O sistema oferece integração bidirecional via API com ERPs de terceiros
- Autenticação por token estático sem rotação frequente entre os sistemas

**Fluxo de abuso**

1- O atacante obtém o token de API de integração do ERP do cliente \
2- O atacante envia payloads maliciosos simulando uma sincronização legítima de vendas e estoque\
3- O sistema contábil aceita a carga de dados sem validar a assinatura ou o limite de registros\
4- Lançamentos fictícios são criados na contabilidade alterando o resultado fiscal\
5- O volume de dados enviados trava o serviço de sincronização para outros clientes

**Impacto esperado**: Corrupção dos dados contábeis, vazamento de dados de integração e indisponibilidade da API de sync

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Information Disclosure e Denial of Service.

---

### CA37 - Sequestro e Vazamento de Credenciais de API de Integração

**Ator**: Usuário com permissão mal configurada ou atacante interno

**Objetivo**: Roubar segredos e tokens de API de bancos, prefeituras e Receita Federal salvos na plataforma

**Condições necessárias**:

- O sistema permite que o administrador configure e renove credenciais de API 
- Chaves de API e segredos são armazenados sem criptografia irreversível ou exibidos em texto claro na interface

**Fluxo de abuso**

1- O atacante navega até a tela de configuração de integrações e APIs \
2- O atacante visualiza em texto claro os segredos e tokens de acesso aos bancos e prefeituras\
3- O atacante altera a URL de callback da API para apontar para um servidor sob seu controle\
4- As requisições de autorização passam a enviar tokens de acesso diretamente ao atacante\
5- O atacante utiliza os tokens roubados para acessar diretamente as APIs bancárias e fiscais do cliente

**Impacto esperado**: Comprometimento de integrações externas, vazamento de segredos críticos de autenticação e escalada de privilégios

**Categorias STRIDE relacionadas**: Tampering, Repudiation, Information Disclosure e Elevation of Privilege.

---

### CA38 - Adulteração da Tabela de Logs de Alteração de Lançamentos

**Ator**: Usuário com privilégio de banco de dados ou administrador mal-intencionado

**Objetivo**: Modificar os registros de histórico de alterações para ocultar quem modificou valores contábeis

**Condições necessárias**:

- O sistema possui rotina para registrar a autoria, data e valor anterior de qualquer alteração 
- Os logs de alteração são armazenados na mesma base de dados operacional sem proteção contra escrita do admin

**Fluxo de abuso**

1- O atacante realiza uma alteração fraudulenta em um lançamento contábil\
2- O sistema grava a entrada no log de auditoria associando o usuário do atacante \
3- O atacante aciona comandos na aplicação ou base de dados para alterar o registro de log\
4- O atacante substitui seu ID de usuário pelo ID de outro funcionário no log de alterações\
5- Ao ser auditado, o sistema indica que outro usuário realizou a fraude

**Impacto esperado**: Destruição do não-repúdio, incriminação indevida de usuários inocentes e falsificação de registros

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA39 - Burlar Filtros de Auditoria e Exfiltração da Trilha de Logs por IDOR

**Ator**: Usuário comum ou auditor de empresa concorrente

**Objetivo**: Mapear todas as ações realizadas pelos usuários de outras empresas ou ocultar eventos na consulta de auditoria

**Condições necessárias**:

- O sistema possui interface para consulta da trilha de auditoria por período e usuário 
- A consulta não valida se o auditor possui permissão sobre a empresa pesquisada

**Fluxo de abuso**

1- O atacante acessa a consulta de trilha de auditoria \
2- O atacante altera o parâmetro da requisição inserindo o identificador de outra empresa ou usuário\
3- O sistema executa a busca e retorna todo o histórico de ações, acessos e alterações da outra empresa\
4- O atacante visualiza quem fez alterações, quando foram feitas e os valores anteriores\
5- O atacante utiliza essas informações para descobrir fragilidades operacionais do cliente

**Impacto esperado**: Vazamento de informações estratégicas de auditoria e escalada de privilégios de consulta

**Categorias STRIDE relacionadas**: Information Disclosure e Elevation of Privilege.

---

### CA40 - Injeção de Logs Falsos (Log Injection) e Ocultação de Acessos Sensíveis

**Ator**: Atacante externo ou usuário interno

**Objetivo**: Injetar caracteres de quebra de linha ou logs falsos para cegar a equipe de segurança durante uma invasão

**Condições necessárias**:

- O sistema registra automaticamente todos os logins e acessos a dados sensíveis 
- Falha na sanitização dos dados informados pelo usuário no momento da escrita do log (ex.: parâmetro `User-Agent` ou `Username`)

**Fluxo de abuso**

1- O atacante realiza login informando um nome de usuário contendo quebras de linha e texto formatado de log fictício (`\n[INFO] Login bem sucedido - Admin`)\
2- O sistema grava o log sem sanitizar a entrada \
3- A trilha de auditoria fica corrompida exibindo entradas falsas de ações que jamais ocorreram\
4- O atacante executa acessos indevidos a dados sensíveis enquanto a equipe analisa os logs falsificados\
5- A análise de incidentes fica inviabilizada

**Impacto esperado**: Corrupção da trilha de auditoria de acessos, perda da capacidade de rastreamento de acessos indevidos

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA41 - Exfiltração e Adulteração de Arquivos de Logs Exportados

**Ator**: Administrador mal-intencionado ou atacante com sessão de admin

**Objetivo**: Exportar o pacote completo de logs para fora do sistema e alterar o arquivo baixado antes de entregar aos auditores

**Condições necessárias**:

- O sistema disponibiliza funcionalidade de exportação de logs em massa para compliance 
- O arquivo exportado não possui assinatura digital nem hash de integridade verificado

**Fluxo de abuso**

1- O atacante acessa a função de exportação de logs de compliance \
2- O atacante gera e faz o download do arquivo compactado contendo todos os logs da plataforma\
3- O atacante abre o arquivo e remove as linhas contendo as evidências de suas ações fraudulentas\
4- O atacante entrega o arquivo alterado para os auditores externos alegando ser o log oficial do sistema\
5- Os auditores analisam uma base de logs adulterada e não identificam a fraude

**Impacto esperado**: Quebra da conformidade legal/regulatória, vazamento de metadados operacionais e fraude em auditorias externas

**Categorias STRIDE relacionadas**: Tampering, Repudiation, Information Disclosure e Elevation of Privilege.

---

### CA42 - Adulteração da Linha Digitável de Boletos de Honorários

**Ator**: Atacante externo ou funcionário mal-intencionado

**Objetivo**: Alterar os dados de conta e favorecido dos boletos de honorários para desviar a receita do escritório contábil

**Condições necessárias**:

- O sistema gera boletos bancários para cobrança de honorários dos clientes 
- Falha no controle de integridade dos parâmetros de geração de boleto enviados no front-end

**Fluxo de abuso**

1- O contador aciona a emissão de boletos de honorários para a carteira de clientes \
2- O atacante intercepta a requisição de emissão do boleto\
3- O atacante substitui o código da carteira bancária e a conta corrente pelos dados de sua conta pessoal\
4- O sistema gera os boletos contendo a linha digitável alterada e envia aos clientes\
5- Os clientes pagam os boletos e o dinheiro é creditado na conta do atacante

**Impacto esperado**: Perda financeira para o escritório contábil, cobranças indevidas geradas a clientes e exposição de dados de cobrança

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA43 - Baixa Fraudulenta de Boletos para Ocultação de Inadimplência

**Ator**: Operador financeiro mal-intencionado

**Objetivo**: Marcar boletos de honorários como "Pagos" sem que o dinheiro tenha entrado na conta bancária do escritório

**Condições necessárias**:

- O sistema realiza a conciliação e baixa automática ou manual dos boletos recebidos 
- O sistema permite a baixa manual de boletos sem validação do arquivo de retorno bancário (CNAB)

**Fluxo de abuso**

1- O atacante acessa a tela de conciliação de pagamentos recebidos\
2- O atacante seleciona boletos pendentes de clientes parceiros e força a baixa manual marcando-os como "Concluídos"\
3- O sistema atualiza o status dos boletos sem verificar o arquivo de retorno bancário correspondente\
4- O cliente deixa de ser cobrado e o sistema contábil registra o ingresso do recurso que jamais ocorreu\
5- O saldo de contas a receber fica adulterado

**Impacto esperado**: Prejuízo financeiro, falsificação do fluxo de caixa e acobertamento de inadimplência

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Information Disclosure.

---

### CA44 - Falsificação de Autorização e Desvio em Pagamento de Guias Fiscais

**Ator**: Atacante com conta comprometida ou usuário mal-intencionado

**Objetivo**: Alterar o valor e a conta de destino de um agendamento de pagamento de guias para desviar fundos da conta da empresa

**Condições necessárias**:

- O sistema permite o agendamento e autorização de pagamentos de guias tributárias diretamente via conta bancária vinculada 
- Ausência de segundo fator de autenticação (MFA) para autorização final do pagamento

**Fluxo de abuso**

1- O usuário agenda o pagamento de uma guia tributária no sistema \
2- O atacante intercepta a ordem de autorização do pagamento\
3- O atacante altera a chave Pix/conta de destino ou o valor do agendamento\
4- O sistema envia a ordem de pagamento adulterada para o banco sem exigir aprovação dupla do gestor\
5- O banco executa a transferência transferindo os recursos do cliente para o atacante

**Impacto esperado**: Perda financeira direta de alto valor, não quitação dos impostos da empresa e abuso de privilégios de pagamento

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Repudiation, Information Disclosure e Elevation of Privilege.

---

### CA45 - Envios de Notificações Falsas de Cobrança (Phishing) se Passando pelo Sistema

**Ator**: Atacante externo

**Objetivo**: Disparar e-mails e notificações falsas de cobrança de boletos vencidos contendo links maliciosos e boletos adulterados

**Condições necessárias**:

- O sistema possui módulo de notificação automática de boletos vencidos e baixados via e-mail/SMS 
- Falha na validação de remetente (SPF/DKIM/DMARC) ou exposição da fila de notificações

**Fluxo de abuso**

1- O atacante identifica a rota ou estrutura do template de notificação de cobrança do sistema\
2- O atacante gera mensagens de notificação falsas informando que o cliente possui um boleto vencido\
3- O atacante anexa um boleto falso com seus dados bancários ou insere um link de phishing no e-mail\
4- A mensagem é enviada para os clientes da empresa contábil\
5- Os clientes acreditam ser um aviso real do sistema de contabilidade e efetuam o pagamento no boleto fraudulento

**Impacto esperado**: Dano à reputação da empresa de contabilidade, prejuízo financeiro para os clientes e exposição de dados de cobrança

**Categorias STRIDE relacionadas**: Spoofing, Tampering e Information Disclosure.