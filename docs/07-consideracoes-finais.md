# 7. Considerações finais

A modelagem de ameaças do Sistema de Contabilidade permitiu relacionar suas
funcionalidades, perfis de usuários e integrações externas a cenários que
podem comprometer a segurança das operações. A organização em seis categorias
STRIDE ajudou a analisar tanto o acesso ao sistema quanto o tratamento dos
dados contábeis, fiscais, financeiros e trabalhistas ao longo dos fluxos
descritos na arquitetura.

A análise identificou consequências relevantes nas seis categorias. A
falsificação de identidade pode permitir operações em nome de usuários ou
empresas, enquanto a adulteração pode comprometer lançamentos, documentos e
pagamentos. O repúdio dificulta a investigação e a atribuição de ações, e a
divulgação de informações expõe dados pessoais e empresariais. A negação de
serviço prejudica atividades com prazo, como o fechamento contábil e a folha.
A elevação de privilégio pode permitir acesso a funções restritas e a dados
de outras empresas atendidas.

Os casos de abuso ilustram caminhos pelos quais essas ameaças podem se
manifestar. Cenários como sequestro de conta, alteração de permissões,
troca de dados bancários e adulteração de logs mostram que uma mesma sequência
de ações pode envolver mais de uma categoria STRIDE. Assim, os controles
precisam atuar de forma complementar: MFA e recuperação segura de contas,
autorização no servidor, validação de dados, proteção de credenciais,
aprovação vinculada ao conteúdo da operação, auditoria protegida e limites
de processamento.

Como prioridade inicial, propõe-se tratar os cenários capazes de permitir
sequestro de contas, acesso entre empresas, alteração de valores e pagamentos
indevidos, juntamente com a proteção das evidências necessárias à sua
investigação. Essa priorização é qualitativa e deverá considerar a exposição
real do sistema e os controles existentes quando houver uma implementação.
Os critérios de verificação registrados na [modelagem STRIDE](./05-modelagem-ameacas-stride.md)
constituem uma base para transformar as recomendações em testes de aceitação.

O trabalho tem como limitação seu caráter documental e conceitual. Não foram
realizados testes em uma aplicação nem verificada a eficácia dos controles
propostos. Portanto, as ameaças descritas representam possibilidades
condicionadas às premissas de cada cenário, e não falhas comprovadas. A
priorização ainda não considera probabilidades estimadas, e algumas relações
entre ameaças e casos de abuso precisam de alinhamento das premissas, como a
obtenção do token no cenário de recuperação de senha. A análise não é
exaustiva e deverá ser refinada conforme o projeto evoluir.

Como continuidade, recomenda-se revisar o modelo a cada mudança relevante de
arquitetura, integração ou regra de negócio, detalhar as fronteiras de
confiança e validar os controles por meio de testes orientados aos casos de
abuso. A contribuição deste trabalho é fornecer uma base organizada para
discutir riscos e incorporar requisitos de segurança às decisões de projeto
antes da implementação.
