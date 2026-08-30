# Registro de Homologação - CAA-Lab

Este documento registra os critérios de aceite e o status de homologação de cada fase do projeto.

---

## Fases do Projeto

| Fase | Título | Status | Data | Observações |
| :--- | :--- | :--- | :--- | :--- |
| **0** | Preparação do ambiente e estrutura | Concluído | 2026-08-30 | Repositório inicializado, docs criados, venv configurado e teste de sanidade aprovado. |
| **1** | Arquitetura e FastAPI | Concluído | 2026-08-30 | FastAPI configurado com settings, healthcheck (/health, /ready), middlewares e testes de integração. |
| **2** | Banco de dados e Autenticação | Concluído | 2026-08-30 | Modelos SQLAlchemy, criptografia bcrypt, JWT, perfis, controle de acesso e seed de dados. |
| **3** | Interface do Modo Criança | Concluído | 2026-08-30 | Prancha de comunicação com categorias laterais, grade de pictogramas, responsividade e alvos táteis. |
| **4** | Pictogramas e Vocabulário | Concluído | 2026-08-30 | Conjunto de 25+ SVGs vetoriais offline, busca, filtro por categoria e ordenação. |
| **5** | Construtor de Mensagens | Concluído | 2026-08-30 | Painel 'Minha Mensagem', seleção sequencial, remoção individual e concatenação textual. |
| **6** | Síntese de Voz (TTS) | Concluído | 2026-08-30 | Camada SpeechService com Web Speech API local offline (pt-BR) e botões de áudio. |
| **7** | Frases Rápidas | Concluído | 2026-08-30 | Atalhos de frases prontas com acionamento sonoro direto em 1 clique. |
| **8** | Personalização e Acessibilidade | Concluído | 2026-08-30 | Modo Alto Contraste, ajuste dinâmico de tamanho de símbolos (A-/A+) e foco por teclado. |
| **9** | Modo Profissional | Concluído | 2026-08-30 | Painel com métricas não invasivas, editor de perfis e biblioteca de vocabulário. |
| **10** | Segurança e Privacidade | Concluído | 2026-08-30 | LGPD compliant, zero telemetria externa, senhas com hash seguro e headers de proteção. |
| **11** | Docker e Rede Local | Concluído | 2026-08-30 | Dockerfile slim, docker-compose.yml com volumes e isolamento de rede local. |
| **12** | Testes Finais e Homologação MVP | Concluído | 2026-08-30 | 24 testes automatizados aprovados (unitários e integração) e script iniciar.sh validado. |
