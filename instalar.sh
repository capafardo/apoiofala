#!/usr/bin/env bash
# ==============================================================================
# CAA-Lab — Script de Instalação e Preparação (Executado 1x com Internet)
# Laboratório Tecnológico Inclusivo (CETAM / Instituto Benjamin Constant)
# ==============================================================================
# Este script configura o ambiente local para que a aplicação possa ser
# utilizada posteriormente de forma 100% OFFLINE, sem depender de Docker
# ou de qualquer conexão com a internet.
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "=========================================================="
echo "    CAA-LAB — INSTALAÇÃO E CONFIGURAÇÃO OFFLINE NATIVA    "
echo "=========================================================="

# 1. Verificar dependências básicas do sistema operacional
echo "[1/7] Verificando dependências do sistema..."
if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERRO] python3 não está instalado no sistema. Instale com: sudo apt update && sudo apt install -y python3 python3-venv"
    exit 1
fi

if ! command -v espeak-ng >/dev/null 2>&1 && ! command -v espeak >/dev/null 2>&1; then
    echo "[AVISO] 'espeak-ng' não encontrado no sistema operacional."
    echo "        Para garantir síntese de fala 100% offline no Linux, instale:"
    echo "        sudo apt install -y espeak-ng"
else
    echo "[OK] Sintetizador espeak-ng detectado no sistema."
fi

# 2. Criar diretórios locais essenciais
echo "[2/7] Criando diretórios locais de persistência..."
mkdir -p data assets/audio/tts-cache assets/pictograms assets/uploads app/static/pictograms

# 3. Configurar arquivo de variáveis de ambiente .env
echo "[3/7] Verificando arquivo de configuração .env..."
if [ ! -f .env ]; then
    echo "[INFO] Gerando .env a partir de .env.example..."
    cp .env.example .env
fi

# 4. Criar e configurar o ambiente virtual Python (.venv)
echo "[4/7] Configurando ambiente virtual Python (.venv)..."
if [ ! -d .venv ]; then
    echo "[INFO] Criando ambiente virtual em .venv..."
    python3 -m venv .venv
fi

echo "[INFO] Instalando dependências a partir de requirements.txt..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# 5. Gerar todos os pictogramas vetoriais locais (SVGs)
echo "[5/7] Gerando e verificando biblioteca vetorial de pictogramas..."
.venv/bin/python scripts/generate_pictograms.py

# 6. Inicializar o banco de dados SQLite local
echo "[6/7] Inicializando banco de dados SQLite local e migrações..."
.venv/bin/python -c "from app.core.init_db import init_db; init_db()"

# 7. Pré-aquecer cache de áudio TTS das palavras e frases padrão
echo "[7/7] Pré-aquecendo cache de áudio para uso offline..."
.venv/bin/python scripts/precache_audio.py || true

# Garantir permissão de execução nos scripts de controle
chmod +x iniciar.sh parar.sh instalar.sh

echo ""
echo "=========================================================="
echo "    INSTALAÇÃO DO CAA-LAB CONCLUÍDA COM SUCESSO!         "
echo "=========================================================="
echo " A aplicação está configurada para operar 100% OFFLINE."
echo " Não é necessário Docker nem conexão com a internet."
echo ""
echo " Para iniciar a aplicação no dia a dia:"
echo "   ./iniciar.sh"
echo ""
echo " Para encerrar a aplicação:"
echo "   ./parar.sh"
echo "=========================================================="
