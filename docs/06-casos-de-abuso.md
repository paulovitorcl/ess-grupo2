# 6. Casos de abuso

### CA01 - Credential Stuffing e Ataque de Força Bruta para Invasão de Conta Contábil

**Ator:** Atacante externo

**Objetivo:** Invadir contas de contadores ou clientes para acessar dados financeiros ou realizar operações não autorizadas.

**Ponto de interação:** P1 - Tela/API de login e MFA

**Condições necessárias:**

- O sistema disponibiliza interface de autenticação por e-mail e senha sem limite adequado de tentativas de login ou CAPTCHA.
- O atacante possui listas de credenciais vazadas em outros serviços ou utiliza tentativas automatizadas de força bruta.

**Fluxo de abuso:**

1. O atacante automatiza tentativas de autenticação contra a tela de login. 
2. O sistema processa múltiplas tentativas sem aplicar mecanismos adequados de limitação ou bloqueio.
3. O atacante identifica um par de e-mail e senha válido e obtém uma sessão autenticada.
4. O atacante acessa o painel da empresa associada à conta comprometida.
5. O usuário legítimo passa a ter sua conta acessada sem consentimento.

**Impacto esperado:** Acesso não autorizado a dados contábeis e financeiros, representação fraudulenta do usuário e violação de confidencialidade.

**Categoria STRIDE principal:** **Spoofing**

**Categorias STRIDE secundárias:**

- **Information Disclosure:** a conta comprometida pode permitir acesso a informações financeiras e contábeis.
- **Elevation of Privilege:** caso a conta comprometida possua permissões superiores às necessárias para o atacante.
- **Denial of Service:** pode ocorrer caso o mecanismo de bloqueio de contas seja explorado para impedir o acesso dos usuários legítimos.

---

### CA02 - Sequestro de Conta via Manipulação do Token de Recuperação de Senha

**Ator:** Atacante externo

**Objetivo:** Alterar a senha de um cliente ou administrador para assumir o controle da conta.

**Ponto de interação:** P2 - Recuperação de senha

**Condições necessárias:**

- O sistema disponibiliza funcionalidade de recuperação de senha por link ou token.
- O fluxo de recuperação apresenta identificadores previsíveis, como `user_id`, ou validação insuficiente do token.
- O sistema não vincula adequadamente o token à identidade e ao contexto da solicitação original.

**Fluxo de abuso:**

1. O atacante solicita a redefinição de senha informando o e-mail da vítima.
2. O atacante manipula os parâmetros da requisição de recuperação para tentar associá-la à conta alvo.
3. O sistema gera ou aceita um token de redefinição sem validar adequadamente a identidade do solicitante.
4. O atacante define uma nova senha para a conta da vítima sem possuir autorização legítima.
5. O atacante realiza login com a nova senha e assume o controle da conta.

**Impacto esperado:** Perda de controle da conta do cliente ou administrador, acesso não autorizado a informações e possibilidade de utilização da conta para novas ações fraudulentas.

**Categoria STRIDE principal:** **Spoofing**

**Categorias STRIDE secundárias:**

- **Tampering:** manipulação dos parâmetros ou do contexto da solicitação de recuperação.
- **Information Disclosure:** acesso aos dados disponíveis na conta comprometida.
- **Elevation of Privilege:** caso a conta comprometida possua privilégios administrativos ou superiores aos do atacante.

---

### CA03 - Criação Fraudulenta de Contas Privilegiadas sem Rastro de Auditoria

**Ator:** Usuário mal-intencionado ou conta administrativa comprometida

**Objetivo:** Criar contas com permissões administrativas para manter acesso persistente ou desativar contas de administradores e auditores legítimos.

**Ponto de interação:** P3 - Gestão de contas e perfis (RBAC)

**Condições necessárias:**

- O sistema possui interface para gerenciamento, criação e desativação de contas.
- O endpoint de gerenciamento não realiza checagem estrita de autorização.
- O sistema não exige aprovação adicional ou reautenticação para operações administrativas críticas.
- Há falhas na gravação ou proteção dos registros de auditoria.

