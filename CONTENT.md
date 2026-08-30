# CONTENT.md

# CAA-Lab --- Aplicação Web de Comunicação Aumentativa e Alternativa

**Projeto:** Laboratório Tecnológico Inclusivo\
**Contexto:** CETAM / Instituto Benjamin Constant\
**Versão do documento:** 1.0\
**Finalidade:** especificação funcional, técnica e de desenvolvimento
para execução por uma IA de desenvolvimento no Antigravity CLI.

------------------------------------------------------------------------

## 1. INSTRUÇÃO PRINCIPAL À IA DE DESENVOLVIMENTO

Você é o agente responsável pelo desenvolvimento do **CAA-Lab**, uma
aplicação web local de apoio à Comunicação Aumentativa e Alternativa
(CAA), concebida como parte do Laboratório Tecnológico Inclusivo.

O sistema deve ser desenvolvido de forma incremental, documentada,
testável e reversível.

### Regras obrigatórias

1.  **Não alterar requisitos já homologados sem justificativa e
    aprovação explícita.**
2.  Antes de iniciar cada fase, ler este `CONTENT.md` e toda a
    documentação existente em `docs/`.
3.  Ao final de cada fase:
    -   executar testes;
    -   revisar o código produzido;
    -   corrigir problemas encontrados;
    -   atualizar a documentação;
    -   verificar os critérios de aceitação;
    -   registrar a fase como concluída;
    -   executar `git status`;
    -   criar um commit Git exclusivo para a etapa.
4.  Nunca considerar uma fase concluída apenas porque o código foi
    escrito.
5.  Não introduzir dependências desnecessárias.
6.  Priorizar software livre e de código aberto.
7.  A aplicação deve funcionar na rede local sem depender de serviços
    externos de IA ou APIs pagas.
8.  A IA/Ollama será componente complementar e opcional, nunca requisito
    para a comunicação básica.
9.  Dados potencialmente relacionados a crianças devem permanecer na
    infraestrutura local e ser tratados com princípio de minimização.
10. Não criar funcionalidades clínicas, diagnósticas ou terapêuticas. O
    sistema é uma ferramenta tecnológica de apoio.
11. Não interpretar automaticamente o estado emocional ou a intenção da
    criança como fato. A comunicação deve permanecer sob controle do
    usuário.
12. Toda funcionalidade nova deve ter documentação e testes
    correspondentes.
13. Não usar Internet em runtime para carregar fontes, bibliotecas,
    imagens, APIs ou serviços externos, salvo na estação explicitamente
    autorizada para profissionais.
14. A interface deve ser utilizável por toque, mouse e teclado.
15. O projeto deve ser executável por meio do script final `iniciar.sh`.

------------------------------------------------------------------------

# 2. CONTEXTO DO PROJETO

A proposta pedagógica do Laboratório Tecnológico Inclusivo prevê uma
infraestrutura tecnológica destinada ao apoio de crianças e jovens com
transtornos do neurodesenvolvimento, incluindo pessoas com TEA. O
projeto deve integrar formação técnica, infraestrutura real,
acessibilidade, segurança, documentação e homologação.

A proposta original prevê servidores locais para serviços e IA com
Ollama, estações de trabalho com softwares de apoio e acessibilidade,
rede local fechada, proteção de dados e software gratuito e de código
aberto.

No cenário atual informado para o desenvolvimento deste software existem
**6 máquinas, sendo 2 servidores**, todas utilizando Ubuntu. A solução
deve, portanto, funcionar nesse ambiente atual e permanecer preparada
para expansão futura.

O documento pedagógico estabelece ainda que a tecnologia deve atuar como
instrumento de apoio, e não como substituta da atuação de profissionais
especializados.

------------------------------------------------------------------------

# 3. VISÃO DO PRODUTO

## 3.1 Nome

**CAA-Lab**

CAA = Comunicação Aumentativa e Alternativa.

## 3.2 Propósito

Criar uma aplicação web local que permita ao usuário:

-   selecionar pictogramas;
-   visualizar palavras associadas aos pictogramas;
-   montar mensagens;
-   ouvir as mensagens por síntese de voz;
-   utilizar frases rápidas;
-   navegar por categorias;
-   utilizar vocabulário personalizado;
-   trabalhar com diferentes níveis de complexidade;
-   utilizar o sistema sem Internet.

