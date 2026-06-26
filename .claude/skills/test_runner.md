---
name: test_runner
description: Run tests for the Todo App (API and frontend)
triggers:
  - user asks to run tests
  - user asks to test the app
  - testing the todo app
---

# Test Runner Skill

## Commands

### Run API tests
```sh
cd api
uv sync
uv run pytest tests/ -v
cd ..
```

### Run frontend tests
```sh
cd web
bun install
bun run test
cd ..
```
