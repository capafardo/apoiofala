# Operação e Implantação - CAA-Lab

## 1. Instalação Inicial (1x com internet)

Para configurar a estação de trabalho após clonar o repositório:

```bash
chmod +x instalar.sh iniciar.sh parar.sh
./instalar.sh
```

O script cuidará de:
1. Verificar dependências de sistema (`python3`, `python3-venv`, `espeak-ng`);
2. Criar os diretórios locais necessários (`data/`, `assets/`);
3. Preparar o ambiente virtual Python local (`.venv`) e instalar dependências;
4. Gerar a biblioteca de pictogramas vetoriais locais (SVGs);
5. Inicializar o banco de dados SQLite local (`caa_lab.db`) com as migrações;
6. Pré-aquecer o cache de áudio TTS de todos os símbolos e frases padrão.

## 2. Execução Diária (100% Offline / Sem Internet / Sem Docker)

Para iniciar a aplicação no dia a dia:

```bash
./iniciar.sh
```

O script inicia o servidor Uvicorn nativo em segundo plano e abre o navegador padrão automaticamente.

Para encerrar o servidor:

```bash
./parar.sh
```

## 3. Execução em Ambiente de Desenvolvimento

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

## 4. Voz do Sistema (TTS Offline-First)

A síntese de voz do backend opera em arquitetura híbrida de alto desempenho:
* **Cache Local em Disco (`assets/audio/tts-cache/`):** Durante o `./instalar.sh`, os áudios neurais dos símbolos e frases padrão já são pré-sintetizados e armazenados em disco. Na reprodução diária offline, são servidos instantaneamente (<5ms).
* **Circuit Breaker Automático:** Se uma palavra inédita for falada sem internet, o backend detecta a ausência de rede sem travamentos e chaveia imediatamente (<20ms) para o motor local **espeak-ng** ou Web Speech API.
* **Modo Offline Estrito:** Em estações isoladas por política de segurança, basta definir no `.env`:
  ```ini
  TTS_OFFLINE_MODE=true
  ```
  Neste modo, nenhuma requisição externa de áudio jamais é tentada.