O sistema deverá possuir também um **Modo Profissional**, destinado à
configuração e acompanhamento técnico do ambiente.

------------------------------------------------------------------------

# 4. PRINCÍPIOS DO PRODUTO

## 4.1 Comunicação antes da tecnologia

O aplicativo deve facilitar a comunicação, e não transformar a
tecnologia em obstáculo.

## 4.2 Simplicidade

A interface destinada à criança deve apresentar poucas decisões
simultâneas, controles grandes e organização visual consistente.

## 4.3 Autonomia

O usuário deve conseguir selecionar símbolos e produzir uma mensagem sem
depender de interpretação automática por IA.

## 4.4 Personalização

Não assumir que todas as crianças utilizam a mesma quantidade de
símbolos, categorias ou organização visual.

## 4.5 Multimodalidade

O sistema deve combinar:

-   pictograma;
-   palavra escrita;
-   construção de frase;
-   voz sintetizada.

## 4.6 Segurança

Dados devem permanecer na infraestrutura local sempre que possível.

## 4.7 Acessibilidade

A interface deve considerar:

-   tamanho dos elementos;
-   contraste;
-   legibilidade;
-   navegação por teclado;
-   toque;
-   feedback visual;
-   feedback sonoro;
-   redução de distrações;
-   possibilidade de personalização.

## 4.8 IA como componente auxiliar

O Ollama poderá ser utilizado para funções auxiliares, como organização
ou sugestão de vocabulário, mas não pode ser necessário para a
comunicação básica.

------------------------------------------------------------------------

# 5. ESCOPO DO MVP

O MVP deverá conter:

1.  autenticação;
2.  perfis de usuário;
3.  Modo Criança;
4.  Modo Profissional;
5.  biblioteca de pictogramas;
6.  categorias;
7.  construtor de mensagens;
8.  síntese de voz;
9.  frases rápidas;
10. vocabulário personalizado;
11. configurações de acessibilidade;
12. armazenamento local;
13. API local;
14. Docker;
15. documentação;
16. testes;
17. logs técnicos sem conteúdo sensível desnecessário;
18. script `iniciar.sh`.

------------------------------------------------------------------------

# 6. PERFIS DE USUÁRIO

## 6.1 Administrador

Responsável por:

-   usuários;
-   permissões;
-   configurações técnicas;
-   estações;
-   categorias;
-   manutenção.

## 6.2 Profissional

Pode:

-   configurar perfis;
-   organizar vocabulário;
-   criar frases;
-   configurar aparência;
-   acompanhar estatísticas técnicas de utilização;
-   preparar o ambiente para determinado usuário.

## 6.3 Usuário/participante

Utiliza principalmente:

-   pictogramas;
-   categorias;
-   construtor de mensagens;
-   frases rápidas;
-   voz.

A interface desse perfil deve ser deliberadamente simplificada.

------------------------------------------------------------------------

# 7. MODO CRIANÇA

O Modo Criança é o núcleo do produto.

## 7.1 Tela inicial

A tela deverá apresentar categorias visuais, por exemplo:

-   Comunicar;
-   Sentimentos;
-   Necessidades;
-   Comida e bebida;
-   Pessoas;
-   Lugares;
-   Brincar;
-   Frases rápidas;
-   Mais.

A organização exata deverá permanecer configurável.

## 7.2 Cartão de pictograma

Cada símbolo deverá possuir:

-   imagem;
-   palavra;
-   categoria;
-   identificador;
-   estado ativo/inativo;
-   ordem;
-   possibilidade de associação a áudio;
-   possibilidade de associação a frase.

## 7.3 Construção de mensagem

Exemplo:

`EU` + `QUERO` + `BEBER`

Resultado:

**Eu quero beber.**

A mensagem deverá ser apresentada visualmente e possuir botão de
reprodução.

## 7.4 Controles essenciais

A interface deve possuir pelo menos:

-   Falar;
-   Limpar;
-   Voltar;
-   Página anterior;
-   Próxima página;
-   Repetir mensagem;
-   Acessibilidade.

Os controles principais devem ter tamanho adequado para toque.

------------------------------------------------------------------------

