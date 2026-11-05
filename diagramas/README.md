# Diagramas

Arquivos-fonte dos diagramas do trabalho, organizados por etapa.

| Etapa | Arquivo | Descrição | Usado em |
| --- | --- | --- | --- |
| 1 | [`etapa-1/arquitetura-alto-nivel.mmd`](etapa-1/arquitetura-alto-nivel.mmd) | Atores, camadas de acesso, núcleo, persistência e integrações | [4.1](../docs/etapa1/04-visao-geral-arquitetura-fluxo.md#41-arquitetura-de-alto-nível) |
| 1 | [`etapa-1/fluxo-login-lancamento.mmd`](etapa-1/fluxo-login-lancamento.mmd) | Sequência do login ao lançamento auditado | [4.2](../docs/etapa1/04-visao-geral-arquitetura-fluxo.md#42-fluxo-típico--do-login-ao-lançamento-auditado) |
| 1 | [`etapa-1/fluxo-transmissao-fiscal.mmd`](etapa-1/fluxo-transmissao-fiscal.mmd) | Sequência da transmissão fiscal (SPED/NFS-e/eSocial) | [4.3](../docs/etapa1/04-visao-geral-arquitetura-fluxo.md#43-fluxo-típico--integração-externa-transmissão-fiscal) |

Os diagramas estão em [Mermaid](https://mermaid.js.org/), renderizado
diretamente pelo GitHub nos documentos Markdown. Para gerar a imagem PNG de um
arquivo `.mmd`:

```bash
npx @mermaid-js/mermaid-cli -i etapa-1/arquitetura-alto-nivel.mmd -o etapa-1/arquitetura-alto-nivel.png -b white
```

Ao alterar um diagrama, atualize o `.mmd` e o bloco correspondente no
documento Markdown.
