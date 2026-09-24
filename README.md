# CAA-Lab — Aplicação Web de Comunicação Aumentativa e Alternativa

**Laboratório Tecnológico Inclusivo** | CETAM / Instituto Benjamin Constant  
*Tecnologia como ponte para a expressão, autonomia e inclusão social.*

---

## 📋 Sumário

- [Visão Geral e Propósito](#-visão-geral-e-propósito)
- [Principais Funcionalidades](#-principais-funcionalidades)
  - [Modo Criança (Prancha de Comunicação)](#1-modo-criança-prancha-de-comunicação)
  - [Modo Profissional (Administração & Personalização)](#2-modo-profissional-administração--personalização)
- [Arquitetura & Stack Tecnológica](#-arquitetura--stack-tecnológica)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Como Executar a Aplicação](#-como-executar-a-aplicação)
  - [Opção 1: Inicialização Automática no Ubuntu Linux](#opção-1-inicialização-automática-no-ubuntu-linux-recomendado)
  - [Opção 2: Com Docker Compose](#opção-2-com-docker-compose)
  - [Opção 3: Ambiente de Desenvolvimento Local (Python)](#opção-3-ambiente-de-desenvolvimento-local-python)
  - [Opção 4: Aplicativo Desktop (.deb) — ApoioFala](#opção-4-aplicativo-desktop-deb--apoiofala)
- [Catálogo de Testes Automatizados](#-catálogo-de-testes-automatizados)
- [Conformidade com a LGPD e Segurança](#-conformidade-com-a-lgpd-e-segurança)
- [Documentação Técnica Completa](#-documentação-técnica-completa)

---

## 🌟 Visão Geral e Propósito

O **CAA-Lab** é uma aplicação web local de apoio à **Comunicação Aumentativa e Alternativa (CAA)** desenvolvida especificamente para apoiar crianças e jovens com dificuldades de fala ou transtornos do neurodesenvolvimento (como o Transtorno do Espectro Autista - TEA).

### Princípios Fundamentais:
1. **100% Offline-First:** Opera integralmente em rede local fechada, sem requisições externas para CDNs, fontes do Google ou APIs em nuvem.
2. **Acessibilidade Universal:** Controles táteis amplos, navegação por teclado, temas de Alto Contraste e retorno sonoro imediato.
3. **Privacidade e Minimização de Dados (LGPD):** Nenhum dado pessoal sensível ou conversas privadas de crianças saem da máquina/servidor local.
4. **Comunicação sem Bloqueios (Fail-Safe):** A interface básica funciona independentemente de qualquer serviço de IA ou infraestrutura externa.

---

## 🚀 Principais Funcionalidades

### 1. Modo Criança (Prancha de Comunicação)
* **Navegação Intuitiva por Categorias:** Categorias temáticas (*Início, Comunicar, Frases rápidas, Sentimentos, Necessidades, Comida e bebida, Pessoas, Lugares, Brincar, Mais*).
* **Biblioteca Vetorial com mais de 80 Símbolos SVG:** Imagens nítidas e coloridas com rótulos em texto de fácil leitura.
* **Construtor de Mensagens ("Minha Mensagem"):** Montagem sequencial de frases (`[eu] + [quero] + [água]`), exibição em texto natural formatado (*"Eu quero água."*) e remoção de itens individuais com 1 clique.
* **Síntese de Voz Integrada (TTS):** Reprodução instantânea com **voz neural da Microsoft** (pt-BR, gratuita via edge-tts, sem chave de API) e velocidade configurável; fallback offline garantido.
* **Frases Rápidas:** Acesso a pedidos e expressões frequentes com reprodução sonora imediata em 1 toque.
* **Seletor de Perfil na Barra Superior:** Permite alternar instantaneamente entre perfis cadastrados, carregando a prancha e preferências de cada criança.
* **Acessibilidade Rápida:** Botões *A-* e *A+* para ajuste dinâmico do tamanho dos cartões e botão de alternância para *Alto Contraste*.

### 2. Modo Profissional (Administração & Personalização)
* **Personalização de Pranchas via Arrastar e Soltar (Drag-and-Drop):**
  * O terapeuta visualiza a **Biblioteca Global de Símbolos** com busca instantânea.
  * Pode selecionar um ou vários símbolos simultaneamente e **arrastá-los e soltá-los na prancha da categoria desejada**.
  * A configuração da prancha fica salva individualmente no perfil daquela criança.
* **Gerenciamento de Perfis com Apelidos:**
  * Cadastro de novos perfis informando o **Apelido da Criança** (ex: *Joãozinho, Clarinha*) e o **Apelido da Mãe ou Acompanhante** (ex: *Mãe Ana, Tia Carla*).
  * Ajuste individual de tamanho dos símbolos (*Pequeno, Médio, Grande*), quantidade de itens por página (*6, 12, 20*) e velocidade da fala.
* **Painel de Métricas Técnicas Não-Invasivas:**
  * Estatísticas gerais (número de toques, categorias mais acessadas, frases frequentes) sem gravar conteúdo conversacional sensível.

---

## 🛠️ Arquitetura & Stack Tecnológica

* **Backend:** Python 3.11+ com **FastAPI**, **SQLAlchemy 2.0** e **Pydantic v2**.
* **Banco de Dados:** SQLite com modo WAL (*Write-Ahead Logging*) e integridade relacional de chaves estrangeiras ativada.
* **Frontend:** HTML5 Semântico, CSS3 Moderno com variáveis nativas para Alto Contraste e JavaScript Modular (ES Modules) nativo sem necessidade de compilação em runtime.
* **Síntese de Voz (TTS):** Abstração `SpeechService` com provedor cliente via Web Speech API (zero latência) e backend com **voz neural Microsoft (edge-tts, gratuita)** com cache em disco e fallback espeak-ng offline.
* **Execução Nativa:** Execução direta no sistema operacional via scripts Bash (`./instalar.sh`, `./iniciar.sh`, `./parar.sh`), sem necessidade de Docker.

---

## 📁 Estrutura do Projeto

```text
apoio-fala/
├── app/
│   ├── api/                 # Endpoints REST (/auth, /symbols, /profiles, etc.)
│   ├── core/                # Configurações, segurança, database e seed inicial
│   ├── models/              # Modelos SQLAlchemy (User, Profile, Category, Symbol, etc.)
│   ├── schemas/             # Validação e serialização Pydantic
│   ├── services/            # Serviços de negócio e SpeechService
│   ├── static/              # CSS, JS modular e SVGs vetoriais locais
│   └── templates/           # Templates HTML (index.html, profissional.html)
├── assets/                  # Volumes persistentes de pictogramas e áudio
├── data/                    # Volume do banco de dados SQLite persistente
├── desktop/                 # Versão desktop (.deb): shell Electron + empacotamento
│   ├── electron/            #   Shell Electron (janela própria, backend embutido)
│   ├── deb/                 #   Arquivos do pacote (control, postinst, ícone, .desktop)
│   └── build_deb.sh         #   Script de build do pacote .deb
├── dist/                    # Pacote .deb gerado (ignorado pelo git)
├── docs/                    # Documentação técnica detalhada
├── scripts/                 # Scripts auxiliares (geração de SVGs offline, pré-cache TTS)
├── tests/                   # Testes automatizados (Unitários e Integração)
├── instalar.sh              # Script de instalação e configuração inicial (1x com internet)
├── iniciar.sh               # Script de inicialização automática (100% offline)
├── parar.sh                 # Script para encerrar a aplicação local
└── requirements.txt         # Dependências do Python
```

---

## 💻 Como Instalar e Executar a Aplicação (100% Offline)

A aplicação foi projetada para rodar **diretamente no sistema operacional** (sem Docker), operando com banco de dados local SQLite, assets vetoriais locais e síntese de voz com cache em disco e fallback para `espeak-ng`.

### Passo 1: Instalação Inicial (Executado 1 única vez, com internet)

Após clonar o repositório, execute o script de instalação para configurar o ambiente virtual, dependências, banco local e pré-gerar os áudios e pictogramas:

```bash
chmod +x instalar.sh iniciar.sh parar.sh
./instalar.sh
```

O script `instalar.sh` automaticamente:
1. Verifica dependências de sistema (`python3`, `python3-venv`, `espeak-ng`);
2. Cria o ambiente virtual `.venv` e instala as bibliotecas Python;
3. Gera os arquivos de banco de dados SQLite (`./data/caa_lab.db`) e migrações;
4. Gera e valida os mais de 80 pictogramas vetoriais locais;
5. Pré-aquece o cache de áudio das expressões padrão para disponibilidade offline imediata.

---

### Passo 2: Execução no Dia a Dia (100% Offline, sem internet)

Com a instalação concluída, a máquina pode ser desconectada da internet e a aplicação iniciada a qualquer momento:

```bash
./iniciar.sh
```

O script inicia o backend localmente e abre o navegador padrão automaticamente em `http://localhost:8000`.

**Para encerrar o serviço:**
```bash
./parar.sh
```

---

### Opção 2: Desenvolvimento Local Manual

Se preferir rodar em modo de desenvolvimento com live reload:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

---

### Opção 4: Aplicativo Desktop (.deb) — ApoioFala

Uma versão **desktop instalável** (`.deb`) chamada **ApoioFala**, que abre a prancha em **janela própria** (sem navegador), com o backend FastAPI embutido e dados persistentes **por usuário** em `~/.local/share/apoiofala/`.

**Características:**
* Janela nativa (Electron/Chromium) sem barra de endereço nem abas — ideal para uso por crianças;
* `F11` alterna tela cheia; modo quiosque via `CAA_KIOSK=1` (sair com `Ctrl+Shift+X`);
* Síntese de voz robusta: Web Speech API (latência zero) com **fallback automático para o backend** — voz neural da Microsoft (edge-tts, pt-BR natural, cache local) e, sem internet, espeak-ng offline — o som funciona em qualquer cenário;
* Instalação 100% offline (dependências Python embarcadas no pacote);
* Backend instalado em `/opt/apoiofala`; dados de cada usuário em `~/.local/share/apoiofala`;
* Atalho no menu de aplicativos com ícone próprio.

**Gerar o pacote (na máquina de build, com npm e dpkg-deb instalados):**

```bash
./desktop/build_deb.sh
# Saída: dist/apoiofala_0.1.0_amd64.deb
```

**Instalar no Ubuntu:**

```bash
sudo dpkg -i dist/apoiofala_0.1.0_amd64.deb
sudo apt install -f   # garante dependências apt (speech-dispatcher, espeak-ng, etc.)
```

> Se você instalou uma versão anterior com o nome `caa-lab`, remova-a antes:
> `sudo apt remove caa-lab`

Depois é só procurar **ApoioFala** no menu de aplicativos ou executar `apoiofala` no terminal. Para desinstalar: `sudo apt remove apoiofala` (os dados dos usuários em `~/.local/share/apoiofala` são preservados).

---

## 🧪 Catálogo de Testes Automatizados

A aplicação conta com **28 testes automatizados** cobrindo autenticação, integridade do banco, categorias, personalização de pranchas por drag-and-drop, métricas e rotas web.

Para executar todos os testes:

```bash
.venv/bin/pytest
```

---

## 🛡️ Conformidade com a LGPD e Segurança

* **Armazenamento 100% Local:** Nenhum dado sai da rede interna da instituição.
* **Nota sobre TTS neural:** para voz natural (Microsoft/edge-tts) o texto é enviado ao serviço gratuito da Microsoft; em ambientes **sem internet**, defina `TTS_ENGINE=espeak` (ou `engine=espeak` na requisição) para manter o áudio 100% local.
* **Criptografia Forte:** Senhas armazenadas com hash `bcrypt` (fator de custo 12).
* **Minimização de Dados:** Mensagens privadas da criança não são salvas em bancos de logs ou telemetria.
* **Segurança HTTP:** Headers de segurança configurados nativamente (`X-Frame-Options`, `X-Content-Type-Options`, etc.).

---

## 📚 Documentação Técnica Completa

Para aprofundamento técnico, consulte os documentos na pasta [`docs/`](docs/README.md):

* [Arquitetura do Sistema](docs/arquitetura.md)
* [Requisitos Funcionais e Não-Funcionais](docs/requisitos.md)
* [Modelagem e Banco de Dados](docs/banco-de-dados.md)
* [Especificação da API REST](docs/api.md)
* [Acessibilidade e Usabilidade](docs/acessibilidade.md)
* [Segurança e Privacidade (LGPD)](docs/seguranca.md)
* [Estratégia e Catálogo de Testes](docs/testes.md)
* [Registro de Homologação](docs/homologacao.md)
* [Operação e Implantação](docs/operacao.md)
* [Decisões Arquiteturais (ADRs)](docs/decisoes/)