**Fluxo de abuso:**

1. O atacante acessa a funcionalidade de gerenciamento de usuários.
2. O atacante envia uma requisição para criar uma nova conta atribuindo perfil administrativo.
3. O sistema cria a conta sem exigir autorização adicional ou aprovação de outro administrador.
4. O atacante desativa contas de administradores ou auditores legítimos para dificultar a revogação de seu acesso.
5. O atacante passa a operar no sistema com privilégios elevados.

**Impacto esperado:** Persistência de acessos não autorizados, comprometimento da administração do sistema e bloqueio de usuários legítimos.

**Categoria STRIDE principal:** **Tampering** e **Elevation of Privilege**

**Categorias STRIDE secundárias:**

- **Repudiation:** ausência ou insuficiência de registros confiáveis que permitam identificar a autoria das ações.
- **Denial of Service:** desativação de contas legítimas pode impedir o acesso de administradores e auditores.

---

### CA04 - Escalada de Privilégios por Manipulação de Matriz de Permissões (RBAC)

**Ator:** Usuário operacional mal-intencionado

**Objetivo:** Alterar a atribuição de papéis e permissões para conceder a si próprio privilégios administrativos ou de gestão financeira.

**Ponto de interação:** P3 - Gestão de contas e perfis (RBAC)

**Condições necessárias:**

- O sistema utiliza controle de acesso baseado em papéis (RBAC).
- As requisições de alteração de permissões não validam adequadamente se o solicitante possui autorização administrativa.
- O backend confia indevidamente nos parâmetros de papel ou permissão enviados pelo cliente.

**Fluxo de abuso:**

1. O atacante com perfil comum envia uma requisição de atualização de seu perfil.
2. O atacante adiciona parâmetros de permissões administrativas, como `role=admin` ou `permissions=all`.
3. O sistema processa e grava a alteração sem validar se o solicitante possui autorização para modificar seu próprio papel.
4. O atacante passa a possuir permissões administrativas.
5. O atacante acessa módulos restritos, como escrituração, relatórios, folha e pagamentos.

**Impacto esperado:** Quebra da política de segurança RBAC, acesso irrestrito a dados sensíveis e execução de ações não autorizadas.

**Categoria STRIDE principal:** **Tampering** e **Elevation of Privilege**

**Categorias STRIDE secundárias:**

- **Repudiation:** ausência de registros confiáveis pode dificultar a identificação do responsável pela alteração.
- **Information Disclosure:** os privilégios obtidos permitem acessar escrituração, relatórios, folhas de pagamentos e outros dados restritos.

---

### CA05 - Desvio de Pagamentos por Troca de Dados Bancários Cadastrais

**Ator:** Atacante interno ou invasor de conta

**Objetivo:** Substituir a conta bancária ou chave Pix de um cliente ou fornecedor para desviar transferências financeiras.

**Ponto de interação:** P4 - Cadastros e dados bancários; P10 - Pagamentos

**Condições necessárias:**

- O sistema permite o cadastro e atualização de dados bancários.
- O sistema não exige MFA ou confirmação adicional para alterações sensíveis.
- Os registros de auditoria não são suficientemente detalhados ou protegidos.

**Fluxo de abuso:**

1. O atacante acessa a funcionalidade de atualização de dados bancários.
2. O atacante insere os dados de sua própria conta bancária ou chave Pix no cadastro da vítima.
3. O sistema salva os novos dados sem exigir confirmação adicional.
4. As rotinas de pagamento utilizam os dados bancários adulterados.
5. O pagamento de guias, reembolsos ou fornecedores é direcionado à conta controlada pelo atacante.

**Impacto esperado:** Prejuízo financeiro direto, fraude em pagamentos e alteração não autorizada de dados bancários.

**Categoria STRIDE principal:** **Tampering**

**Categorias STRIDE secundárias:**

