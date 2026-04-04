# =================================================================
# Any Auto Register Deployment Script (Windows/Docker)
# =================================================================

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("start", "stop", "restart", "logs", "status")]
    [string]$Action
)

switch ($Action) {
    "start" {
        Write-Host "🚀 Starting services..." -ForegroundColor Cyan
        docker compose up -d --build
    }
    "stop" {
        Write-Host "🛑 Stopping services..." -ForegroundColor DarkYellow
        docker compose down
    }
    "restart" {
        Write-Host "🔄 Restarting services..." -ForegroundColor Cyan
        docker compose down
        docker compose up -d --build
    }
    "logs" {
        Write-Host "📋 Showing logs (Ctrl+C to exit)..." -ForegroundColor Gray
        docker compose logs -f app
    }
    "status" {
        Write-Host "📊 Service status:" -ForegroundColor Cyan
        docker compose ps
    }
}
