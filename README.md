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
funcionamento e analisar seus problemas de segurança: ameaças, casos de abuso,
riscos, arquitetura segura, código seguro, verificação de vulnerabilidades,
detecção de intrusões e DevSecOps.

## Identificação

- **Sistema:** Sistema de Contabilidade
- **Repositório:** <https://github.com/paulovitorcl/ess-grupo2>
- **Integrantes:** Andrey Dias, Jeanluca Martins, João Carlos Gonçalves e
  Paulo Vitor Costa Lima
- **Justificativa:** um sistema de contabilidade concentra **dados financeiros,
  fiscais e pessoais sensíveis (LGPD)**, possui **múltiplos perfis de usuário**
  com permissões distintas e realiza **troca de informações com serviços
  externos** e órgãos governamentais. Esse contexto permite identificar
  ameaças e casos de abuso em todas as categorias do STRIDE.

## Entregáveis por etapa

| Etapa | Status | Artefatos |
| --- | --- | --- |
| **1. Ameaças STRIDE e casos de abuso** | Concluída | [1. Identificação](docs/etapa1/01-identificacao-do-sistema.md) · [2. Descrição](docs/etapa1/02-descricao-do-sistema.md) · [3. Usuários, ativos e pontos de interação](docs/etapa1/03-usuarios-e-pontos-de-interacao.md) · [4. Arquitetura e fluxo](docs/etapa1/04-visao-geral-arquitetura-fluxo.md) · [Casos de uso e STRIDE por funcionalidade](docs/etapa1/casos-de-uso-stride.md) · [5. Modelagem STRIDE](docs/etapa1/05-modelagem-ameacas-stride.md) · [6. Casos de abuso](docs/etapa1/06-casos-de-abuso.md) · [7. Considerações finais](docs/etapa1/07-consideracoes-finais.md) |
| **2. Riscos e NIST CSF 2.0** | Em andamento | [Introdução](docs/etapa2/2.0-analise-e-priorizacao-de-riscos.md) · [2.1 Probabilidade](docs/etapa2/2.1-criterios-probabilidade.md) · [2.2 Impacto](docs/etapa2/2.2-criterios-impacto.md) · [2.3 Cálculo e classificação](docs/etapa2/2.3-calculo-e-classificacao.md) |
| **3. Arquitetura segura** | Planejada | `docs/etapa3/` · `diagramas/etapa-3/` |
| **4. Código seguro e testes** | Planejada | `docs/etapa4/` · [`codigo/etapa-4/`](codigo/etapa-4/) |
| **5. Verificação de vulnerabilidades** | Planejada | [`evidencias/etapa-5/`](evidencias/etapa-5/) |
| **6. Detecção de intrusões** | Planejada | [Roteiro](roteiros/etapa-6-deteccao-de-intrusoes.md) |
| **7. DevSecOps e apresentação final** | Planejada | [Roteiro](roteiros/etapa-7-devsecops-e-video-final.md) |
| **Artigo (SBC/IEEE)** | Planejado | [`artigo/`](artigo/) |

> _Concluída_ = artefatos completos no repositório; _Em andamento_ = parte
> dos itens produzida; _Planejada_ = etapa prevista, ainda a ser produzida.

## Organização do repositório

```
ess-grupo2/
├── README.md                  # esta página inicial
├── docs/
│   ├── etapa1/                # Etapa 1 — STRIDE e casos de abuso
│   └── etapa2/                # Etapa 2 — riscos e NIST CSF 2.0
├── diagramas/
│   └── etapa-1/               # fontes Mermaid (.mmd) dos diagramas
├── codigo/
│   └── etapa-4/               # implementação/pseudocódigo e testes
├── evidencias/
│   └── etapa-5/               # relatório e capturas de tela do ZAP
├── roteiros/                  # Etapas 6 e 7
└── artigo/                    # artigo final (template SBC ou IEEE)
```

## Visão geral da arquitetura

Arquitetura em camadas: os atores acessam o sistema por uma aplicação web/API,
protegida por autenticação (login + MFA) e autorização por perfil (RBAC). O
núcleo concentra os módulos de negócio, que persistem dados sensíveis e se
comunicam com serviços governamentais e bancários por uma camada de integração.
Os diagramas estão em
[Visão geral da arquitetura e fluxo](docs/etapa1/04-visao-geral-arquitetura-fluxo.md)
e suas fontes em [`diagramas/etapa-1/`](diagramas/etapa-1/).

## Participação

Cada integrante demonstra sua participação por meio de commits próprios no
repositório, com mensagens que descrevem a contribuição realizada (por
exemplo, `Inclui caso de abuso de alteração de pagamento`). Verifique se seus
commits estão associados à sua conta do GitHub.