- **Repudiation:** ausência de trilha de auditoria confiável pode dificultar a identificação do responsável.
- **Information Disclosure:** os dados bancários envolvidos na operação podem ser expostos indevidamente.

---

### CA06 - Estorno Indevido de Lançamentos para Alteração de Resultados Fiscais

**Ator:** Usuário com perfil operacional contábil

**Objetivo:** Estornar receitas legítimas já contabilizadas para alterar artificialmente os resultados contábeis e fiscais.

**Ponto de interação:** P5 - Escrituração

**Condições necessárias:**

- O sistema permite o estorno e ajuste de lançamentos contábeis previamente realizados.
- Não existe controle de permissão suficientemente restritivo para estornos relevantes.
- O sistema não exige justificativa ou aprovação para operações críticas.
- O histórico do valor original não é protegido adequadamente.

**Fluxo de abuso:**

1. O atacante acessa a lista de lançamentos contábeis da empresa.
2. O atacante seleciona lançamentos de receita e solicita o estorno.
3. O sistema executa o estorno sem exigir justificativa ou aprovação adequada.
4. A alteração modifica os valores utilizados nos processos contábeis e fiscais.
5. O atacante tenta negar a autoria caso seja questionado sobre a alteração.

**Impacto esperado:** Distorção de balancetes e resultados fiscais, inconsistências contábeis e quebra da integridade do histórico contábil.

**Categoria STRIDE principal:** **Tampering**

**Categorias STRIDE secundárias:**

- **Repudiation:** ausência de evidências confiáveis pode dificultar a comprovação da autoria.
- **Elevation of Privilege:** caso o usuário consiga executar estornos que deveriam exigir privilégios superiores.

---

### CA07 - Indisponibilidade e Alteração Massiva no Processamento da Folha de Pagamento

**Ator:** Atacante interno ou usuário autenticado comprometido

**Objetivo:** Adulterar a folha de pagamento e provocar indisponibilidade durante o período de fechamento.

**Ponto de interação:** P7 - Folha de pagamento e holerites

**Condições necessárias:**

- O sistema realiza processamento em lote da folha de pagamento.
- Não existe limite adequado para execuções concorrentes.
- Não existem mecanismos suficientes de controle de integridade dos dados processados.
- A operação não possui controles adequados para detectar reprocessamentos anormais.

**Fluxo de abuso:**

1. O atacante acessa o módulo de processamento da folha.
2. O atacante altera dados de múltiplos funcionários e inicia repetidamente o processamento.
3. O sistema processa as solicitações sem controles suficientes de concorrência.
4. O servidor e os recursos de banco de dados entram em sobrecarga.
5. A base de dados pode registrar valores salariais incorretos.
6. A empresa fica impossibilitada de concluir o processamento da folha no prazo esperado.

**Impacto esperado:** Pagamento incorreto de salários, atraso no processamento da folha, corrupção de dados e indisponibilidade do sistema.

**Categoria STRIDE principal:** **Tampering** e **Denial of Service**

**Categorias STRIDE secundárias:**

---

### CA08 - Exfiltração de Holerites e Salários de Terceiros via Parâmetro IDOR

**Ator:** Funcionário comum ou usuário sem privilégio suficiente

**Objetivo:** Acessar, visualizar e realizar o download de holerites e informações salariais de outros colaboradores.

**Ponto de interação:** P7 - Folha de pagamento e holerites

**Condições necessárias:**

- O sistema permite a visualização ou download de holerites individuais.
- A requisição utiliza um identificador como `employee_id`.
- O backend não valida corretamente se o funcionário autenticado possui autorização para acessar o recurso solicitado.

**Fluxo de abuso:**

1. O funcionário realiza login e acessa a funcionalidade de visualização de holerite.
2. O funcionário modifica o identificador do recurso solicitado.
3. O sistema não verifica corretamente a relação entre o usuário autenticado e o funcionário identificado na requisição.
4. O sistema retorna o holerite de outro colaborador.
5. O funcionário obtém informações como salário, CPF e descontos do terceiro.

