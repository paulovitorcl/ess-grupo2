# Modelagem de Ameaças STRIDE — Sistema de Contabilidade

Este documento especifica os **casos de uso** de um sistema que presta serviços de
contabilidade e realiza o **mapeamento das ameaças STRIDE** aplicáveis a cada
funcionalidade, com justificativa breve de cada categoria.

## Categorias STRIDE

| Letra | Ameaça | Propriedade violada |
|-------|--------|---------------------|
| **S** | Spoofing (falsificação de identidade) | Autenticação |
| **T** | Tampering (adulteração de dados) | Integridade |
| **R** | Repudiation (repúdio) | Não-repúdio |
| **I** | Information Disclosure (vazamento) | Confidencialidade |
| **D** | Denial of Service (negação de serviço) | Disponibilidade |
| **E** | Elevation of Privilege (elevação de privilégio) | Autorização |

## Módulos e Funcionalidades

| Módulo | Funcionalidade |
|--------|----------------|
| Autenticação / Acesso | Login de contadores, clientes e administradores; MFA; recuperação de senha |
| Cadastro | Empresas, sócios, plano de contas, CNPJ/CPF, dados bancários |
| Escrituração contábil | Lançamentos de débito/crédito |
| Fiscal / Tributário | Apuração de impostos, emissão de guias (DARF/DAS) |
| Folha de pagamento | Cálculo de salários, encargos (INSS/FGTS), holerites |
| Emissão de documentos | Notas fiscais (NF-e/NFS-e), relatórios |
| Integrações | APIs de bancos (Open Finance), Receita Federal, prefeituras, ERP dos clientes |
| Auditoria / Logs | Trilha de auditoria de lançamentos e alterações |
| Pagamentos | Emissão de boletos, integração com contas bancárias |

---

## 1. Autenticação / Acesso

### Casos de uso
- **UC-01** — Contador realiza login com e-mail e senha
- **UC-02** — Usuário valida segundo fator (MFA)
- **UC-03** — Cliente solicita recuperação de senha
- **UC-04** — Administrador cria/desativa contas
- **UC-05** — Sistema encerra sessão por inatividade
- **UC-06** — Administrador define perfis e permissões (RBAC)

### Avaliação STRIDE

**UC-01 — Login com e-mail/senha**
- **S**: alvo clássico de credential stuffing / roubo de credenciais para se passar por usuário legítimo
- **R**: sem log de IP/device, o usuário pode negar acessos
- **I**: mensagens de erro podem revelar existência de contas (enumeração)
- **D**: tentativas em massa podem saturar o serviço ou disparar lockout geral

**UC-02 — Validação MFA**
- **S**: bypass de MFA (SIM swap, phishing de OTP) permite falsificar identidade
- **D**: flood de códigos pode esgotar SMS/quota e bloquear acesso legítimo

**UC-03 — Recuperação de senha**
- **S**: sequestro de conta via reset se o token for previsível
- **I**: fluxo pode confirmar se o e-mail existe
- **E**: manipular `user_id` no reset permite trocar senha de outro usuário

**UC-04 — Criar/desativar contas**
- **R**: alterações administrativas precisam de rastro de autoria
- **E**: falha de controle permite criar conta com privilégios indevidos

**UC-05 — Encerramento por inatividade**
- **S**: sessão não expirada permite sequestro/reuso por terceiros

**UC-06 — Definir perfis/permissões (RBAC)**
- **T**: adulteração de permissões altera o modelo de acesso
- **R**: mudanças de privilégio exigem auditoria
- **E**: núcleo da escalada — perfil mal atribuído concede poderes indevidos

---

## 2. Cadastro

### Casos de uso
- **UC-07** — Contador cadastra nova empresa (CNPJ, regime tributário)
- **UC-08** — Contador vincula sócios/responsáveis (CPF)
- **UC-09** — Usuário importa/valida CNPJ na base da Receita
- **UC-10** — Contador configura o plano de contas
- **UC-11** — Cliente cadastra/atualiza dados bancários
- **UC-12** — Administrador inativa empresa encerrada

