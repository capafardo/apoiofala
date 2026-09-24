# Operação e Implantação - CAA-Lab

## 1. Inicialização Rápida (Execução Local Nativa / Sem Docker)

Para iniciar a aplicação em qualquer estação Ubuntu (sem uso de Docker):

```bash
./iniciar.sh
```

O script cuidará de:
1. Configurar o arquivo de variáveis de ambiente (`.env`);
2. Criar os diretórios locais necessários (`data/`, `assets/`);
3. Preparar o ambiente virtual Python local (`.venv`) e instalar dependências;
4. Gerar os pictogramas essenciais caso necessário;
5. Garantir que nenhum container Docker do projeto esteja ativo ou configurado para inicialização;
6. Subir o servidor Uvicorn nativo em segundo plano e validar o healthcheck (`/health`);
7. Abrir a interface web no navegador padrão da estação (`xdg-open`).

Para encerrar o servidor:

```bash
./parar.sh
```

## 2. Execução em Ambiente de Desenvolvimento

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

## 3. Voz do Sistema (TTS)

A síntese de voz do backend usa, por padrão, a **voz neural da Microsoft**
(pt-BR natural, ex.: *Francisca*), via biblioteca `edge-tts` — gratuita e sem
chave de API. As respostas ficam em cache em `assets/audio/tts-cache/` para
reprodução instantânea em repetições.

Cascata de motores (padrão `TTS_ENGINE=auto`):

1. **edge-neural** — voz natural da Microsoft (requer internet no primeiro uso;
   depois, servido pelo cache local);
2. **espeak-ng** — voz robotizada, 100% offline, usada automaticamente se não
   houver conectividade ou via `engine=espeak` na requisição.

Em ambientes **sem internet**, defina `TTS_ENGINE=espeak` no `.env` (ou passe
`engine=espeak` na chamada) para manter o áudio integralmente local.