# 8. FRASES RÁPIDAS

O sistema deverá permitir frases previamente cadastradas.

Exemplos conceituais:

-   Eu quero água.
-   Eu quero brincar.
-   Preciso de ajuda.
-   Não entendi.
-   Quero ir para casa.
-   Estou com fome.
-   Quero ir ao banheiro.

As frases devem ser personalizáveis por perfil.

O sistema não deve presumir que essas frases sejam apropriadas para
todos os usuários.

------------------------------------------------------------------------

# 9. VOCABULÁRIO E PICTOGRAMAS

O vocabulário deverá ser organizado em categorias.

Cada item deve possuir, no mínimo:

``` text
id
nome
texto
categoria
imagem
ordem
ativo
cor/contexto opcional
audio opcional
```

O administrador/profissional deverá poder:

-   criar;
-   editar;
-   desativar;
-   ordenar;
-   categorizar;
-   pesquisar;
-   associar imagem;
-   definir palavra;
-   definir frase falada.

O MVP deve possuir um conjunto inicial de símbolos de demonstração.

**Não utilizar imagens protegidas por direitos autorais sem
autorização.**

Preferir bibliotecas de pictogramas com licença compatível com o
projeto.

------------------------------------------------------------------------

# 10. SÍNTESE DE VOZ

A comunicação básica deverá funcionar localmente.

A arquitetura deve possuir uma abstração:

``` text
SpeechService
    |
    +-- LocalSpeechProvider
    |
    +-- FutureProvider
```

Assim, o mecanismo de voz poderá ser substituído sem alterar o restante
da aplicação.

Prioridade:

1.  funcionamento local;
2.  voz em português;
3.  baixa latência;
4.  ausência de dependência externa;
5.  possibilidade de configuração.

------------------------------------------------------------------------

# 11. MODO PROFISSIONAL

O Modo Profissional deverá possuir uma interface diferente do Modo
Criança.

Funcionalidades do MVP:

### Painel

-   usuários;
-   perfis;
-   vocabulário;
-   frases;
-   configurações;
-   relatórios técnicos.

### Perfil

Permitir configurar:

-   quantidade de símbolos por página;
-   tamanho dos símbolos;
-   categorias habilitadas;
-   vocabulário;
-   frases rápidas;
-   voz;
-   velocidade da voz;
-   contraste;
-   tema;
-   nível de complexidade.

------------------------------------------------------------------------

# 12. ESTATÍSTICAS

O MVP pode registrar métricas técnicas de uso, desde que sejam realmente
necessárias.

Exemplos:

-   quantidade de mensagens produzidas;
-   categorias utilizadas;
-   símbolos mais acessados;
-   frases rápidas utilizadas;
-   quantidade de sessões.

Evitar registrar conteúdo de comunicação quando não for necessário.

Não apresentar estatísticas como diagnóstico clínico.

Não utilizar os dados para inferir automaticamente condições
psicológicas ou clínicas.

------------------------------------------------------------------------

# 13. IA / OLLAMA

A integração com Ollama deverá ser opcional.

Possíveis utilizações futuras:

-   sugestão de vocabulário;
-   organização de categorias;
-   sugestão de frases;
-   personalização assistida;
-   auxílio ao profissional.

Não utilizar IA para:

-   diagnosticar;
-   classificar a criança;
-   afirmar emoções;
-   decidir o que a criança quis dizer;
-   substituir profissional;
-   bloquear comunicação.

A aplicação deverá continuar plenamente funcional quando Ollama estiver
desligado.

------------------------------------------------------------------------

# 14. ARQUITETURA PROPOSTA

## 14.1 Visão

``` text
                  REDE LOCAL

             ┌───────────────────┐
             │     SERVIDOR 1    │
             │ API / Banco / Web │
             └─────────┬─────────┘
                       │
                       │ LAN
                       │
             ┌─────────▼─────────┐
             │     SERVIDOR 2    │
             │ Ollama / Serviços │
             └─────────┬─────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
   ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
   │ Estação │    │ Estação │    │ Estação │
   │ Docker  │    │ Docker  │    │ Docker  │
   └─────────┘    └─────────┘    └─────────┘
```

