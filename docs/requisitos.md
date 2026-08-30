# Requisitos do Sistema - CAA-Lab

## Requisitos Funcionais (RF)

- **RF01 - Autenticação e Perfis:** Suporte a perfis de Administrador, Profissional e Usuário/Criança.
- **RF02 - Modo Criança:** Navegação por categorias, grade de símbolos táteis, botões grandes de ação ("Falar" e "Limpar").
- **RF03 - Catálogo de Símbolos:** Cadastro, categorização, busca, ordenação e ativação/desativação de pictogramas.
- **RF04 - Construtor de Mensagens:** Seleção sequencial de símbolos, visualização concatenada e remoção de itens.
- **RF05 - Síntese de Voz:** Reprodução sonora local em português com controle de velocidade e suporte a fallback.
- **RF06 - Frases Rápidas:** Acesso a frases frequentes pré-configuradas acionáveis com 1 toque.
- **RF07 - Personalização de Perfil:** Ajuste de tamanho de símbolos, quantidade por página, cores, contraste e nível de complexidade.
- **RF08 - Modo Profissional:** Painel com métricas técnicas não invasivas e gestão de vocabulário e perfis.

## Requisitos Não Funcionais (RNF)

- **RNF01 - Autonomia Offline:** Funcionamento 100% autônomo sem internet.
- **RNF02 - Fail-Safe:** Falha em componentes secundários ou IA não deve interromper a comunicação básica.
- **RNF03 - Acessibilidade:** Conformidade com padrões de acessibilidade (toque, teclado, alto contraste, sem dependência exclusiva de cor).
- **RNF04 - Privacidade e LGPD:** Não registrar conteúdo conversacional sensível de crianças; dados armazenados exclusivamente local.
- **RNF05 - Desempenho e Latência:** Resposta tátil e síntese de voz com baixa latência em estações locais.
- **RNF06 - Inicialização Automatizada:** Executável diretamente via `./iniciar.sh`.
