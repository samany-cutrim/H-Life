# Frontend Web (Next.js)

## Principais Features

- Onboarding guiado com estados de carregamento e erro.
- Dashboard responsivo com temas light/dark (dark por padrão).
- Módulos: Nutrição, Lista de Compras, Treinos, Hidratação, Bioimpedância, Laudos, Relatórios, Evolução Corporal, Chat IA.
- Upload de fotos/vídeos com checklist, overlay e estimativa calórica.
- Service Worker + Web Push (VAPID) com fluxo de permissões.
- Acessibilidade: alto contraste, atalhos (`?` abre modal, `g n` navega para nutrição etc.).

## Stack

- Next.js 14 (App Router)
- TypeScript + Zod (validação)
- Zustand (estado)
- Tailwind CSS + Radix UI
- Workbox para SW/PWA

## Scripts

| Comando | Descrição |
|---------|-----------|
| `pnpm dev` | Dev server com HMR |
| `pnpm lint` | ESLint + Stylelint |
| `pnpm test` | Vitest + Testing Library |
| `pnpm build` | Build produção |
| `pnpm start` | Servir build |

### Observações para Windows

- Para remover a pasta de cache do Next.js use PowerShell com `Remove-Item -Recurse -Force .next`.

## Variáveis (`.env.local`)

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_VAPID_PUBLIC_KEY=...
NEXT_PUBLIC_SENTRY_DSN=
NEXT_PUBLIC_ANALYTICS_ID=
```

## Documentação Complementar

- Componentes em `frontend/src/components`
- Hooks em `frontend/src/hooks`
- Páginas em `frontend/src/app`
- Testes em `frontend/src/__tests__`

## Referências

- [Web Push on the Open Web](https://web.dev/push-notifications-overview/)
- [Next.js App Router](https://nextjs.org/docs/app)