A implementação deve ser compatível com a infraestrutura atual de 6
máquinas e escalável para a configuração futura prevista para o
laboratório.

------------------------------------------------------------------------

# 15. STACK TECNOLÓGICA

A implementação inicial deverá priorizar:

### Backend

-   Python;
-   FastAPI;
-   Pydantic;
-   SQLAlchemy;
-   Uvicorn.

### Frontend

Preferir inicialmente:

-   HTML5;
-   CSS3;
-   JavaScript moderno.

Pode-se adotar React/Vite caso a complexidade real do projeto
justifique, mas não adicionar um framework apenas por preferência.

### Banco

Para o MVP:

-   SQLite, quando o banco for utilizado por uma única instância
    central.

A arquitetura deve manter uma camada de acesso a dados que permita
migração futura para PostgreSQL.

### Infraestrutura

-   Ubuntu;
-   Docker;
-   Docker Compose;
-   Git;
-   navegador web;
-   rede TCP/IP local.

### Testes

-   pytest;
-   testes de API;
-   testes de integração;
-   testes de frontend quando aplicável.

------------------------------------------------------------------------

# 16. ESTRUTURA DO PROJETO

Criar estrutura semelhante a:

``` text
caa-lab/
├── CONTENT.md
├── README.md
├── iniciar.sh
├── docker-compose.yml
├── .env.example
├── .gitignore
│
├── app/
│   ├── main.py
│   ├── core/
│   ├── api/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── templates/
│   └── static/
│
├── data/
│   └── .gitkeep
│
├── assets/
│   ├── pictograms/
│   └── audio/
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/
│
└── docs/
    ├── README.md
    ├── arquitetura.md
    ├── requisitos.md
    ├── banco-de-dados.md
    ├── api.md
    ├── acessibilidade.md
    ├── seguranca.md
    ├── docker.md
    ├── testes.md
    ├── homologacao.md
    ├── operacao.md
    ├── changelog.md
    └── decisoes/
```

A IA poderá ajustar a estrutura se houver justificativa técnica, mas não
deverá criar complexidade desnecessária.

------------------------------------------------------------------------

# 17. DOCUMENTAÇÃO AUTOMÁTICA

A pasta `docs/` é parte obrigatória do projeto.

Toda fase deverá atualizar a documentação correspondente.

## Documentos mínimos

### `docs/arquitetura.md`

Descrever:

-   componentes;
-   fluxo;
-   portas;
-   rede;
-   dependências;
-   comunicação entre máquinas;
-   containers.

### `docs/requisitos.md`

Manter requisitos funcionais e não funcionais atualizados.

### `docs/api.md`

Documentar endpoints.

### `docs/banco-de-dados.md`

Documentar:

-   tabelas;
-   relacionamentos;
-   índices;
-   migrations;
-   política de dados.

### `docs/acessibilidade.md`

Registrar decisões de acessibilidade e resultados dos testes.

### `docs/seguranca.md`

Registrar:

-   autenticação;
-   autorização;
-   armazenamento de credenciais;
-   proteção de dados;
-   exposição de portas;
-   logs;
-   backups.

### `docs/testes.md`

Registrar:

-   testes existentes;
-   cobertura;
-   testes manuais;
-   resultados.

### `docs/homologacao.md`

Registrar os critérios de aceite e o resultado de cada homologação.

### `docs/changelog.md`

Registrar alterações por versão.

### `docs/decisoes/`

Registrar decisões arquiteturais importantes no formato:

``` text
ADR-001-nome-da-decisao.md
ADR-002-nome-da-decisao.md
```

------------------------------------------------------------------------

# 18. CONTROLE DE VERSÃO

Git é obrigatório.

Antes de iniciar:

``` bash
git status
```

Cada fase concluída deve gerar um commit.

Formato recomendado:

``` text
feat(fase-01): estrutura inicial do projeto
feat(fase-02): autenticação e perfis
feat(fase-03): modo criança
feat(fase-04): vocabulário e pictogramas
feat(fase-05): construtor de mensagens
feat(fase-06): síntese de voz
feat(fase-07): modo profissional
feat(fase-08): acessibilidade
feat(fase-09): docker e rede local
test(fase-10): testes e homologação
docs(fase-11): documentação final
feat(fase-12): script de inicialização
```

