#!/usr/bin/env bash
# ==============================================================================
# ApoioFala — Build do pacote .deb (aplicativo desktop Electron)
#
# Produz: dist/apoiofala_<versão>_amd64.deb
#
# Requisitos na máquina de build (Ubuntu):
#   - python3 (>= 3.11) com suporte a venv
#   - Node.js/npm (para baixar o Electron)
#   - dpkg-deb
#
# Uso:
#   ./desktop/build_deb.sh
#   CAA_VERSION=0.2.0 ./desktop/build_deb.sh   # versão customizada
# ==============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="${CAA_VERSION:-0.1.0}"
ARCH="${CAA_ARCH:-amd64}"
PKG="apoiofala"
DIST="$ROOT/dist"
STAGE="$DIST/${PKG}_${VERSION}_${ARCH}"
APP_DEST="$STAGE/opt/${PKG}"

log() { echo "[build] $*"; }

# ---------------------------------------------------------------------------
# Pré-requisitos
# ---------------------------------------------------------------------------
for cmd in python3 npm dpkg-deb; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "[erro] Comando '$cmd' não encontrado. Instale-o antes de gerar o pacote."
        exit 1
    fi
done

# ---------------------------------------------------------------------------
# Preparação do diretório de staging
# ---------------------------------------------------------------------------
rm -rf "$DIST"
mkdir -p "$APP_DEST" "$STAGE/DEBIAN" \
         "$STAGE/usr/bin" "$STAGE/usr/share/applications" \
         "$STAGE/usr/share/icons/hicolor/scalable/apps"

# ---------------------------------------------------------------------------
# 1. Código Python (backend FastAPI)
# ---------------------------------------------------------------------------
log "Copiando código do backend..."
cp -r "$ROOT/app" "$APP_DEST/app"
cp -r "$ROOT/scripts" "$APP_DEST/scripts"
cp "$ROOT/requirements.txt" "$APP_DEST/"
find "$APP_DEST" -type d -name __pycache__ -prune -exec rm -rf {} +
find "$APP_DEST" -type f -name '*.pyc' -delete

# ---------------------------------------------------------------------------
# 2. Wheelhouse: dependências Python offline (cp312/cp313 + build local)
#    Instalação no destino usa o wheelhouse (sem internet) com fallback online.
# ---------------------------------------------------------------------------
log "Baixando wheels Python (3.12/3.13) para o wheelhouse..."
PYBUILD="$DIST/.venv-build"
python3 -m venv "$PYBUILD"
WHL="$APP_DEST/wheelhouse"
mkdir -p "$WHL"

for PYVER in 3.12 3.13; do
    ABI="cp${PYVER/./}"
    for PLAT in manylinux2014_x86_64 manylinux_2_28_x86_64 manylinux_2_34_x86_64; do
        log "  wheels para Python $PYVER ($PLAT)..."
        if "$PYBUILD/bin/pip" download \
                --dest "$WHL" --only-binary=:all: \
                --implementation cp --python-version "$PYVER" --abi "$ABI" \
                --platform "$PLAT" \
                -r "$ROOT/requirements.txt" >/dev/null 2>&1; then
            break
        fi
    done
done

# Wheels para a versão do Python da máquina de build (uso/teste local)
"$PYBUILD/bin/pip" download --dest "$WHL" --only-binary=:all: \
    -r "$ROOT/requirements.txt" >/dev/null 2>&1 || true

# ---------------------------------------------------------------------------
# 3. Shell Electron (janela nativa)
# ---------------------------------------------------------------------------
log "Instalando Electron (download ~120 MB na primeira vez)..."
(cd "$ROOT/desktop/electron" && npm install --no-audit --no-fund --save-dev electron)

mkdir -p "$APP_DEST/electron"
cp -a "$ROOT/desktop/electron/node_modules/electron/dist/." "$APP_DEST/electron/"
# Renomeia o binário para 'apoiofala' (define o WM_CLASS usado pelo .desktop)
mv "$APP_DEST/electron/electron" "$APP_DEST/electron/apoiofala"
cp "$ROOT/desktop/electron/main.js" "$ROOT/desktop/electron/package.json" \
   "$APP_DEST/electron/"

# ---------------------------------------------------------------------------
# 4. Integração com o sistema (launcher, menu, ícone)
# ---------------------------------------------------------------------------
install -m 755 "$ROOT/desktop/deb/apoiofala-launcher" "$STAGE/usr/bin/apoiofala"
install -m 644 "$ROOT/desktop/deb/apoiofala.desktop" \
    "$STAGE/usr/share/applications/apoiofala.desktop"
install -m 644 "$ROOT/desktop/deb/apoiofala.svg" \
    "$STAGE/usr/share/icons/hicolor/scalable/apps/apoiofala.svg"

# ---------------------------------------------------------------------------
# 5. Scripts de manutenção do pacote (DEBIAN/)
# ---------------------------------------------------------------------------
install -m 755 "$ROOT/desktop/deb/postinst" "$STAGE/DEBIAN/postinst"
install -m 755 "$ROOT/desktop/deb/prerm"   "$STAGE/DEBIAN/prerm"

INSTALLED_SIZE="$(du -sk "$APP_DEST" | cut -f1)"
sed -e "s/__VERSION__/$VERSION/" \
    -e "s/__INSTALLED_SIZE__/$INSTALLED_SIZE/" \
    "$ROOT/desktop/deb/control" > "$STAGE/DEBIAN/control"
# Garantir nova linha final (exigida pelo dpkg-deb)
printf '\n' >> "$STAGE/DEBIAN/control"

# ---------------------------------------------------------------------------
# 6. Empacotar
# ---------------------------------------------------------------------------
log "Gerando pacote .deb..."
dpkg-deb --build --root-owner-group "$STAGE" "$DIST/${PKG}_${VERSION}_${ARCH}.deb" >/dev/null

log "Concluído: $DIST/${PKG}_${VERSION}_${ARCH}.deb"
log "Instale com: sudo dpkg -i $DIST/${PKG}_${VERSION}_${ARCH}.deb"
log "Dependências apt: sudo apt install -f"