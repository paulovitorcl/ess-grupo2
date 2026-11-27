# Etapa 7 — Roteiro da apresentação final

**Status: versão inicial para preparação e ensaio.** A apresentação é presencial; este roteiro também pode orientar um vídeo opcional de documentação, que não substitui a apresentação.

O objetivo é mostrar como a análise do Sistema de Contabilidade evoluiu das ameaças aos controles, às verificações e ao [pipeline DevSecOps](etapa-7-devsecops-e-video-final.md). As falas abaixo servem como apoio e podem ser adaptadas ao meu jeito de apresentar, preservando as informações e evidências do projeto.

## 1. Sistema escolhido

**Mostrar:** [visão geral da arquitetura e do fluxo](../docs/etapa1/04-visao-geral-arquitetura-fluxo.md).

**Fala-base:** “Analisamos um sistema de contabilidade que atende diferentes empresas e concentra serviços fiscais, folha de pagamento e operações financeiras. Ele possui usuários com permissões distintas e integrações com bancos e órgãos governamentais. Dados pessoais, informações financeiras e ordens de pagamento tornam a segurança parte das regras do negócio. Nosso trabalho analisa esse sistema e apresenta exemplos executáveis de controles selecionados.”

Destacar os perfis de contador, cliente, administrador, funcionário e auditor, sem detalhar todas as funcionalidades. Encerrar apontando dois fluxos que orientarão a apresentação: acesso aos dados de uma empresa e autorização de pagamentos.

## 2. Ameaças e casos de abuso

**Mostrar:** um recorte da [modelagem STRIDE](../docs/etapa1/05-modelagem-ameacas-stride.md) e dos [casos de abuso](../docs/etapa1/06-casos-de-abuso.md).

**Fala-base:** “Usamos STRIDE para analisar falsificação de identidade, adulteração, repúdio, divulgação de informações, negação de serviço e elevação de privilégio. Entre os cenários relevantes estão o uso de credenciais comprometidas, o acesso aos dados de outra empresa e a execução de pagamentos sem autorização válida. Os casos de abuso descrevem como essas ações poderiam ocorrer e quais ativos seriam afetados.”

Usar o CA13, de pagamento não autorizado, como exemplo principal: explicar quem tenta agir, qual autorização pretende contornar e o possível prejuízo. Relacioná-lo às ameaças de adulteração e elevação de privilégio. Citar o acesso entre empresas como segundo exemplo e fazer a transição: “Esses cenários orientaram a priorização dos riscos.”

## 3. Riscos prioritários

**Mostrar:** R13, R18 e R01 no [registro de riscos](../docs/etapa2/2.4-registro-de-riscos.md), acompanhados da [estimativa de risco residual](../docs/etapa2/2.7-estrategias-de-tratamento.md).

**Fala-base:** “A pontuação combina probabilidade e impacto. Destacamos R13, relacionado aos pagamentos, R18, ao isolamento entre empresas, e R01, ao comprometimento de identidade. Os três receberam pontuação inicial 12, classificada como crítica. Isso orienta a implementação de controles de autorização, segregação de funções e proteção da autenticação.”

Explicar que o residual previsto para esses riscos é 8, ainda alto. Essa redução é uma estimativa condicionada à eficácia dos controles, não uma medição obtida pelos exemplos de código. Ressaltar que tratar um risco exige definir controle, responsável e evidência de verificação; não basta mudar sua classificação na tabela.

## 4. Requisitos e decisões de arquitetura

**Mostrar:** [diagrama da arquitetura segura](../diagramas/etapa-3/arquitetura-segura.png), [requisitos](../docs/etapa3/3.1-requisitos-de-seguranca.md) e [decisões arquiteturais](../docs/etapa3/3.4-decisoes-de-arquitetura.md).

**Fala-base:** “Os riscos foram traduzidos em requisitos verificáveis. RS01 trata da autorização de pagamentos; RS02, do vínculo entre usuário e empresa; RS03, da autenticação com MFA e limitação de tentativas. As decisões arquiteturais definem onde esses controles devem atuar.”

- **DA01:** centralizar no servidor a autorização por empresa e recurso, evitando que um identificador enviado pelo cliente seja suficiente para conceder acesso.
- **DA02:** separar autenticação, aprovação e execução do pagamento, exigindo autorização da operação e preservação dos dados aprovados.
- **DA03:** separar a proteção de segredos e a auditoria, reduzindo exposição de credenciais e apoiando a investigação de ações.

Apontar os componentes no diagrama e explicar que ele representa a arquitetura proposta. Os exemplos da próxima etapa verificam apenas um recorte dessas decisões.

## 5. Práticas de código seguro

**Mostrar:** [práticas da Etapa 4](../docs/etapa4/4-codigo-seguro-e-testes.md), [testes de autorização](../codigo/etapa-4/test_autorizacao.py), [testes de pagamentos](../codigo/etapa-4/test_pagamentos.py) e [saída dos testes](../evidencias/etapa-4/saida-testes.txt).