A IA deve verificar:

``` bash
git status
git diff
```

antes de cada commit.

Nunca utilizar:

``` bash
git add .
```

sem revisar o que será incluído.

Preferir adicionar explicitamente os arquivos relevantes.

------------------------------------------------------------------------

# 19. FASES DE DESENVOLVIMENTO

## FASE 0 --- Preparação

### Objetivo

Preparar o repositório.

### Entregas

-   Git;
-   estrutura inicial;
-   `.gitignore`;
-   `README.md`;
-   `docs/README.md`;
-   ambiente Python;
-   configuração inicial Docker.

### Aceitação

-   projeto inicia sem erro;
-   documentação inicial existe;
-   Git limpo após commit.

------------------------------------------------------------------------

## FASE 1 --- Arquitetura

### Entregas

-   FastAPI;
-   estrutura de módulos;
-   configuração;
-   health check;
-   página inicial;
-   configuração de ambiente.

Endpoint mínimo:

``` text
GET /health
```

Resposta esperada:

``` json
{
  "status": "ok"
}
```

### Aceitação

-   servidor inicia;
-   `/health` funciona;
-   aplicação não possui dependências externas desnecessárias;
-   documentação de arquitetura criada.

------------------------------------------------------------------------

## FASE 2 --- Banco e autenticação

### Entregas

-   banco;
-   modelos;
-   usuário;
-   perfis;
-   autenticação;
-   senha armazenada com hash;
-   autorização.

### Aceitação

-   usuário pode autenticar;
-   senha nunca fica armazenada em texto puro;
-   usuário comum não acessa administração;
-   profissional acessa suas funções;
-   administrador acessa administração;
-   testes automatizados cobrem autenticação.

------------------------------------------------------------------------

## FASE 3 --- Modo Criança

### Entregas

-   interface visual;
-   categorias;
-   cartões;
-   navegação;
-   responsividade;
-   botão Falar;
-   botão Limpar.

### Aceitação

-   criança consegue navegar sem teclado;
-   botões possuem área adequada para toque;
-   textos são legíveis;
-   não há necessidade de Internet;
-   fluxo básico pode ser concluído sem IA.

------------------------------------------------------------------------

## FASE 4 --- Pictogramas e vocabulário

### Entregas

-   banco de símbolos;
-   categorias;
-   busca;
-   ordenação;
-   ativação/desativação;
-   conjunto inicial de demonstração.

### Aceitação

-   símbolo pode ser cadastrado;
-   símbolo aparece na categoria correta;
-   símbolo pode ser desativado;
-   vocabulário personalizado aparece para o perfil correto.

------------------------------------------------------------------------

## FASE 5 --- Construtor de mensagens

### Entregas

-   seleção sequencial;
-   visualização da mensagem;
-   remoção de item;
-   limpeza;
-   reprodução.

Exemplo:

``` text
EU → QUERO → ÁGUA
```

deve resultar em:

``` text
Eu quero água.
```

### Aceitação

-   ordem dos símbolos é preservada;
-   frase correspondente é exibida;
-   frase pode ser reproduzida;
-   erro em um símbolo não impede o restante da aplicação.

------------------------------------------------------------------------

## FASE 6 --- Voz

### Entregas

-   serviço local de voz;
-   configuração de voz;
-   velocidade;
-   tratamento de erro;
-   fallback.

### Aceitação

-   mensagem pode ser ouvida;
-   ausência do serviço de voz não derruba a aplicação;
-   erro é comunicado de maneira simples;
-   nenhuma API externa é obrigatória.

------------------------------------------------------------------------

## FASE 7 --- Frases rápidas

### Entregas

-   cadastro;
-   edição;
-   ordenação;
-   exclusão/desativação;
-   reprodução.

### Aceitação

-   frase pode ser criada;
-   frase aparece para o perfil correto;
-   toque reproduz a frase;
-   frases podem ser reorganizadas.

------------------------------------------------------------------------

## FASE 8 --- Personalização

### Entregas

-   tamanho dos símbolos;
-   quantidade por página;
-   contraste;
-   categorias;
-   voz;
-   tema;
-   nível de complexidade.

### Aceitação

