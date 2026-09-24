#!/usr/bin/env bash
# ==============================================================================
# CAA-Lab — Script de Inicialização Automatizada para Ubuntu Linux
# Laboratório Tecnológico Inclusivo (CETAM / Instituto Benjamin Constant)
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================================="
echo "          INICIANDO CAA-LAB (MODO OFFLINE LOCAL)          "
echo "=========================================================="

# 1. Verificar se o arquivo .env existe, caso contrário criar a partir do .env.example
if [ ! -f .env ]; then
    echo "[INFO] Arquivo .env não encontrado. Gerando a partir de .env.example..."
    cp .env.example .env
fi

# Carregar variáveis de ambiente
set -a
# shellcheck source=/dev/null
[ -f .env ] && . .env
set +a

PORT="${PORT:-8000}"
APP_URL="http://localhost:${PORT}"

# 2. Criar diretórios locais essenciais
echo "[INFO] Verificando diretórios locais de persistência..."
mkdir -p data assets/pictograms assets/audio assets/uploads app/static/pictograms

PID_FILE="${PROJECT_DIR}/.caa-lab.pid"

# 3. Preparar ambiente virtual Python local (sem Docker)
echo "[INFO] Verificando ambiente virtual Python local..."
if [ ! -d .venv ]; then
    echo "[INFO] Ambiente virtual .venv não encontrado. Criando..."
    if ! command -v python3 >/dev/null 2>&1; then
        echo "[ERRO] python3 não está instalado no sistema."
        exit 1
    fi
    python3 -m venv .venv
    echo "[INFO] Instalando dependências a partir de requirements.txt..."
    .venv/bin/pip install --upgrade pip
    .venv/bin/pip install -r requirements.txt
fi

if [ ! -f .venv/bin/uvicorn ]; then
    echo "[INFO] Uvicorn não encontrado no .venv. Instalando dependências..."
    .venv/bin/pip install -r requirements.txt
fi

# 4. Gerar pictogramas offline caso não existam
echo "[INFO] Verificando pictogramas..."
.venv/bin/python scripts/generate_pictograms.py || true

# 5. Garantir que nenhum container Docker do projeto esteja ativo ou seja iniciado
if command -v docker >/dev/null 2>&1; then
    if docker compose version >/dev/null 2>&1; then
        docker compose down --remove-orphans >/dev/null 2>&1 || true
    elif command -v docker-compose >/dev/null 2>&1; then
        docker-compose down --remove-orphans >/dev/null 2>&1 || true
    fi
    docker stop caa-lab-app >/dev/null 2>&1 || true
    docker rm caa-lab-app >/dev/null 2>&1 || true
fi

# 6. Iniciar servidor Uvicorn nativo (fora de qualquer container)
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

    echo "[INFO] Iniciando servidor Uvicorn nativo na porta ${PORT}..."
    setsid .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" </dev/null > /tmp/caa-lab.log 2>&1 &
    APP_PID=$!
    echo "$APP_PID" > "$PID_FILE"

    echo "[INFO] Aguardando inicialização e validação de saúde do serviço..."
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

# 7. Abrir a aplicação no navegador padrão
echo "[INFO] Abrindo o CAA-Lab no navegador padrão..."
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
