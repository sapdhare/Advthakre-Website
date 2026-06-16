#!/bin/bash

cd /opt/advthakre || exit 1

echo "Pulling latest code..."
git pull origin main

echo "Rebuilding containers..."
docker compose up -d --build

echo "Cleaning old Docker images..."
docker image prune -f

echo "Deployment completed!"
