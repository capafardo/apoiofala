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

# 3. Gerar SVGs caso não existam
if [ -f .venv/bin/python ]; then
    .venv/bin/python scripts/generate_pictograms.py || true
elif command -v python3 >/dev/null 2>&1; then
    python3 scripts/generate_pictograms.py || true
fi

# 4. Verificar se Docker e Docker Compose estão disponíveis
HAS_DOCKER=false
if command -v docker >/dev/null 2>&1; then
    HAS_DOCKER=true
fi

# Modo Docker
if [ "$HAS_DOCKER" = true ]; then
    echo "[INFO] Docker detectado. Subindo containers via Docker Compose..."
    if docker compose version >/dev/null 2>&1; then
        docker compose up -d --build
    elif command -v docker-compose >/dev/null 2>&1; then
        docker-compose up -d --build
    fi

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
        echo "[SUCESSO] CAA-Lab está pronto e operacional em: ${APP_URL}"
    else
        echo "[AVISO] Não foi possível validar o healthcheck no tempo previsto. Verifique com 'docker compose logs'."
    fi

# Modo Fallback Local (caso Docker não esteja em execução)
else
    echo "[INFO] Docker não detectado ou inativo. Iniciando via ambiente Python local..."
    if [ ! -d .venv ]; then
        echo "[INFO] Criando ambiente virtual .venv..."
        python3 -m venv .venv
        .venv/bin/pip install -r requirements.txt
    fi
    echo "[INFO] Iniciando servidor Uvicorn em background..."
    nohup .venv/bin/uvicorn app.main:app --host 0.0.0.0 --port "${PORT}" > /tmp/caa-lab.log 2>&1 &
    sleep 2
fi

# 5. Abrir a aplicação no navegador padrão
echo "[INFO] Abrindo o CAA-Lab no navegador padrão..."
if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "${APP_URL}" >/dev/null 2>&1 &
elif command -v sensible-browser >/dev/null 2>&1; then
    sensible-browser "${APP_URL}" >/dev/null 2>&1 &
fi

echo "=========================================================="
echo " CAA-Lab em execução: ${APP_URL}"
echo " Modo Criança: ${APP_URL}/"
echo " Modo Profissional: ${APP_URL}/profissional"
echo "=========================================================="