-   configurações persistem;
-   alterações aparecem imediatamente ou após recarregamento;
-   configuração de um usuário não altera outro;
-   interface continua utilizável em telas pequenas.

------------------------------------------------------------------------

## FASE 9 --- Modo Profissional

### Entregas

-   painel;
-   usuários;
-   perfis;
-   vocabulário;
-   frases;
-   configurações;
-   métricas técnicas.

### Aceitação

-   acesso protegido;
-   criança não acessa painel profissional;
-   profissional consegue preparar um perfil;
-   ações importantes são registradas em log técnico.

------------------------------------------------------------------------

## FASE 10 --- Segurança e privacidade

### Entregas

-   revisão de autenticação;
-   autorização;
-   sessões;
-   headers de segurança;
-   validação de entrada;
-   proteção contra acesso indevido;
-   política de logs;
-   política de dados;
-   backup.

### Aceitação

-   endpoints protegidos;
-   dados não são enviados para serviços externos;
-   segredos não ficam no Git;
-   `.env` não é versionado;
-   logs não armazenam dados desnecessários;
-   documentação de segurança atualizada.

------------------------------------------------------------------------

## FASE 11 --- Docker e infraestrutura

### Entregas

-   Dockerfile;
-   Docker Compose;
-   healthcheck;
-   volumes;
-   configuração de rede;
-   documentação de implantação.

### Aceitação

Executar:

``` bash
docker compose up -d
```

e obter aplicação funcional.

Verificar:

``` bash
docker compose ps
```

Todos os serviços necessários devem estar saudáveis.

------------------------------------------------------------------------

## FASE 12 --- Testes e homologação

### Testes obrigatórios

-   autenticação;
-   autorização;
-   banco;
-   API;
-   vocabulário;
-   construção de mensagens;
-   voz;
-   frases rápidas;
-   personalização;
-   acessibilidade;
-   Docker.

Executar:

``` bash
pytest
```

### Homologação manual

Testar pelo menos:

1.  login;
2.  seleção de pictograma;
3.  criação de frase;
4.  reprodução de voz;
5.  limpeza;
6.  frase rápida;
7.  alteração de configuração;
8.  acesso profissional;
9.  funcionamento sem Internet;
10. reinicialização do container.

------------------------------------------------------------------------

# 20. ACESSIBILIDADE

A aplicação deverá seguir princípios de acessibilidade web.

Verificar:

-   contraste;
-   foco visível;
-   navegação por teclado;
-   textos alternativos;
-   semântica HTML;
-   tamanho dos controles;
-   ausência de dependência exclusiva de cor;
-   mensagens de erro compreensíveis;
-   suporte a redução de movimento;
-   compatibilidade com leitores de tela quando aplicável.

A interface da criança deve evitar excesso de elementos simultâneos.

------------------------------------------------------------------------

# 21. SEGURANÇA E LGPD

O projeto deverá adotar princípios de:

-   minimização;
-   necessidade;
-   controle de acesso;
-   armazenamento local;
-   proteção de credenciais;
-   backups controlados;
-   separação de perfis;
-   registro de ações administrativas relevantes.

A IA não deve enviar dados para serviços externos.

O sistema não deve coletar dados pessoais além do necessário para seu
funcionamento.

Qualquer utilização real com crianças deverá ser submetida à avaliação e
orientação dos profissionais e responsáveis institucionais competentes.

------------------------------------------------------------------------

# 22. TESTES DE REDE

A aplicação deverá ser testada em:

### localhost

``` text
http://localhost:PORTA
```

### IP da estação

``` text
http://IP_DA_ESTACAO:PORTA
```

### acesso pela LAN

Outra máquina deverá conseguir acessar o serviço quando essa for a
arquitetura adotada.

Verificar também:

-   firewall;
-   portas abertas;
-   resolução de nomes, se utilizada;
-   isolamento da rede;
-   indisponibilidade do servidor;
-   reinicialização dos serviços.

------------------------------------------------------------------------

# 23. OBSERVABILIDADE

Criar pelo menos:

``` text
/health
```

Opcionalmente:

``` text
/ready
```

Os logs devem permitir diagnosticar:

-   inicialização;
-   erro de API;
-   erro de banco;
-   erro de voz;
-   indisponibilidade de serviço.

