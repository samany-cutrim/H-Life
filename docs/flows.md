# Fluxos Principais

## Geração de Dieta/Treino

```mermaid
sequenceDiagram
    participant User
    participant Web
    participant API
    participant AI as IA Provider
    participant DB as Postgres
    participant Cache as Redis
    User->>Web: Solicita plano semanal
    Web->>API: POST /plan/nutrition/generate
    API->>DB: Busca histórico e restrições
    API->>AI: Prompt LLM + Regras internas
    AI-->>API: Cardápio e macros sugeridas
    API->>Cache: Salva rascunho
    API-->>Web: Plano detalhado + metas
    Web->>API: POST /plan/training/generate
    API->>DB: Consulta progressões
    API->>AI: Regras MoveNet/Progressão
    API-->>Web: Agenda semanal por modalidade
```

## Lista de Compras

```mermaid
flowchart TD
    A[Plano Nutricional] --> B[Normalizar porção]
    B --> C[Converter unidade (xícara -> g)]
    C --> D[Ajustar cru/cozido]
    D --> E[Aplicar rendimento/desperdício]
    E --> F[Somar por categoria]
    F --> G[Gerar checklist com quantidades]
```

## Evolução Corporal

```mermaid
sequenceDiagram
    participant Mobile
    participant API
    participant Storage as MinIO/S3
    participant Pose as Pose Pipeline
    participant Compare as Body Compare
    Mobile->>API: Solicita URL upload (metadados)
    API->>Storage: Gera presigned URL
    API-->>Mobile: URL + campos
    Mobile->>Storage: Upload fotos frente/lado/costas
    API->>Pose: Estimar keypoints (MoveNet)
    Pose-->>API: Keypoints + confiança
    API->>Compare: Calcular métricas (delta %, confiança)
    Compare-->>API: Resultado com veredito
    API-->>Mobile: Relatório de evolução
```