### Avaliação STRIDE

**UC-07 — Cadastrar empresa**
- **T**: alteração de regime tributário/CNPJ afeta toda a apuração
- **R**: precisa registrar quem cadastrou/alterou
- **I**: dados cadastrais são sensíveis (LGPD)

**UC-08 — Vincular sócios (CPF)**
- **T**: adulteração de vínculo societário
- **I**: CPF e dados pessoais expostos

**UC-09 — Validar CNPJ na Receita**
- **S**: resposta forjada de servidor falso
- **T**: MITM alterando situação cadastral
- **I**: exposição de dados retornados pela consulta

**UC-10 — Configurar plano de contas**
- **T**: alteração indevida distorce a contabilidade
- **R**: exige rastro de quem alterou a estrutura
- **E**: usuário sem permissão modificando estrutura contábil

**UC-11 — Cadastrar dados bancários**
- **T**: troca de conta = fraude de desvio de pagamento
- **R**: alteração precisa de autoria registrada
- **I**: dados bancários são sensíveis

**UC-12 — Inativar empresa**
- **T**: inativação indevida oculta obrigações
- **R**: ação relevante exige auditoria
- **E**: operação restrita a perfis autorizados

---

## 3. Escrituração Contábil

### Casos de uso
- **UC-13** — Contador registra lançamento de débito/crédito
- **UC-14** — Sistema importa lançamentos em lote (planilha/OFX)
- **UC-15** — Contador realiza conciliação bancária
- **UC-16** — Contador estorna/ajusta lançamento
- **UC-17** — Contador encerra período contábil (bloqueio)
- **UC-18** — Usuário consulta livro-razão e diário

### Avaliação STRIDE

**UC-13 — Registrar lançamento D/C**
- **T**: adulteração de valor compromete a integridade contábil
- **R**: lançamento fraudulento pode ser negado sem trilha
- **I**: lançamentos revelam dados financeiros
- **E**: perfil somente-leitura não deveria criar lançamentos

**UC-14 — Importar lançamentos em lote**
- **T**: arquivo importado pode ser adulterado
- **R**: origem/autoria da carga precisa ser registrada
- **I**: arquivo contém dados financeiros
- **D**: cargas volumosas podem saturar o processamento

**UC-15 — Conciliação bancária**
- **T**: manipulação de matches oculta divergências
- **R**: ajustes precisam de rastro
- **I**: exposição de extratos/saldos

**UC-16 — Estornar/ajustar lançamento**
- **T**: estorno usado para mascarar fraude
- **R**: exige auditoria do valor anterior
- **E**: operação sensível restrita a perfil autorizado

**UC-17 — Encerrar período (bloqueio)**
- **T**: alterar período fechado quebra a integridade
- **R**: quem encerrou/reabriu deve ser registrado
- **E**: reabertura de período é privilégio restrito

**UC-18 — Consultar razão/diário**
- **I**: exposição de dados financeiros completos
- **E**: IDOR/multi-tenant — ver dados de outra empresa

---

## 4. Fiscal / Tributário

### Casos de uso
- **UC-19** — Sistema apura impostos do período (ICMS/ISS/IRPJ/PIS-COFINS)
- **UC-20** — Contador emite guia DARF/DAS
- **UC-21** — Sistema gera arquivo SPED
- **UC-22** — Contador valida e retifica apuração
- **UC-23** — Usuário consulta calendário de obrigações/vencimentos

### Avaliação STRIDE

**UC-19 — Apurar impostos**
- **T**: alteração da base/valor gera guia incorreta
- **R**: apuração precisa de autoria e versão
- **I**: exposição de dados fiscais
- **D**: apurações massivas sobrecarregam o serviço

**UC-20 — Emitir DARF/DAS**
- **T**: adulteração de valor/código de barras
- **R**: emissão precisa ser rastreável
- **I**: guia contém dados fiscais sensíveis