Não registrar conteúdo de mensagens da criança por padrão.

------------------------------------------------------------------------

# 24. PRINCÍPIO DE FAIL-SAFE

O aplicativo nunca deve deixar de funcionar simplesmente porque um
componente secundário falhou.

Exemplo:

``` text
Ollama indisponível
       ↓
CAA continua funcionando

Banco de sugestões indisponível
       ↓
CAA continua funcionando

Serviço opcional de IA indisponível
       ↓
CAA continua funcionando
```

A comunicação básica deve depender apenas dos componentes essenciais.

------------------------------------------------------------------------

# 25. INTERFACE VISUAL

A imagem conceitual fornecida para o projeto deve ser tratada como
**referência de inspiração**, não como especificação pixel a pixel.

Diretrizes visuais:

-   interface limpa;
-   aparência acolhedora;
-   alto contraste;
-   cartões grandes;
-   pictogramas claros;
-   palavra escrita abaixo do símbolo;
-   painel de mensagem sempre visível;
-   botão de voz claramente identificável;
-   navegação simples;
-   Modo Criança visualmente diferente do Modo Profissional.

O design deve priorizar funcionalidade e acessibilidade sobre efeitos
visuais.

------------------------------------------------------------------------

# 26. IA NO ANTIGRAVITY CLI

O agente deverá trabalhar seguindo este ciclo:

``` text
LER
 ↓
PLANEJAR
 ↓
IMPLEMENTAR
 ↓
TESTAR
 ↓
REVISAR
 ↓
DOCUMENTAR
 ↓
HOMOLOGAR
 ↓
COMMIT
 ↓
PRÓXIMA FASE
```

Antes de cada fase:

``` bash
git status
```

Depois da implementação:

``` bash
pytest
```

e os demais testes aplicáveis.

Depois:

``` bash
git diff
```

Depois atualizar:

``` text
docs/
```

Somente então realizar o commit.

------------------------------------------------------------------------

# 27. REVISÃO OBRIGATÓRIA

Ao final de cada fase, a IA deve executar uma revisão com estas
perguntas:

### Código

-   Existe código duplicado?
-   Há dependências desnecessárias?
-   Há erros evidentes?
-   Existem funções excessivamente complexas?
-   Há tratamento adequado de exceções?

### Segurança

-   Há dados sensíveis expostos?
-   Existem segredos no código?
-   Os endpoints estão protegidos?
-   Há validação de entrada?

### Acessibilidade

-   A funcionalidade pode ser usada por toque?
-   Pode ser usada por teclado?
-   Os elementos são suficientemente grandes?
-   Há feedback visual e textual?

### Privacidade

-   Estamos armazenando mais dados do que o necessário?
-   Algum dado está sendo enviado para fora da rede?

### Infraestrutura

-   O container inicia corretamente?
-   O serviço reinicia?
-   O healthcheck funciona?

### Documentação

-   `docs/` está atualizado?
-   README está atualizado?
-   Changelog está atualizado?

------------------------------------------------------------------------

# 28. DEFINITION OF DONE

Uma fase só pode ser marcada como concluída quando:

-   [ ] implementação concluída;
-   [ ] testes executados;
-   [ ] erros corrigidos;
-   [ ] revisão concluída;
-   [ ] critérios de aceitação atendidos;
-   [ ] documentação atualizada;
-   [ ] Git revisado;
-   [ ] commit realizado;
-   [ ] working tree em estado conhecido.

------------------------------------------------------------------------

# 29. SCRIPT `iniciar.sh`

Ao final do projeto deverá existir:

``` text
iniciar.sh
```

Objetivo:

> Preparar o ambiente e iniciar a aplicação automaticamente.

O script deverá:

1.  detectar a pasta do projeto;
2.  verificar Docker;
3.  verificar Docker Compose;
4.  verificar dependências essenciais;
5.  criar diretórios necessários;
6.  carregar variáveis de ambiente de `.env`, quando existente;
7.  iniciar os containers;
8.  aguardar o healthcheck;
9.  identificar a URL da aplicação;
10. abrir a aplicação no navegador padrão do Ubuntu.

Comportamento conceitual:

