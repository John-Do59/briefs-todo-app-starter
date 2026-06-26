#!/bin/sh
# Run all Todo App tests
set -e

echo "Running API tests..."
cd api
uv sync
uv run pytest tests/ -v
cd ..

echo "Running frontend tests..."
cd web
bun install
bun run test
cd ..

echo "All tests passed!"
