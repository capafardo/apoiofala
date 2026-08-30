# Requisitos do Sistema - CAA-Lab

## Requisitos Funcionais (RF)

- **RF01 - Autenticação e Perfis:** Suporte a perfis de Administrador, Profissional e Usuário/Criança.
- **RF02 - Modo Criança:** Prancha tátil com navegação por categorias, grade de símbolos, botões grandes de ação ("Falar" e "Limpar").
- **RF03 - Catálogo e Biblioteca de Símbolos:** Cadastro, categorização, busca instantânea e ativação/desativação de mais de 80 pictogramas vetoriais locais.
- **RF04 - Construtor de Mensagens:** Seleção sequencial de símbolos, visualização concatenada ("Minha Mensagem") e remoção de itens individuais.
- **RF05 - Síntese de Voz (TTS):** Reprodução sonora local em português com controle de velocidade, tom e retorno imediato.
- **RF06 - Frases Rápidas:** Acesso a frases frequentes pré-configuradas acionáveis com 1 toque.
- **RF07 - Personalização de Pranchas (Drag-and-Drop):** Seleção de múltiplos símbolos na biblioteca e adição por arrastar e soltar nas categorias do perfil da criança.
- **RF08 - Cadastro de Perfis com Apelidos:** Cadastro de novos perfis com apelido da criança e apelido da mãe ou acompanhante, além de preferências visuais.
- **RF09 - Alternância de Perfis na Interface:** Seletor rápido de perfis na tela principal que recarrega a prancha e preferências sob medida.
- **RF10 - Modo Profissional:** Painel com métricas técnicas não invasivas, gestão de perfis e biblioteca de vocabulário.

---

## Requisitos Não Funcionais (RNF)

- **RNF01 - Autonomia 100% Offline:** Funcionamento autônomo sem conexão à Internet em tempo de execução.
- **RNF02 - Fail-Safe:** Falha em componentes secundários ou IA não interrompe a comunicação básica.
- **RNF03 - Acessibilidade:** Conformidade com padrões de acessibilidade (toque, teclado, temas de Alto Contraste, sem dependência exclusiva de cor).
- **RNF04 - Privacidade e LGPD:** Não registrar conteúdo conversacional sensível de crianças; dados armazenados exclusivamente local.
- **RNF05 - Desempenho e Baixa Latência:** Resposta tátil e síntese de voz instantâneas em estações locais Ubuntu.
- **RNF06 - Inicialização Automatizada:** Executável diretamente via `./iniciar.sh` e empacotado em Docker.
