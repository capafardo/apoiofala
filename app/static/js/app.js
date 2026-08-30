/**
 * CAA-Lab - Modo Criança (Lógica de Prancha de Comunicação Personalizada)
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Estado da Aplicação
  const state = {
    profiles: [],
    currentProfileId: null,
    currentProfile: null,
    categories: [],
    currentCategoryId: null,
    currentCategorySlug: 'inicio',
    allSymbols: [],
    filteredSymbols: [],
    currentPage: 1,
    pageSize: 12,
    messageTokens: [],
    isHighContrast: false,
  };

  // Elementos do DOM
  const userProfileSelect = document.getElementById('user-profile-select');
  const sidebarProfileLabel = document.getElementById('sidebar-profile-label');
  const categoriesListEl = document.getElementById('category-list');
  const activeCategoryTitleEl = document.getElementById('active-category-title');
  const symbolsGridEl = document.getElementById('symbols-grid');
  const paginationDotsEl = document.getElementById('pagination-dots');
  const prevPageBtn = document.getElementById('prev-page-btn');
  const nextPageBtn = document.getElementById('next-page-btn');
  const messageBuilderFlowEl = document.getElementById('message-builder-flow');
  const renderedMessageTextEl = document.getElementById('rendered-message-text');
  const quickPhrasesListEl = document.getElementById('quick-phrases-list');

  // Botões de Ação
  const speakMainBtn = document.getElementById('btn-speak-main');
  const clearMainBtn = document.getElementById('btn-clear-main');
  const speakInlineBtn = document.getElementById('btn-speak-inline');
  const btnFontDec = document.getElementById('btn-font-dec');
  const btnFontInc = document.getElementById('btn-font-inc');
  const btnContrastToggle = document.getElementById('btn-contrast-toggle');

  // 1. Inicializar Perfis
  async function initProfiles() {
    state.profiles = await window.API.getProfiles();
    if (!userProfileSelect) return;

    userProfileSelect.innerHTML = '';
    state.profiles.forEach((p) => {
      const opt = document.createElement('option');
      opt.value = p.id;
      const childNick = p.child_nickname ? ` (${p.child_nickname})` : '';
      const guardian = p.guardian_nickname ? ` - Resp: ${p.guardian_nickname}` : '';
      opt.textContent = `${p.name}${childNick}${guardian}`;
      userProfileSelect.appendChild(opt);
    });

    const savedProfileId = localStorage.getItem('caa_lab_active_profile_id');
    if (savedProfileId && state.profiles.some((p) => p.id === parseInt(savedProfileId))) {
      state.currentProfileId = parseInt(savedProfileId);
    } else if (state.profiles.length > 0) {
      state.currentProfileId = state.profiles[0].id;
    }

    userProfileSelect.value = state.currentProfileId;
    applyProfileSettings(state.currentProfileId);

    userProfileSelect.onchange = () => {
      state.currentProfileId = parseInt(userProfileSelect.value);
      localStorage.setItem('caa_lab_active_profile_id', state.currentProfileId);
      applyProfileSettings(state.currentProfileId);
      loadSymbols();
      loadQuickPhrases();
    };
  }

  function applyProfileSettings(profileId) {
    const p = state.profiles.find((x) => x.id === profileId);
    if (!p) return;
    state.currentProfile = p;

    // Atualizar label na barra lateral
    if (sidebarProfileLabel) {
      const nick = p.child_nickname || p.name;
      const resp = p.guardian_nickname ? ` • ${p.guardian_nickname}` : '';
      sidebarProfileLabel.textContent = `${nick}${resp}`;
    }

    // Aplicar tamanho dos símbolos
    document.body.classList.remove('symbol-small', 'symbol-large');
    if (p.symbol_size === 'pequeno') {
      document.body.classList.add('symbol-small');
    } else if (p.symbol_size === 'grande') {
      document.body.classList.add('symbol-large');
    }

    // Aplicar itens por página
    state.pageSize = p.symbols_per_page || 12;

    // Ajustar velocidade da voz
    if (window.speechCtrl && p.voice_speed) {
      window.speechCtrl.setSpeed(p.voice_speed);
    }
  }

  // 2. Inicializar Categorias
  async function initCategories() {
    state.categories = await window.API.getCategories();
    renderCategories();
    if (state.categories.length > 0) {
      selectCategory(state.categories[0].id, state.categories[0].name, state.categories[0].slug);
    }
  }

  function renderCategories() {
    if (!categoriesListEl) return;
    categoriesListEl.innerHTML = '';

    const iconMap = {
      inicio: '🏠',
      comunicar: '💬',
      'frases-rapidas': '⭐',
      sentimentos: '❤️',
      necessidades: '🚾',
      'comida-bebida': '🍎',
      pessoas: '👥',
      lugares: '🏫',
      brincar: '⚽',
      mais: '➕',
    };

    state.categories.forEach((cat) => {
      const btn = document.createElement('button');
      btn.className = `category-btn ${cat.id === state.currentCategoryId ? 'active' : ''}`;
      btn.innerHTML = `<span class="icon">${iconMap[cat.slug] || '📁'}</span><span>${cat.name}</span>`;
      btn.addEventListener('click', () => {
        selectCategory(cat.id, cat.name, cat.slug);
        window.API.recordMetric('change_category', cat.slug, cat.id);
      });
      categoriesListEl.appendChild(btn);
    });
  }

  function selectCategory(id, name, slug) {
    state.currentCategoryId = id;
    state.currentCategorySlug = slug;
    state.currentPage = 1;

    if (activeCategoryTitleEl) {
      activeCategoryTitleEl.textContent = name;
    }

    renderCategories();
    loadSymbols();
  }

  // 3. Carregar e Renderizar Símbolos (considerando perfil ativo)
  async function loadSymbols() {
    state.allSymbols = await window.API.getSymbols(state.currentCategoryId, state.currentProfileId);
    state.filteredSymbols = state.allSymbols;
    renderSymbolsGrid();
  }

  function renderSymbolsGrid() {
    if (!symbolsGridEl) return;
    symbolsGridEl.innerHTML = '';

    const totalPages = Math.ceil(state.filteredSymbols.length / state.pageSize) || 1;
    const startIdx = (state.currentPage - 1) * state.pageSize;
    const pageItems = state.filteredSymbols.slice(startIdx, startIdx + state.pageSize);

    if (pageItems.length === 0) {
      symbolsGridEl.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: var(--text-secondary); padding: 40px;">Nenhum símbolo disponível nesta categoria para este perfil.</div>';
      renderPagination(1, 1);
      return;
    }

    pageItems.forEach((sym) => {
      const card = document.createElement('div');
      card.className = 'symbol-card';
      if (sym.bg_color && !state.isHighContrast) {
        card.style.backgroundColor = sym.bg_color;
      }

      card.innerHTML = `
        <div class="symbol-img-wrap">
          <img src="${sym.image_path}" alt="${sym.text_label}" loading="lazy" />
        </div>
        <div class="symbol-label">${sym.text_label}</div>
      `;

      card.addEventListener('click', () => {
        addSymbolToMessage(sym);
        // Feedback sonoro imediato do símbolo
        window.speechCtrl.speak(sym.spoken_text || sym.text_label);
        window.API.recordMetric('touch_symbol', sym.name, state.currentCategoryId);
      });

      symbolsGridEl.appendChild(card);
    });

    renderPagination(state.currentPage, totalPages);
  }

  function renderPagination(currentPage, totalPages) {
    if (!paginationDotsEl) return;
    paginationDotsEl.innerHTML = '';

    if (prevPageBtn) prevPageBtn.disabled = currentPage <= 1;
    if (nextPageBtn) nextPageBtn.disabled = currentPage >= totalPages;

    for (let i = 1; i <= totalPages; i++) {
      const dot = document.createElement('div');
      dot.className = `dot ${i === currentPage ? 'active' : ''}`;
      dot.addEventListener('click', () => {
        state.currentPage = i;
        renderSymbolsGrid();
      });
      paginationDotsEl.appendChild(dot);
    }
  }

  if (prevPageBtn) {
    prevPageBtn.addEventListener('click', () => {
      if (state.currentPage > 1) {
        state.currentPage--;
        renderSymbolsGrid();
      }
    });
  }

  if (nextPageBtn) {
    nextPageBtn.addEventListener('click', () => {
      const totalPages = Math.ceil(state.filteredSymbols.length / state.pageSize) || 1;
      if (state.currentPage < totalPages) {
        state.currentPage++;
        renderSymbolsGrid();
      }
    });
  }

  // 4. Construtor de Mensagens (Minha Mensagem)
  function addSymbolToMessage(symbol) {
    state.messageTokens.push(symbol);
    renderMessageBuilder();
  }

  function removeSymbolFromMessage(index) {
    state.messageTokens.splice(index, 1);
    renderMessageBuilder();
  }

  function clearMessage() {
    state.messageTokens = [];
    renderMessageBuilder();
  }

  function getConstructedSentence() {
    if (state.messageTokens.length === 0) return '';
    const words = state.messageTokens.map((t) => t.spoken_text || t.text_label);
    let sentence = words.join(' ');
    sentence = sentence.charAt(0).toUpperCase() + sentence.slice(1) + '.';
    return sentence;
  }

  function renderMessageBuilder() {
    if (!messageBuilderFlowEl || !renderedMessageTextEl) return;
    messageBuilderFlowEl.innerHTML = '';

    if (state.messageTokens.length === 0) {
      messageBuilderFlowEl.innerHTML = '<span style="color: var(--text-secondary); font-size: 0.9rem;">Toque nos símbolos para montar sua mensagem...</span>';
      renderedMessageTextEl.textContent = '...';
      return;
    }

    state.messageTokens.forEach((token, idx) => {
      if (idx > 0) {
        const plus = document.createElement('span');
        plus.className = 'token-plus-sign';
        plus.textContent = '+';
        messageBuilderFlowEl.appendChild(plus);
      }

      const tokenEl = document.createElement('div');
      tokenEl.className = 'message-symbol-token';
      tokenEl.title = 'Clique para remover';
      tokenEl.innerHTML = `
        <img src="${token.image_path}" alt="${token.text_label}" />
        <span>${token.text_label}</span>
      `;
      tokenEl.addEventListener('click', () => removeSymbolFromMessage(idx));
      messageBuilderFlowEl.appendChild(tokenEl);
    });

    const sentence = getConstructedSentence();
    renderedMessageTextEl.textContent = sentence;
  }

  function speakConstructedMessage() {
    const sentence = getConstructedSentence();
    if (sentence && sentence !== '...') {
      window.speechCtrl.speak(sentence);
      window.API.recordMetric('speak_message', sentence);
    }
  }

  if (speakMainBtn) speakMainBtn.addEventListener('click', speakConstructedMessage);
  if (speakInlineBtn) speakInlineBtn.addEventListener('click', speakConstructedMessage);
  if (clearMainBtn) clearMainBtn.addEventListener('click', clearMessage);

  // 5. Frases Rápidas
  async function loadQuickPhrases() {
    if (!quickPhrasesListEl) return;
    const phrases = await window.API.getQuickPhrases(state.currentProfileId);
    quickPhrasesListEl.innerHTML = '';

    phrases.forEach((qp) => {
      const item = document.createElement('div');
      item.className = 'quick-phrase-item';
      item.innerHTML = `
        <span class="quick-phrase-text">${qp.text}</span>
        <button class="quick-phrase-btn" aria-label="Reproduzir ${qp.text}">▶</button>
      `;

      item.addEventListener('click', () => {
        window.speechCtrl.speak(qp.spoken_text || qp.text);
        window.API.recordMetric('quick_phrase', qp.text);
      });

      quickPhrasesListEl.appendChild(item);
    });
  }

  // 6. Controles de Acessibilidade
  if (btnContrastToggle) {
    btnContrastToggle.addEventListener('click', () => {
      state.isHighContrast = !state.isHighContrast;
      document.body.classList.toggle('high-contrast', state.isHighContrast);
      renderSymbolsGrid();
    });
  }

  if (btnFontInc) {
    btnFontInc.addEventListener('click', () => {
      if (document.body.classList.contains('symbol-small')) {
        document.body.classList.remove('symbol-small');
      } else {
        document.body.classList.add('symbol-large');
      }
    });
  }

  if (btnFontDec) {
    btnFontDec.addEventListener('click', () => {
      if (document.body.classList.contains('symbol-large')) {
        document.body.classList.remove('symbol-large');
      } else {
        document.body.classList.add('symbol-small');
      }
    });
  }

  // Carregamento Inicial
  await initProfiles();
  await initCategories();
  await loadQuickPhrases();
});
