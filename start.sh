#!/usr/bin/env bash
# Sobe backend (FastAPI, :8000) e frontend (Vite, :5173) juntos.
# Uso: ./start.sh   (Ctrl+C encerra os dois)
#
# uvicorn --reload e "npm run dev" geram processos-filhos reais no Windows;
# um `kill` simples no PID pai não mata a árvore, por isso usamos taskkill /T.

set -e
cd "$(dirname "$0")"

BACKEND_LOG="/tmp/graph-view-backend.log"
FRONTEND_LOG="/tmp/graph-view-frontend.log"

cleanup() {
  echo
  echo "Encerrando backend e frontend..."
  taskkill //PID "$BACKEND_PID" //T //F >/dev/null 2>&1
  taskkill //PID "$FRONTEND_PID" //T //F >/dev/null 2>&1
  exit 0
}
trap cleanup INT TERM

(cd backend && ./.venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8000) \
  > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!

(cd frontend && npm run dev) > "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!

echo "Backend  -> http://localhost:8000  (log: $BACKEND_LOG)"
echo "Frontend -> http://localhost:5173  (log: $FRONTEND_LOG)"
echo "Ctrl+C para encerrar os dois."

wait "$BACKEND_PID" "$FRONTEND_PID"
