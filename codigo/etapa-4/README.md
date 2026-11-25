# Etapa 4 — Código Seguro e Testes de Segurança

Código e testes executáveis das duas práticas descritas em
[`docs/etapa4/4-codigo-seguro-e-testes.md`](../../docs/etapa4/4-codigo-seguro-e-testes.md).

| Arquivo | Conteúdo |
| --- | --- |
| `test_autorizacao.py` | Testes TS01–TS06 da Prática 1 (escritos antes da implementação) |
| `autorizacao.py` | Prática 1 — autorização por empresa e recurso (RS02 / DA01) |
| `test_pagamentos.py` | Testes TS07–TS12 da Prática 2 (escritos antes da implementação) |
| `pagamentos.py` | Prática 2 — autorização de transação de pagamentos (RS01 / DA02) |

## Como executar

Requer Python 3.10+ e nenhuma dependência externa.

```bash
cd codigo/etapa-4
python3 -m unittest -v
```

A saída da última execução está em
[`evidencias/etapa-4/saida-testes.txt`](../../evidencias/etapa-4/saida-testes.txt).
