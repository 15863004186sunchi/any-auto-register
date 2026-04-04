#!/bin/bash

# =================================================================
# Any Auto Register Deployment Script (Linux/Docker)
# =================================================================

ACTION=$1

case $ACTION in
  start)
    echo "🚀 Starting services..."
    docker compose up -d --build
    ;;
  stop)
    echo "🛑 Stopping services..."
    docker compose down
    ;;
  restart)
    echo "🔄 Restarting services..."
    docker compose down
    docker compose up -d --build
    ;;
  logs)
    echo "📋 Showing logs (Ctrl+C to exit)..."
    docker compose logs -f app
    ;;
  status)
    echo "📊 Service status:"
    docker compose ps
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|logs|status}"
    exit 1
esac
