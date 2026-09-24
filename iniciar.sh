#!/usr/bin/env bash
# ==============================================================================
# CAA-Lab — Script de Inicialização (Uso Diário 100% Offline)
# Laboratório Tecnológico Inclusivo (CETAM / Instituto Benjamin Constant)
# ==============================================================================
# Inicia a aplicação localmente sem depender de Docker ou conexão à internet.
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================================="
echo "          INICIANDO CAA-LAB (MODO OFFLINE LOCAL)          "
echo "=========================================================="

# 1. Verificar se o ambiente foi instalado
if [ ! -d .venv ] || [ ! -f .venv/bin/uvicorn ]; then
    echo "[ERRO] Ambiente virtual não configurado."
    echo "       Por favor, execute o script de instalação primeiro:"
    echo "       ./instalar.sh"
    exit 1
fi

# 2. Carregar variáveis de ambiente locais
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "[INFO] Arquivo .env não encontrado. Gerando a partir de .env.example..."
        cp .env.example .env
    fi
fi

set -a
# shellcheck source=/dev/null
[ -f .env ] && . .env
set +a

PORT="${PORT:-8000}"
APP_URL="http://localhost:${PORT}"
PID_FILE="${PROJECT_DIR}/.caa-lab.pid"

# 3. Garantir diretórios locais essenciais
mkdir -p data assets/audio/tts-cache assets/pictograms assets/uploads app/static/pictograms

# 4. Iniciar servidor Uvicorn nativo (100% offline)
if curl -s -f "http://localhost:${PORT}/health" >/dev/null 2>&1; then
    echo "[INFO] CAA-Lab já está em execução e respondendo em: ${APP_URL}"
else
    # Limpar processo anterior caso PID registrado esteja inativo
    if [ -f "$PID_FILE" ]; then
        OLD_PID=$(cat "$PID_FILE" 2>/dev/null || true)
        if [ -n "$OLD_PID" ] && kill -0 "$OLD_PID" 2>/dev/null; then
            kill "$OLD_PID" 2>/dev/null || true
            sleep 1
        fi
        rm -f "$PID_FILE"
    fi

    echo "[INFO] Iniciando servidor local na porta ${PORT}..."
    setsid .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port "${PORT}" </dev/null > /tmp/caa-lab.log 2>&1 &
    APP_PID=$!
    echo "$APP_PID" > "$PID_FILE"

    echo "[INFO] Aguardando validação do serviço local..."
    MAX_ATTEMPTS=20
    ATTEMPT=0
    HEALTHY=false

    while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
        if curl -s -f "http://localhost:${PORT}/health" >/dev/null 2>&1; then
            HEALTHY=true
            break
        fi
        sleep 1
        ATTEMPT=$((ATTEMPT + 1))
    done

    if [ "$HEALTHY" = true ]; then
        echo "[SUCESSO] CAA-Lab está pronto e operacional em: ${APP_URL} (PID: ${APP_PID})"
    else
        echo "[AVISO] Não foi possível validar o healthcheck no tempo previsto. Verifique os logs em /tmp/caa-lab.log."
    fi
fi

# 5. Abrir a aplicação no navegador padrão
echo "[INFO] Abrindo o CAA-Lab no navegador..."
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${APP_URL}" >/dev/null 2>&1 &
elif command -v sensible-browser >/dev/null 2>&1; then
    sensible-browser "${APP_URL}" >/dev/null 2>&1 &
fi

echo "=========================================================="
echo " CAA-Lab em execução local: ${APP_URL}"
echo " Modo Criança: ${APP_URL}/"
echo " Modo Profissional: ${APP_URL}/profissional"
echo " Logs: /tmp/caa-lab.log"
echo " Para encerrar: ./parar.sh"
echo "=========================================================="