``` bash
#!/usr/bin/env bash

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

echo "Iniciando CAA-Lab..."

# verificar Docker
# verificar Docker Compose
# preparar ambiente
# iniciar containers
# aguardar /health
# abrir navegador

echo "CAA-Lab iniciado."
```

O script deve ser idempotente: executá-lo novamente não deve criar
containers duplicados nem corromper dados.

Deve também detectar a ausência de comandos necessários e apresentar
mensagem clara.

Para abrir o navegador, preferir:

``` bash
xdg-open "http://localhost:PORTA"
```

Não assumir que um navegador específico esteja instalado.

O script deve possuir:

``` bash
chmod +x iniciar.sh
```

e ser documentado no `README.md`.

------------------------------------------------------------------------

# 30. CRITÉRIO FINAL DE ACEITAÇÃO DO MVP

O MVP será considerado concluído quando for possível, em uma estação
Ubuntu:

``` text
executar ./iniciar.sh
        ↓
containers iniciam
        ↓
aplicação fica disponível
        ↓
browser abre automaticamente
        ↓
usuário autentica
        ↓
entra no Modo Criança
        ↓
seleciona pictogramas
        ↓
monta uma mensagem
        ↓
visualiza a frase
        ↓
ouve a frase
        ↓
limpa a mensagem
        ↓
utiliza uma frase rápida
```

E, simultaneamente:

-   o Modo Profissional funciona;
-   o vocabulário pode ser personalizado;
-   as configurações podem ser alteradas;
-   os testes passam;
-   a aplicação funciona na rede local;
-   a funcionalidade básica não depende de Internet;
-   a funcionalidade básica não depende de Ollama;
-   a documentação está atualizada;
-   o projeto possui histórico Git organizado;
-   todos os critérios de aceite estão registrados em
    `docs/homologacao.md`.

------------------------------------------------------------------------

# 31. ENTREGA FINAL

Ao terminar todas as fases, produzir:

``` text
README.md
CONTENT.md
iniciar.sh
docker-compose.yml
.env.example
docs/
app/
tests/
assets/
```

Executar uma última revisão completa.

Executar:

``` bash
pytest
docker compose config
docker compose up -d
docker compose ps
```

Testar a aplicação pelo navegador.

Verificar:

``` bash
git status
```

Corrigir qualquer problema restante.

Atualizar:

``` text
docs/changelog.md
docs/homologacao.md
README.md
```

Criar o commit final:

``` text
release(mvp): CAA-Lab MVP 1.0
```

Não declarar o projeto concluído enquanto houver critério de aceitação
pendente.

------------------------------------------------------------------------

# 32. VISÃO DE FUTURO

O MVP deverá ser arquitetado para permitir evolução posterior, sem
implementar prematuramente funcionalidades complexas.

Possíveis extensões:

-   suporte a múltiplas estações;
-   sincronização entre servidor e estações;
-   perfis mais sofisticados;
-   biblioteca ampliada de pictogramas;
-   suporte a fotografias personalizadas;
-   impressão de pranchas de comunicação;
-   modo tablet;
-   integração com dispositivos de acessibilidade;
-   estatísticas avançadas;
-   IA local com Ollama;
-   mecanismos de recomendação;
-   múltiplos idiomas;
-   administração centralizada;
-   backup automatizado;
-   alta disponibilidade.

Essas funcionalidades futuras não devem comprometer a simplicidade do
MVP.

------------------------------------------------------------------------

# 33. PRINCÍPIO FINAL

O CAA-Lab não deve ser tratado apenas como um exercício de programação.

Ele é um **produto tecnológico com finalidade social**, desenvolvido
dentro de um laboratório educacional, com participação de alunos,
orientação especializada e preocupação explícita com acessibilidade,
privacidade, segurança e impacto social.

A prioridade de engenharia deve seguir:

``` text
ACESSIBILIDADE
      ↓
USABILIDADE
      ↓
CONFIABILIDADE
      ↓
PRIVACIDADE
      ↓
SEGURANÇA
      ↓
SIMPLICIDADE
      ↓
TECNOLOGIA
      ↓
IA
```

A IA é uma ferramenta de apoio.

A tecnologia deve servir à comunicação.

**TECNOLOGIA COM PROPÓSITO.**

**FORMAÇÃO TÉCNICA COM IMPACTO SOCIAL.**