**Impacto esperado:** Vazamento de dados pessoais e financeiros, quebra de confidencialidade e acesso indevido a informações trabalhistas.

**Categoria STRIDE principal:** **Information Disclosure**

**Categorias STRIDE secundárias:**

- **Elevation of Privilege:** o usuário obtém acesso a recursos fora de seu escopo autorizado.

---

### CA09 - Exfiltração Massiva de Documentos Fiscais e Contábeis (PDF/XML)

**Ator:** Usuário autenticado ou atacante explorando falhas de controle de acesso

**Objetivo:** Baixar em grande escala documentos fiscais e contábeis de empresas sem autorização.

**Ponto de interação:** P8 - Emissão e exportação de documentos

**Condições necessárias:**

- O sistema permite a exportação de documentos em PDF e XML.
- Não existe mecanismo adequado de controle de taxa de download.
- O sistema não valida corretamente o tenant ou empresa associada ao documento.
- O sistema não registra de maneira suficiente os downloads realizados.

**Fluxo de abuso:**

1. O atacante acessa a funcionalidade de exportação de documentos.
2. O atacante automatiza solicitações para diferentes documentos.
3. O sistema disponibiliza os arquivos sem aplicar controles adequados de autorização e volume.
4. O atacante baixa grande quantidade de arquivos contendo informações fiscais, contábeis e comerciais.
5. Os documentos são armazenados externamente e podem ser utilizados ou divulgados sem autorização.

**Impacto esperado:** Vazamento massivo de informações fiscais e contábeis, exposição de dados sensíveis e perda de rastreabilidade dos acessos.

**Categoria STRIDE principal:** **Information Disclosure**

**Categorias STRIDE secundárias:**

- **Elevation of Privilege:** exploração de falhas de autorização pode permitir acesso a documentos fora do escopo do usuário.
- **Repudiation:** ausência de registros detalhados dificulta a identificação do responsável pelo download.
- **Denial of Service:** downloads automatizados em grande escala podem consumir recursos do sistema.

---

### CA10 - Adulteração da Tabela de Logs de Alteração de Lançamentos

**Ator:** Usuário com privilégio de banco de dados ou administrador mal-intencionado

**Objetivo:** Modificar registros de histórico para ocultar a autoria de alterações contábeis.

**Ponto de interação:** P11 - Auditoria e logs

**Condições necessárias:**

- O sistema registra autoria, data e valores anteriores das alterações.
- Os logs são armazenados na mesma base de dados operacional.
- Usuários administrativos possuem acesso de escrita aos registros de auditoria.
- Não existe mecanismo externo ou imutável para proteção da trilha de auditoria.

**Fluxo de abuso:**

1. O atacante realiza uma alteração fraudulenta em um lançamento contábil.
2. O sistema registra a alteração no log de auditoria.
3. O atacante acessa os registros de auditoria por meio da aplicação ou diretamente na base de dados.
4. O atacante modifica o registro para substituir sua identificação pela de outro usuário.
5. Durante uma auditoria, o sistema apresenta informações de autoria adulteradas.

**Impacto esperado:** Comprometimento da integridade da trilha de auditoria, atribuição incorreta de autoria e perda da confiabilidade dos registros.

**Categoria STRIDE principal:** **Tampering** e **Repudiation**

**Categorias STRIDE secundárias:** 

---

### CA11 - Manipulação de Dados para Geração de Obrigações Fiscais

**Ator:** Usuário operacional mal-intencionado ou conta comprometida

**Objetivo:** Alterar dados utilizados na apuração fiscal para gerar obrigações fiscais incorretas.

**Ponto de interação:** P6 - Apuração fiscal e geração de SPED/guias

**Condições necessárias:**

- O sistema utiliza dados contábeis e fiscais para calcular obrigações.
- O usuário possui acesso aos dados utilizados pela apuração.
- Não existem controles suficientes de segregação de funções ou aprovação das alterações relevantes.

