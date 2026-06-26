---
name: docker_manage
description: Manage Docker Compose for the Todo App
triggers:
  - user asks to start docker
  - user asks to start services
  - start docker compose
  - stop docker compose
  - restart services
---

# Docker Management Skill

## Commands

### Start services
```sh
docker compose up --build -d
```

### Stop services
```sh
docker compose down
```

### Follow logs
```sh
docker compose logs -f
```
