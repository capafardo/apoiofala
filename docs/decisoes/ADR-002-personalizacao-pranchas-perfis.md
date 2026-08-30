# ADR-002: Personalização de Pranchas via Drag-and-Drop e Suporte a Múltiplos Perfis com Apelidos

## Status
Aceito

## Contexto
Crianças com transtornos do neurodesenvolvimento (como TEA) possuem necessidades comunicativas altamente heterogêneas: algumas utilizam apenas 6 símbolos grandes por página, enquanto outras utilizam vocabulários mais complexos. 

Além disso, terapeutas e fonoaudiólogos precisam de uma maneira ágil e visual (Arrastar e Soltar) para selecionar pictogramas de uma biblioteca central e montar pranchas específicas para cada categoria no perfil daquela criança, identificando-a claramente pelo seu apelido e o de sua mãe ou acompanhante.

## Decisão
1. **Modelagem de Prancha por Perfil (`ProfileSymbol`):**
   - Criou-se a tabela associativa `profile_symbols (profile_id, symbol_id, category_id, order_index, is_active)`.
   - Quando um perfil possui símbolos customizados para uma categoria, o sistema exibe essa lista sob medida; caso contrário, realiza fallback automático para os símbolos padrão globais da categoria.
2. **Biblioteca Central Offline:**
   - A biblioteca de mais de 80 símbolos SVG é servida localmente e exposta via `GET /api/v1/symbols/library`.
3. **Mecanismo de Arrastar e Soltar (HTML5 Drag & Drop):**
   - No painel profissional, o terapeuta pode marcar um ou múltiplos símbolos na biblioteca e arrastá-los para a zona de destino da categoria selecionada.
   - O backend expõe os endpoints `/assign` e `/add` para persistência em lote.
4. **Identificação de Perfis:**
   - Adicionados os campos `child_nickname` e `guardian_nickname` no modelo `Profile`.
   - Seletor rápido de perfil integrado no topo do Modo Criança.

## Consequências
- A prancha de cada criança pode ser personalizada sem afetar o vocabulário das outras estações ou perfis.
- A experiência do profissional torna-se intuitiva e tátil.
- O sistema mantém 100% de compatibilidade offline e integridade referencial no SQLite.
