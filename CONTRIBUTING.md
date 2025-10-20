# Guia de Contribuição

Obrigado por considerar contribuir com o H-Life! 💙

## Como Começar

1. Faça um fork do repositório.
2. Crie um branch: `git checkout -b feature/minha-feature`.
3. Siga o estilo de código descrito abaixo.
4. Adicione testes para qualquer nova funcionalidade.
5. Atualize a documentação quando necessário.
6. Abra um Pull Request com descrição clara.

## Convenções de Código

- **Backend (Python)**: siga `black`/`ruff`, tipagem obrigatória, Pydantic v2.
- **Frontend (Next.js)**: TypeScript estrito, componentes acessíveis (ARIA).
- **Mobile (Flutter)**: lint `flutter analyze`, use Riverpod/Zod conforme arquitetura.

## Commits

- Use mensagens no formato `tipo: resumo curto` (ex: `feat: adiciona relatório semanal`).
- Tipos comuns: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.

## Testes & Qualidade

- `poetry run pytest` (backend)
- `pnpm lint && pnpm test` (frontend)
- `flutter test` (mobile)
- Certifique-se que a cobertura não diminuiu.

## Pull Requests

Inclua no PR:

- Contexto do problema
- Screenshots (quando UI)
- Passos de teste manual

## Canal de Contato

- Discord interno
- Email: dev@h-life.test