**UC-21 — Gerar SPED**
- **T**: adulteração do arquivo entregue ao fisco
- **I**: SPED concentra toda a informação fiscal
- **D**: geração pesada pode travar o serviço

**UC-22 — Validar/retificar apuração**
- **T**: retificação indevida
- **R**: exige trilha da retificação
- **E**: operação restrita a perfil autorizado

**UC-23 — Consultar obrigações/vencimentos**
- **I**: exposição de agenda fiscal da empresa

---

## 5. Folha de Pagamento

### Casos de uso
- **UC-24** — Sistema calcula salários e encargos (INSS/FGTS)
- **UC-25** — Contador processa a folha do mês
- **UC-26** — Sistema gera holerites dos funcionários
- **UC-27** — Contador lança férias/rescisão/13º
- **UC-28** — Sistema transmite eventos ao eSocial

### Avaliação STRIDE

**UC-24 — Calcular salários/encargos**
- **T**: manipulação de base de cálculo
- **R**: alterações de rubrica exigem rastro
- **I**: salários e encargos são dados sensíveis

**UC-25 — Processar folha do mês**
- **T**: adulteração dos valores processados
- **R**: fechamento precisa de autoria
- **I**: exposição de remuneração de todos
- **D**: processamento pesado sujeito a sobrecarga

**UC-26 — Gerar holerites**
- **I**: holerite contém dado pessoal/salarial
- **E**: acesso ao holerite de outro funcionário (IDOR)

**UC-27 — Lançar férias/rescisão/13º**
- **T**: adulteração de verbas rescisórias
- **R**: exige auditoria dos lançamentos
- **I**: dados trabalhistas sensíveis

**UC-28 — Transmitir eSocial**
- **S**: certificado/identidade perante o governo
- **T**: adulteração dos eventos transmitidos
- **R**: transmissão precisa de comprovante/rastro
- **I**: dados trabalhistas expostos

---

## 6. Emissão de Documentos

### Casos de uso
- **UC-29** — Cliente emite NF-e / NFS-e
- **UC-30** — Sistema cancela/corrige nota fiscal
- **UC-31** — Contador gera relatórios (balancete, DRE, balanço)
- **UC-32** — Usuário exporta documentos (PDF/XML)

### Avaliação STRIDE

**UC-29 — Emitir NF-e / NFS-e**
- **S**: uso indevido do certificado digital da empresa
- **T**: adulteração de valores/itens da nota
- **R**: emissão precisa ser rastreável
- **I**: nota contém dados fiscais e de clientes

**UC-30 — Cancelar/corrigir nota**
- **T**: cancelamento usado para ocultar operação
- **R**: exige trilha de quem cancelou
- **E**: operação sensível restrita a perfil

**UC-31 — Gerar relatórios (DRE/balanço)**
- **T**: manipulação de parâmetros distorce o resultado
- **I**: relatório expõe situação financeira completa
- **D**: relatórios pesados podem sobrecarregar
- **E**: acesso a relatório de empresa alheia

**UC-32 — Exportar documentos (PDF/XML)**
- **R**: exportações devem ser logadas (vazamento de dados)
- **I**: exfiltração de documentos sensíveis
- **E**: baixar documento de outro tenant

---

## 7. Integrações

### Casos de uso
- **UC-33** — Sistema importa extratos bancários via Open Finance
- **UC-34** — Sistema consulta situação cadastral na Receita Federal
- **UC-35** — Sistema transmite NFS-e à prefeitura
- **UC-36** — Sistema sincroniza dados com o ERP do cliente
- **UC-37** — Administrador configura/renova credenciais de API

### Avaliação STRIDE

**UC-33 — Importar extratos (Open Finance)**
- **S**: servidor falso se passando pelo banco
- **T**: MITM alterando extratos
- **I**: dados bancários trafegados
- **D**: falha/indisponibilidade da integração paralisa importação

**UC-34 — Consultar Receita Federal**
- **S**: endpoint forjado
- **T**: adulteração da resposta em trânsito
- **I**: dados cadastrais retornados
- **D**: dependência externa sujeita a indisponibilidade

