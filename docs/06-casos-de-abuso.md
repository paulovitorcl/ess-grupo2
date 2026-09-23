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

**Categorias STRIDE relacionadas**: Spoofing, Tampering, Information Disclosure e Elevation of Privilege.

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

### CA06 - Escalada de Privilégios por Manipulação de Matriz de Permissões (RBAC)

**Ator**: Usuário operacional mal-intencionado

**Objetivo**: Alterar a atribuição de papéis e permissões para conceder a si próprio privilégios de gestão financeira

**Condições necessárias**:

- O sistema utiliza controle de acesso baseado em papéis (RBAC) para restringir funcionalidades 
- As requisições de alteração de permissão não validam adequadamente se o solicitante possui papel de administrador

**Fluxo de abuso**

1- O atacante com perfil comum intercepta a requisição de atualização do seu perfil de usuário \
2- O atacante adiciona parâmetros de permissões administrativas (ex.: `role=admin` ou `permissions=all`), adulterando a estrutura lógica de controle \
3- O sistema processa e grava a alteração na base de dados sem validar se o autor possui privilégios para isso, aplicando os novos papéis \
4- O sistema não registra logs de auditoria seguros com detalhes de IP e identificação de autoria, ou o atacante consegue apagar os vestígios da alteração \
5- O atacante passa a acessar módulos restritos, como escrituração, relatórios e pagamentos, e pode negar posteriormente que adulterou o sistema por falta de provas de autoria

**Impacto esperado**: Quebra da política de segurança RBAC, acesso irrestrito a dados sensíveis e execução de ações não autorizadas

**Categorias STRIDE relacionadas**: Tampering, Repudiation e Elevation of Privilege.

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
3- O sistema salva a nova conta bancária sem exigir aprovação por um segundo usuário e sem registrar logs de auditoria detalhados e imutáveis da sessão de alteração\
4- As rotinas automatizadas de pagamento utilizam os novos dados bancários adulterados\
5- O pagamento de guias, reembolsos ou fornecedores é transferido para a conta do atacante

**Impacto esperado**: Prejuízo financeiro direto, fraude em pagamentos e vazamento de dados bancários

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
3- O sistema registra a ação de forma genérica ou sem logs de auditoria seguros/imutáveis\
4- O servidor entra em sobrecarga ao tentar reprocessar a folha de pagamento de todas as empresas\
5- A base de dados grava valores salariais incorretos para os colaboradores\
6- A empresa fica impossibilitada de emitir e pagar a folha no prazo regulamentar

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
