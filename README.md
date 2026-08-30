# CAA-Lab — Aplicação Web de Comunicação Aumentativa e Alternativa

**Laboratório Tecnológico Inclusivo** | CETAM / Instituto Benjamin Constant

O **CAA-Lab** é uma plataforma web local e inclusiva voltada para apoio à Comunicação Aumentativa e Alternativa (CAA) de crianças e jovens com transtornos do neurodesenvolvimento (como TEA).

---

## 🌟 Principais Características

- **100% Offline e Local:** Projetado para operar em rede local fechada sem necessidade de conexão externa à Internet.
- **Dois Modos Distintos:**
  - **Modo Criança:** Prancha de comunicação visual com botões grandes, categorias intuitivas, construtor de frases ("Minha Mensagem") e síntese de voz (TTS).
  - **Modo Profissional:** Gestão de vocabulário, personalização de tamanho e contraste dos símbolos, e métricas técnicas respeitosas à privacidade.
- **Acessibilidade Nativa:** Suporte total a toque, teclado, alto contraste e leitores de tela.
- **Privacidade e LGPD:** Princípio de minimização de dados, armazenamento 100% local e ausência de telemetria externa.

---

## 🚀 Como Iniciar

### Modo Rápido (Ubuntu Linux)

```bash
chmod +x iniciar.sh
./iniciar.sh
```

### Com Docker Compose

```bash
docker compose up -d
```

Acesse no navegador: `http://localhost:8000`

### Ambiente de Desenvolvimento

```bash
# Criar ambiente virtual e instalar dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Executar servidor
uvicorn app.main:app --reload --port 8000

# Executar testes
pytest
```

---

## 📚 Documentação Técnica

Consulte a pasta [`docs/`](docs/README.md) para especificações completas:
- [Arquitetura](docs/arquitetura.md)
- [Requisitos](docs/requisitos.md)
- [Banco de Dados](docs/banco-de-dados.md)
- [API REST](docs/api.md)
- [Acessibilidade](docs/acessibilidade.md)
- [Segurança & LGPD](docs/seguranca.md)
- [Homologação](docs/homologacao.md)