**UC-35 — Transmitir NFS-e à prefeitura**
- **S**: identidade/certificado perante a prefeitura
- **T**: adulteração do documento transmitido
- **R**: transmissão precisa de protocolo/rastro
- **I**: dados fiscais em trânsito
- **D**: fila de transmissão pode ser saturada

**UC-36 — Sincronizar com ERP do cliente**
- **S**: autenticação mútua entre sistemas
- **T**: dados adulterados na sincronização
- **I**: exposição de dados entre sistemas
- **D**: sync massivo pode sobrecarregar

**UC-37 — Configurar/renovar credenciais API**
- **S**: credencial comprometida permite impersonação
- **T**: alteração de endpoint/segredo
- **R**: mudança de credencial exige rastro
- **I**: vazamento de tokens/segredos
- **E**: quem configura integração ganha acesso amplo

---

## 8. Auditoria / Logs

### Casos de uso
- **UC-38** — Sistema registra quem alterou cada lançamento (quando/valor anterior)
- **UC-39** — Auditor consulta trilha de auditoria por período/usuário
- **UC-40** — Sistema registra logins e acessos a dados sensíveis
- **UC-41** — Administrador exporta logs para análise/compliance

### Avaliação STRIDE

**UC-38 — Registrar alteração de lançamento**
- **T**: adulteração do próprio log invalida a auditoria
- **R**: é o controle central de não-repúdio
- **I**: logs contêm valores e dados sensíveis

**UC-39 — Consultar trilha de auditoria**
- **T**: manipulação de filtros oculta eventos
- **I**: exposição de quem fez o quê
- **E**: acesso à auditoria de outro tenant

**UC-40 — Registrar logins/acessos sensíveis**
- **T**: adulteração de registros de acesso
- **R**: base para provar/negar acessos
- **I**: metadados de acesso são sensíveis

**UC-41 — Exportar logs (compliance)**
- **T**: log exportado pode ser alterado
- **R**: exportação precisa ser rastreada
- **I**: pacote de logs concentra dados sensíveis
- **E**: exportação restrita a auditor/admin

---

## 9. Pagamentos

### Casos de uso
- **UC-42** — Contador emite boleto de honorários
- **UC-43** — Sistema concilia pagamentos recebidos
- **UC-44** — Cliente agenda/autoriza pagamento de guias via conta bancária
- **UC-45** — Sistema notifica boletos vencidos/baixados

### Avaliação STRIDE

**UC-42 — Emitir boleto de honorários**
- **T**: adulteração de valor/linha digitável
- **R**: emissão precisa de rastro
- **I**: dados de cobrança expostos

**UC-43 — Conciliar pagamentos recebidos**
- **T**: manipulação de baixas oculta inadimplência/fraude
- **R**: conciliação precisa de autoria
- **I**: dados financeiros expostos

**UC-44 — Autorizar pagamento de guias**
- **S**: autorização precisa comprovar identidade do autorizador
- **T**: alteração de beneficiário/valor = desvio
- **R**: autorização precisa de rastro forte (quem/quando)
- **I**: dados bancários sensíveis
- **E**: pagamento é operação de alto privilégio (segregação de funções)

**UC-45 — Notificar boletos vencidos/baixados**
- **S**: notificação falsa (phishing) com boleto adulterado
- **I**: exposição de dados de cobrança ao destinatário errado

---

## Padrões observados

- **T (Tampering)** e **R (Repudiation)** aparecem em quase todo UC que **cria ou altera dado financeiro/fiscal** → exigem trilha de auditoria imutável.
- **I (Information Disclosure)** domina onde há **dado pessoal/sensível (LGPD)** — folha, cadastros, holerites.
- **S (Spoofing)** concentra-se em **autenticação e integrações externas** (certificados, tokens, mTLS).
- **E (Elevation of Privilege)** surge em operações com **regra de autorização por perfil/tenant** (bloqueio de período, RBAC, multiempresa).
- **D (Denial of Service)** foca em **processamentos pesados e integrações em lote** (apuração, SPED, importações).
