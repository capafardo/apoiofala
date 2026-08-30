# ADR-001: Definição da Arquitetura Base e Stack Inicial

## Status
Aceito

## Contexto
O CAA-Lab necessita operar em estações de trabalho e servidores com Ubuntu Linux em ambiente fechado de rede local (sem internet em tempo de execução no modo criança), atendendo a crianças e jovens com necessidades de comunicação aumentativa.

## Decisão
1. **Backend:** FastAPI (Python 3.11+) com SQLAlchemy e Pydantic v2. Fornece alto desempenho, tipagem robusta e baixa sobrecarga.
2. **Frontend:** HTML5 semântico, CSS3 com variáveis nativas e JavaScript modular. Elimina ferramentas pesadas de build que possam falhar em redes desconectadas e permite suporte a Alto Contraste nativo.
3. **Síntese de Voz:** Web Speech API nativa no cliente + abstração `SpeechService` no backend.
4. **Persistência:** SQLite via SQLAlchemy com padrão Repository no MVP.
5. **Containerização:** Docker e Docker Compose com script de automação `iniciar.sh`.

## Consequências
- A aplicação é leve, rápida de subir, altamente portável e 100% autônoma offline.
