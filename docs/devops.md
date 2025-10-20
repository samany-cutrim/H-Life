# DevOps & Qualidade

## CI/CD

- GitHub Actions (`.github/workflows/ci.yml`): lint, type-check, testes backend/frontend/mobile, build web/mobile, checagem de migrations.
- Pipeline de deploy opcional (`deploy.yml`) com Docker build + push para Render/Fly/DO.

## Observabilidade

- Sentry (web/mobile/backend) configurado via env.
- LogRocket no front.
- Prometheus + Grafana (dashboards em `infra/monitoring`).

## Backups

- `pg_dump` diário armazenado em S3 (`s3://h-life-backups`).
- Retenção de 30 dias, criptografado com KMS.

## Qualidade

- Coverage mínimo 80% (backend) e 70% (frontend/mobile) validado em CI.
- Dependabot habilitado.
- Renovação automática de certificados via GitHub Actions + Terraform Cloud.

## Scripts

| Comando | Descrição |
|---------|-----------|
| `make qa` | Lint + testes + coverage consolidado |
| `make docker-build` | Build imagens multi-stage |
| `make migrate-check` | Verifica migrations pendentes |
