#!/bin/sh
# Start the Todo App with Docker Compose
echo "Starting Todo App services..."
docker compose up --build -d
echo "Services started! API: http://localhost:8000, Web: http://localhost:5173"