**Fluxo de abuso:**

1. O atacante acessa dados utilizados na apuração fiscal.
2. O atacante altera informações que influenciam os cálculos fiscais.
3. O sistema utiliza os dados adulterados durante a apuração.
4. O sistema gera SPED, guias ou outros documentos fiscais com informações incorretas.
5. Os documentos gerados são utilizados no cumprimento das obrigações fiscais.

**Impacto esperado:** Inconsistências fiscais, distorção de valores apurados, possíveis multas e prejuízos financeiros.

**Categoria STRIDE principal:** **Tampering**

**Categorias STRIDE secundárias:**

- **Repudiation:** ausência de histórico confiável pode dificultar a identificação das alterações.
- **Elevation of Privilege:** caso o usuário consiga modificar dados que deveriam ser restritos a funções administrativas ou de supervisão.

---

### CA12 - Manipulação de Dados por API de Integração Externa

**Ator:** Atacante externo, sistema externo comprometido ou terceiro com credencial de integração comprometida

**Objetivo:** Utilizar uma integração legítima para inserir ou modificar dados contábeis, fiscais ou financeiros de forma não autorizada.

**Ponto de interação:** P9 - APIs de integração externa

**Condições necessárias:**

- O sistema disponibiliza APIs para integração com bancos, Receita Federal, prefeituras, eSocial ou ERP dos clientes.
- As integrações utilizam credenciais, tokens ou certificados digitais.
- Os mecanismos de autenticação, autorização, escopo ou validação de origem são insuficientes.
- O sistema não valida adequadamente a integridade e consistência dos dados recebidos.

**Fluxo de abuso:**

1. O atacante obtém ou utiliza indevidamente uma credencial de integração.
2. O atacante envia requisições para a API utilizando a identidade da integração comprometida.
3. O sistema aceita as requisições como provenientes de uma integração autorizada.
4. Dados contábeis, fiscais ou financeiros são inseridos ou modificados.
5. Os dados adulterados passam a ser utilizados pelos módulos internos do sistema.

**Impacto esperado:** Corrupção de dados, fraude, inconsistências contábeis e fiscais e comprometimento de processos dependentes da integração.

**Categoria STRIDE principal:** **Spoofing** e **Tampering**

**Categorias STRIDE secundárias:**

- **Repudiation:** dificuldade de diferenciar o usuário legítimo da integração comprometida sem registros adequados.
- **Elevation of Privilege:** utilização de uma credencial de integração para acessar operações além do escopo originalmente autorizado.
- **Information Disclosure:** exposição de dados durante o uso indevido da integração.

---

### CA13 - Autorização Indevida de Pagamento

**Ator:** Atacante interno ou usuário autenticado com conta comprometida

**Objetivo:** Criar, alterar ou autorizar pagamentos sem autorização do responsável financeiro.

**Ponto de interação:** P10 - Pagamentos

**Condições necessárias:**

- O sistema permite criação e/ou autorização de pagamentos.
- Não existe segregação adequada entre criação e aprovação.
- Não existe MFA ou autenticação adicional para operações financeiras críticas.
- Não há limite ou aprovação adicional para transações de alto valor.

**Fluxo de abuso:**

1. O atacante acessa o módulo de pagamentos.
2. O atacante cria ou seleciona uma operação de pagamento.
3. O sistema permite que o próprio atacante autorize a operação sem uma segunda validação.
4. A operação é encaminhada para execução.
5. O valor é transferido para o destinatário informado.

**Impacto esperado:** Prejuízo financeiro direto, realização de pagamentos não autorizados e comprometimento do processo financeiro.

**Categoria STRIDE principal:** **Tampering** e **Elevation of Privilege**

**Categorias STRIDE secundárias:**

- **Spoofing:** utilização de uma conta legítima comprometida para representar um usuário autorizado.
- **Repudiation:** ausência de trilha de auditoria adequada pode dificultar a identificação da autoria da autorização.