# 4. Visão Geral da Arquitetura e Fluxo

Arquitetura em camadas: clientes acessam o sistema por uma aplicação web/API,
protegida por autenticação (login + MFA) e autorização por perfil (RBAC). O
núcleo concentra os módulos de negócio, que persistem dados sensíveis e se
comunicam com serviços governamentais e bancários através de uma camada de
integração.

## 4.1 Arquitetura de alto nível

```mermaid
flowchart TB
    subgraph Atores["Atores"]
        Contador([Contador])
        Cliente([Cliente])
        Admin([Administrador])
        Auditor([Auditor])
    end

    subgraph Borda["Camada de Acesso"]
        WebAPI["Aplicação Web / API"]
        Auth["Autenticação + MFA / RBAC"]
    end

    subgraph Nucleo["Núcleo de Negócio"]
        Cadastro["Cadastro"]
        Escrit["Escrituração Contábil"]
        Fiscal["Fiscal / Tributário"]
        Folha["Folha de Pagamento"]
        Docs["Emissão de Documentos"]
        Pgto["Pagamentos"]
    end

    subgraph Dados["Persistência"]
        DB[("Banco de Dados")]
        Audit[("Trilha de Auditoria / Logs")]
    end

    subgraph Integr["Camada de Integração"]
        Banco["Bancos / Open Finance"]
        Receita["Receita Federal / SPED"]
        Pref["Prefeituras / NFS-e"]
        ESocial["eSocial"]
        ERP["ERP do Cliente"]
    end

    Contador & Cliente & Admin & Auditor --> WebAPI
    WebAPI --> Auth
    Auth --> Nucleo
    Nucleo --> DB
    Nucleo --> Audit
    Escrit & Fiscal --> Banco & Receita
    Docs --> Pref
    Folha --> ESocial
    Nucleo --> ERP
    Pgto --> Banco
```

## 4.2 Fluxo típico — do login ao lançamento auditado

```mermaid
sequenceDiagram
    actor C as Contador
    participant W as Web/API
    participant A as Auth (MFA/RBAC)
    participant N as Núcleo (Escrituração)
    participant D as Banco de Dados
    participant L as Auditoria/Logs

    C->>W: Credenciais (e-mail/senha)
    W->>A: Valida credenciais + MFA
    A-->>W: Sessão autenticada + perfil
    C->>W: Registra lançamento D/C
    W->>A: Verifica permissão (RBAC)
    A-->>W: Autorizado
    W->>N: Processa lançamento
    N->>D: Persiste dado financeiro
    N->>L: Grava trilha (quem/quando/valor)
    L-->>C: Confirmação
```

## 4.3 Fluxo típico — integração externa (transmissão fiscal)

```mermaid
sequenceDiagram
    participant N as Núcleo (Fiscal)
    participant I as Camada de Integração
    participant G as Serviço Governamental
    participant L as Auditoria/Logs

    N->>I: Solicita transmissão (SPED / NFS-e / eSocial)
    I->>G: Envia documento assinado (certificado digital)
    G-->>I: Protocolo de recebimento
    I->>L: Registra protocolo e rastro
    I-->>N: Confirma transmissão
```

> **Nota de segurança:** os pontos de maior exposição STRIDE concentram-se em
> três fronteiras — a **Camada de Acesso** (Spoofing/Elevation), a **Persistência
> e Trilha de Auditoria** (Tampering/Repudiation) e a **Camada de Integração**
> (Spoofing/Information Disclosure/Denial of Service). O detalhamento por caso de
> uso está no README e nos entregáveis do item 5.
