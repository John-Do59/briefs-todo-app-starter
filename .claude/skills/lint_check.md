---
name: lint_check
description: Run linting for the Todo App
triggers:
  - user asks to lint
  - user asks to check linting
  - linting the todo app
---

# Linting Skill

## Commands

### Run repo-level linting
```sh
bun install
bun run lint
```

### Run API linting (ruff)
```sh
cd api
uv sync
uv run ruff check .
cd ..
```
