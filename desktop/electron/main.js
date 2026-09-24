/**
 * ApoioFala — Shell Desktop (Electron)
 *
 * Responsabilidades:
 *  1. Iniciar o backend FastAPI (uvicorn) localmente em 127.0.0.1;
 *  2. Abrir a interface web em uma janela própria (sem barra de navegador);
 *  3. Gerenciar o ciclo de vida: encerra o backend ao fechar a janela.
 *
 * Dados persistentes por usuário: ~/.local/share/apoiofala/
 * (configurável via variável de ambiente CAA_DATA_DIR).
 */

const { app, BrowserWindow, dialog, globalShortcut } = require('electron');

// Permite reprodução de áudio (TTS do backend) sem gesto do usuário —
// importante no modo quiosque/tela cheia usado por crianças.
app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');

// ============================================================
// Configuração (valores padrão para a instalação empacotada)
// ============================================================
const BACKEND_DIR = process.env.CAA_BACKEND_DIR || '/opt/apoiofala';
const UVICORN = process.env.CAA_UVICORN || path.join(BACKEND_DIR, 'venv', 'bin', 'uvicorn');
const HOST = process.env.CAA_HOST || '127.0.0.1';
const PORT = parseInt(process.env.CAA_PORT || '8000', 10);
const DATA_ROOT = process.env.CAA_DATA_DIR || path.join(os.homedir(), '.local', 'share', 'apoiofala');
const KIOSK = process.env.CAA_KIOSK === '1';
const BACKEND_TIMEOUT_MS = 60000;

let backendProcess = null;
let mainWindow = null;

// ============================================================
// Diretórios de dados do usuário (perfil, banco, uploads)
// ============================================================
function ensureDataDirs() {
  const dataDir = path.join(DATA_ROOT, 'data');
  const assetsDir = path.join(DATA_ROOT, 'assets');
  const subdirs = [
    dataDir,
    path.join(assetsDir, 'pictograms'),
    path.join(assetsDir, 'audio'),
    path.join(assetsDir, 'uploads'),
  ];
  for (const dir of subdirs) {
    fs.mkdirSync(dir, { recursive: true });
  }

  // Chave secreta persistente por usuário (gerada na primeira execução)
  const secretFile = path.join(dataDir, '.secret');
  let secret = '';
  try {
    secret = fs.readFileSync(secretFile, 'utf8').trim();
  } catch (_) {
    /* arquivo ainda não existe */
  }
  if (!secret) {
    secret = crypto.randomBytes(32).toString('hex');
    fs.writeFileSync(secretFile, secret, { mode: 0o600 });
  }

  return { dataDir, assetsDir, secret };
}

// ============================================================
// Backend (FastAPI / uvicorn)
// ============================================================
function isHealthy() {
  return new Promise((resolve) => {
    const req = http.get({ host: HOST, port: PORT, path: '/health', timeout: 1500 }, (res) => {
      res.resume();
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.on('timeout', () => {
      req.destroy();
      resolve(false);
    });
  });
}

async function waitHealthy(timeoutMs = BACKEND_TIMEOUT_MS) {
  const start = Date.now();
  while (Date.now() - start < timeoutMs) {
    if (await isHealthy()) return true;
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  return false;
}

async function ensureBackend() {
  // Já existe um backend saudável (instância anterior): reaproveita.
  if (await isHealthy()) return true;

  const { dataDir, assetsDir, secret } = ensureDataDirs();

  const env = {
    ...process.env,
    APP_NAME: 'ApoioFala',
    APP_ENV: 'production',
    DEBUG: 'false',
    HOST,
    PORT: String(PORT),
    DATABASE_URL: `sqlite:///${path.join(dataDir, 'caa_lab.db')}`,
    DATA_DIR: dataDir,
    ASSETS_DIR: assetsDir,
    SECRET_KEY: secret,
  };

  backendProcess = spawn(
    UVICORN,
    ['app.main:app', '--app-dir', BACKEND_DIR, '--host', HOST, '--port', String(PORT)],
    { cwd: BACKEND_DIR, env, stdio: ['ignore', 'pipe', 'pipe'] }
  );

  backendProcess.stdout.on('data', (d) => process.stdout.write(`[backend] ${d}`));
  backendProcess.stderr.on('data', (d) => process.stderr.write(`[backend] ${d}`));
  backendProcess.on('exit', (code, signal) => {
    console.log(`[backend] encerrado (code=${code}, signal=${signal})`);
    backendProcess = null;
  });

  return waitHealthy();
}

// ============================================================
// Janela principal
// ============================================================
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    show: false,
    autoHideMenuBar: true,
    title: 'ApoioFala',
    backgroundColor: '#0f172a',
    webPreferences: {
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
    },
  });

  mainWindow.loadURL(`http://${HOST}:${PORT}/`);

  mainWindow.once('ready-to-show', () => {
    mainWindow.maximize();
    mainWindow.show();
    if (KIOSK) mainWindow.setKiosk(true);
  });

  // Bloqueia navegação para fora da aplicação local
  mainWindow.webContents.on('will-navigate', (event, url) => {
    if (!url.startsWith(`http://${HOST}:${PORT}`)) event.preventDefault();
  });

  // Bloqueia abertura de janelas externas (pop-ups)
  mainWindow.webContents.setWindowOpenHandler(() => ({ action: 'deny' }));

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// ============================================================
// Ciclo de vida do Electron
// ============================================================
const gotLock = app.requestSingleInstanceLock();

if (!gotLock) {
  // Outra instância já está em execução: foca a janela existente e sai.
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  app.whenReady().then(async () => {
    const backendOk = await ensureBackend();
    if (!backendOk) {
      dialog.showErrorBox(
        'ApoioFala',
        'Não foi possível iniciar o serviço local do ApoioFala.\n\n' +
          `Verifique se o backend foi instalado corretamente (${BACKEND_DIR}) e tente novamente.`
      );
      app.quit();
      return;
    }
    createWindow();

    // Atalhos
    if (!KIOSK) {
      globalShortcut.register('F11', () => {
        if (mainWindow) mainWindow.setFullScreen(!mainWindow.isFullScreen());
      });
    }
    // Em modo quiosque, Ctrl+Shift+X encerra (acesso do supervisor)
    if (KIOSK) {
      globalShortcut.register('Control+Shift+X', () => app.quit());
    }
  });

  app.on('window-all-closed', () => app.quit());
}

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});

app.on('before-quit', () => {
  if (backendProcess) {
    backendProcess.kill('SIGTERM');
  }
});