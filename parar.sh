#!/usr/bin/env bash
# ==============================================================================
# CAA-Lab — Script para Encerrar o Servidor Local
# Laboratório Tecnológico Inclusivo (CETAM / Instituto Benjamin Constant)
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

PID_FILE="${PROJECT_DIR}/.caa-lab.pid"
STOPPED=false

# 1. Encerrar pelo arquivo PID, se existir
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE" 2>/dev/null || true)
    if [ -n "$PID" ] && kill -0 "$PID" 2>/dev/null; then
        echo "[INFO] Encerrando processo CAA-Lab (PID: $PID)..."
        kill "$PID" 2>/dev/null || true
        STOPPED=true
    fi
    rm -f "$PID_FILE"
fi

# 2. Encerrar qualquer processo uvicorn associado a este projeto
PIDS=$(pgrep -f "uvicorn app.main:app" 2>/dev/null || true)
if [ -n "$PIDS" ]; then
    echo "[INFO] Encerrando processos Uvicorn ativos ($PIDS)..."
    # shellcheck disable=SC2086
    kill $PIDS 2>/dev/null || true
    STOPPED=true
fi

if [ "$STOPPED" = true ]; then
    echo "[SUCESSO] Servidor CAA-Lab finalizado com sucesso."
else
    echo "[INFO] Nenhum servidor CAA-Lab em execução encontrado."
fi
