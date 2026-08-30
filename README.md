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
* **Síntese de Voz Integrada (TTS Local):** Reprodução instantânea por voz em português (pt-BR) com velocidade configurável.
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
* **Síntese de Voz (TTS):** Abstração `SpeechService` com provedor cliente via Web Speech API (zero latência e suporte nativo a pt-BR).
* **Containerização:** Docker e Docker Compose com volumes de dados persistentes.

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
├── docs/                    # Documentação técnica detalhada
├── scripts/                 # Scripts auxiliares (geração de SVGs offline)
├── tests/                   # Testes automatizados (Unitários e Integração)
├── docker-compose.yml       # Orquestração de containers
├── Dockerfile               # Imagem Docker slim
├── iniciar.sh               # Script mestre de inicialização automática no Ubuntu
└── requirements.txt         # Dependências do Python
```

---

## 💻 Como Executar a Aplicação

### Opção 1: Inicialização Automática no Ubuntu Linux (Recomendado)

O script `iniciar.sh` detecta o ambiente, configura o arquivo `.env`, valida dependências, sobe o serviço e abre o navegador automaticamente via `xdg-open`:

```bash
chmod +x iniciar.sh
./iniciar.sh
```

---

### Opção 2: Com Docker Compose

```bash
# Iniciar container em segundo plano
docker compose up -d

# Verificar logs
docker compose logs -f

# Acessar a aplicação
# Modo Criança: http://localhost:8000
# Modo Profissional: http://localhost:8000/profissional
```

---

### Opção 3: Ambiente de Desenvolvimento Local (Python)

```bash
# 1. Criar e ativar o ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Executar o servidor Uvicorn
uvicorn app.main:app --reload --port 8000
```

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