**Fala-base:** “Implementamos dois exemplos Python em memória. O primeiro verifica o vínculo ativo com a empresa e a permissão sobre o recurso, inclusive para administradores. O segundo separa criação e aprovação de pagamentos, exige MFA acima do limite configurado e verifica a integridade dos dados antes da execução.”

Exibir um caso válido e um caso malicioso de cada prática: acesso à própria empresa versus acesso cruzado; pagamento aprovado por outro usuário versus autoaprovação ou alteração posterior dos dados. A evidência registra **13 testes aprovados**.

Esclarecer que banco e MFA são simulados. Esses testes exercitam regras de RS01 e RS02; não demonstram integração bancária real, armazenamento persistente nem o fluxo completo de login e TOTP de RS03. Para evitar demora, usar a saída registrada; uma execução local pode ser preparada para o ensaio com `python -B -m unittest discover -s codigo/etapa-4 -v`.

## 6. Resultados da verificação

**Mostrar:** [análise da Etapa 5](../docs/etapa5/5-verificacao-de-vulnerabilidades.md) e um recorte do [relatório HTML do ZAP](../evidencias/etapa-5/zap-report.html).

**Fala-base:** “A verificação dinâmica foi realizada em um laboratório local com OWASP Juice Shop e OWASP ZAP. Foram analisados alertas de SQL Injection, atributos de segurança de cookies e informação sensível em URL. O exercício permitiu interpretar evidências e propor correções.”

- **SQL Injection:** mostrar o alerta e o erro de SQL observado; relacionar a prevenção ao uso de consultas parametrizadas e tratamento adequado de erros.
- **Cookies:** explicar a importância de avaliar os atributos de segurança conforme a função do cookie. O cookie de idioma observado não comprova roubo de sessão.
- **Informação na URL:** mostrar o parâmetro de e-mail e explicar sua possível exposição em registros e histórico; isso, isoladamente, não demonstra acesso indevido a outro usuário.

Concluir: os resultados pertencem ao laboratório Juice Shop. As lições são aplicáveis à análise do sistema contábil, mas uma implementação desse sistema precisaria de verificação própria.

## 7. Detecção e resposta

**Mostrar:** as três regras do [roteiro da Etapa 6](etapa-6-deteccao-de-intrusoes.md).

**Fala-base:** “Os controles preventivos precisam ser acompanhados de detecção. Propomos registrar eventos de autenticação, autorização e pagamentos para identificar comportamentos suspeitos e orientar a resposta.”

- **DET-01:** tentativas de autenticação suspeitas; exemplo: mais de 20 falhas envolvendo pelo menos 10 contas, pelo mesmo IP, em 5 minutos.
- **DET-02:** tentativas de acesso entre empresas; exemplo: pelo menos 5 negativas por usuário em 10 minutos.
- **DET-03:** possíveis fraudes em pagamentos; exemplo: divergência de integridade entre os dados aprovados e os dados a executar.

Explicar a sequência de resposta: analisar o alerta, conter a ação, investigar os eventos, corrigir a causa e recuperar o serviço, com comunicação e registro dos aprendizados. No caso de pagamento divergente, reter a operação antes do envio bancário. As regras são propostas documentais; os limiares precisam de calibração e não há monitoramento operacional comprovado.

## 8. Pipeline DevSecOps

**Mostrar:** a tabela do [pipeline e suas condições de bloqueio](etapa-7-devsecops-e-video-final.md).

**Fala-base:** “O pipeline conecta as etapas do trabalho: planejamento de ameaças, requisitos e arquitetura, implementação, testes automatizados, análise de código e dependências, teste dinâmico, implantação e monitoramento. Cada fase define uma atividade, sua evidência e uma condição para continuar.”

Destacar pelo menos três bloqueios concretos:

1. **B01:** teste obrigatório de segurança ausente, não executado ou reprovado.
2. **B02:** acesso entre empresas sem vínculo, autoaprovação ou execução de pagamento com dados diferentes dos aprovados.
3. **B03:** credencial, token ou chave privada real exposto em conteúdo versionado ou na saída do processo.

Explicar que corrigir um bloqueio exige nova verificação e registro da versão avaliada. Achados e incidentes voltam ao registro de riscos e aos testes. O pipeline é documental e não há CI nem implantação automatizada comprovada; isso está identificado na coluna de estado atual.

## 9. Aprendizados e encerramento

**Mostrar:** uma síntese visual: ameaça → risco → requisito → decisão → teste → detecção → revisão.

Pontos que posso destacar ao comentar os aprendizados, conforme minha experiência no trabalho:

- A modelagem precisa considerar como uma funcionalidade legítima pode ser usada de forma indevida.
- Priorizar riscos ajuda a justificar decisões de arquitetura; risco residual continua sujeito à verificação e à aceitação responsável.
- Testes negativos e interpretação dos alertas são necessários para avaliar controles; a aprovação de um exemplo não comprova toda a aplicação.
- Detecção, resposta e condições de bloqueio mantêm a segurança presente ao longo das mudanças.

**Sugestão de encerramento:** “O trabalho conecta riscos a decisões e evidências. Os próximos passos de uma implementação seriam ampliar os testes, integrar os componentes reais e validar o pipeline e o monitoramento em ambiente controlado.”

