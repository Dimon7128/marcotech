# Phase 1 — Local App (no Docker)

Visual reference for the Phase 1 build: **frontend + backend + Excel as persistence**.
Use these diagrams as the mental model while you implement the app.

---

## 1. High‑level architecture

```mermaid
flowchart LR
    subgraph Browser["Browser (localhost)"]
        FE["Frontend<br/>HTML + CSS + JS<br/>index.html / style.css / app.js"]
    end

    subgraph Server["Backend (Python — Flask / FastAPI)"]
        API["API layer<br/>GET /api/convert<br/>GET /health"]
        SVC["Service layer<br/>business logic"]
        REPO["Repository layer<br/>ExcelRepository"]
    end

    EXT["External Currency API<br/>(e.g. exchangerate.host)"]
    XLSX[("app_data.xlsx<br/>request history")]

    FE -- "HTTP GET<br/>/api/convert?amount&from&to" --> API
    API --> SVC
    SVC -- "fetch rates" --> EXT
    EXT -- "JSON rate" --> SVC
    SVC -- "save row" --> REPO
    REPO -- "append" --> XLSX
    SVC -- "result" --> API
    API -- "JSON response" --> FE

    classDef store fill:#fff4c2,stroke:#b8860b,color:#000;
    classDef ext fill:#e8e8ff,stroke:#4848c4,color:#000;
    class XLSX store;
    class EXT ext;
```

**Key rule:** the frontend never touches the Excel file. Only the backend does.

---

## 2. Folder structure

```mermaid
flowchart TD
    ROOT["myapp/"]
    FE["frontend/"]
    BE["backend/"]

    ROOT --> FE
    ROOT --> BE

    FE --> FE1["index.html"]
    FE --> FE2["style.css"]
    FE --> FE3["app.js"]

    BE --> BE1["app.py<br/>(API layer / routes)"]
    BE --> SVCS["services/"]
    BE --> DATA["data/"]
    BE --> TESTS["tests/"]

    SVCS --> SVC1["external_api.py<br/>(calls currency API)"]
    SVCS --> SVC2["repository.py<br/>(ExcelRepository)"]

    DATA --> XLSX["app_data.xlsx"]
```

---

## 3. Request flow — “Convert” button

```mermaid
sequenceDiagram
    autonumber
    actor U as User
    participant FE as Frontend (app.js)
    participant API as Backend API<br/>/api/convert
    participant SVC as Service layer
    participant EXT as External API
    participant REPO as ExcelRepository
    participant XLSX as app_data.xlsx

    U->>FE: fills amount + from + to,<br/>clicks "Convert"
    FE->>API: GET /api/convert?amount&from&to
    API->>SVC: convert(amount, from, to)
    SVC->>EXT: GET rates(from, to)
    EXT-->>SVC: { rate }
    SVC->>SVC: result = amount * rate
    SVC->>REPO: save(timestamp, amount, from, to, result)
    REPO->>XLSX: append row
    XLSX-->>REPO: ok
    REPO-->>SVC: ok
    SVC-->>API: { result }
    API-->>FE: 200 JSON { result }
    FE-->>U: render result on page

    Note over FE,API: On error → backend returns 4xx/5xx,<br/>frontend shows error message
```

---

## 4. Backend layering & the swap point

The whole point of splitting layers in Phase 1 is so that **only the repository changes** later.

```mermaid
flowchart TB
    subgraph BE["Backend"]
        direction TB
        A["API layer<br/>routes, request/response, validation"]
        S["Service layer<br/>convert(), call external API,<br/>ask repo to save"]
        R["Repository interface<br/>save(history_row)"]
    end

    EXCEL["ExcelRepository<br/>(Phase 1)"]:::now
    PG["PostgresRepository<br/>(Phase 2+)"]:::later

    A --> S --> R
    R -. implements .-> EXCEL
    R -. implements .-> PG

    classDef now fill:#d6f5d6,stroke:#2e7d32,color:#000;
    classDef later fill:#f0f0f0,stroke:#888,color:#555,stroke-dasharray: 4 3;
```

Frontend ↔ API contract stays identical when the repo is swapped.

---

## 5. Health check

```mermaid
flowchart LR
    Client["curl / browser / monitor"] -- "GET /health" --> H["Backend /health"]
    H -- "200 OK<br/>{ \"status\": \"ok\" }" --> Client
```

---

## 6. Done criteria checklist

```mermaid
flowchart TD
    D1["Frontend works in browser"]:::ok
    D2["Backend works locally"]:::ok
    D3["One external API integrated"]:::ok
    D4["Excel file stores history"]:::ok
    D5["/health returns 200"]:::ok

    classDef ok fill:#e7f7e7,stroke:#2e7d32,color:#000;
```

---

## 7. Excel row schema

| column      | example                  |
|-------------|--------------------------|
| timestamp   | 2026-04-30T19:37:12Z     |
| amount      | 100                      |
| from        | USD                      |
| to          | EUR                      |
| result      | 92.34                    |
