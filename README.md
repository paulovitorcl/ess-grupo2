<div align="center">

# Sistema de Contabilidade — Análise de Segurança

_Modelagem de ameaças, riscos e segurança para um sistema contábil._

</div>

## Sobre o projeto

Este repositório reúne a análise de segurança de um **sistema de contabilidade**
desenvolvida ao longo da disciplina. O sistema presta serviços contábeis,
fiscais, de folha de pagamento e de pagamentos, com integrações externas
(bancos via Open Finance, Receita Federal, prefeituras, eSocial e ERP dos
clientes).

O foco do trabalho **não é implementar o software**, e sim compreender seu
funcionamento e analisar os problemas de segurança: ameaças, casos de abuso,
riscos, arquitetura segura, código seguro, verificação de vulnerabilidades,
detecção de intrusões e DevSecOps.

### Justificativa da escolha

Um sistema de contabilidade concentra **dados financeiros, fiscais e pessoais
sensíveis (LGPD)**, possui **múltiplos perfis de usuário** com permissões
distintas e realiza **troca de informações com serviços externos** e órgãos
governamentais. Esse contexto permite identificar ameaças e casos de abuso em
todas as categorias do STRIDE.

## Identificação

- **Sistema:** Sistema de Contabilidade
- **Repositório:** <https://github.com/paulovitorcl/ess-grupo2>
- **Integrantes:** ver seção [Integrantes](#integrantes)

## Perfis e atores principais

| Perfil | Papel |
| --- | --- |
| Contador | Usuário operacional interno: cadastros, lançamentos, apuração, folha, guias, notas e relatórios. |
| Cliente | Empresa/pessoa atendida: consulta documentos, cadastra dados bancários, emite notas, autoriza pagamentos. |
| Administrador | Gestão de acesso: cria/desativa contas, define perfis (RBAC), configura credenciais de API. |
| Auditor | Compliance: consulta a trilha de auditoria e exporta logs. |
| Funcionário (do cliente) | Acessa o próprio holerite. |
| Sistemas externos | Bancos, Receita Federal, prefeituras, eSocial e ERP do cliente. |

Os detalhes de atores, ativos e pontos de interação estão em
[Usuários, ativos e pontos de interação](docs/03-usuarios-e-pontos-de-interacao.md).

## Navegação por etapa

| Etapa | Status | Artefatos |
| --- | --- | --- |
| Base | Documentada | [Usuários e pontos de interação](docs/03-usuarios-e-pontos-de-interacao.md), [Arquitetura e fluxo](docs/04-visao-geral-arquitetura-fluxo.md) |
| 1. Ameaças STRIDE e casos de abuso | Documentada | [Modelagem de ameaças STRIDE](docs/etapa-1-ameacas-stride.md) |
| 2. Riscos e NIST CSF 2.0 | Planejada | `docs/etapa-2-riscos-nist.md` |
| 3. Arquitetura segura | Planejada | `docs/etapa-3-arquitetura-segura.md` |
| 4. Código seguro e testes | Planejada | `docs/etapa-4-codigo-seguro.md` |
| 5. Verificação de vulnerabilidades | Planejada | `evidencias/etapa-5/relatorio-da-verificacao.md` |
| 6. Detecção de intrusões | Planejada | `roteiros/etapa-6-deteccao-de-intrusoes.md` |
| 7. DevSecOps e apresentação final | Planejada | `roteiros/etapa-7-devsecops-e-video-final.md` |

> **Status:** _Documentada_ = artefato presente no repositório;
> _Planejada_ = etapa prevista, ainda a ser produzida.

## Organização do repositório

```
ess-grupo2/
├── README.md                         # esta página inicial
└── docs/
    ├── etapa-1-ameacas-stride.md      # casos de uso + STRIDE por funcionalidade
    ├── 03-usuarios-e-pontos-de-interacao.md
    └── 04-visao-geral-arquitetura-fluxo.md
```

Conforme as próximas etapas forem produzidas, serão adicionados os diretórios
`diagramas/`, `codigo/`, `evidencias/` e `roteiros/`, seguindo a estrutura
recomendada no enunciado da disciplina.

## Visão geral da arquitetura

Arquitetura em camadas: os atores acessam o sistema por uma aplicação web/API,
protegida por autenticação (login + MFA) e autorização por perfil (RBAC). O
núcleo concentra os módulos de negócio, que persistem dados sensíveis e se
comunicam com serviços governamentais e bancários por uma camada de integração.
Os diagramas (contexto, fluxo de dados e transmissão fiscal) estão em
[Visão geral da arquitetura e fluxo](docs/04-visao-geral-arquitetura-fluxo.md).

As fronteiras de maior exposição STRIDE são a **Camada de Acesso**
(Spoofing/Elevation), a **Persistência e Trilha de Auditoria**
(Tampering/Repudiation) e a **Camada de Integração**
(Spoofing/Information Disclosure/Denial of Service).

## Integrantes

- Jeanluca
- Paulo Vitor (paulovitorcl)
- Andrey Dias

Cada integrante demonstra sua participação por meio de commits próprios no
repositório. Verifique se seus commits estão corretamente associados à sua
conta do GitHub.
