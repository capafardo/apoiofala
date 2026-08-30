/**
 * CAA-Lab - Modo Profissional (Lógica de Gestão, Biblioteca e Drag-and-Drop)
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Estado Local do Profissional
  const state = {
    profiles: [],
    selectedProfileId: null,
    categories: [],
    selectedCategoryId: null,
    librarySymbols: [],
    categorySymbols: [],
    selectedSymbolIds: new Set(),
  };

  // Tabs
  const tabBtns = document.querySelectorAll('.prof-tab-btn');
  const tabContents = document.querySelectorAll('.prof-tab-content');

  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const tabId = btn.getAttribute('data-tab');
      tabBtns.forEach((b) => b.classList.remove('active'));
      tabContents.forEach((c) => c.classList.remove('active'));
      btn.classList.add('active');
      const targetContent = document.getElementById(tabId);
      if (targetContent) targetContent.classList.add('active');
    });
  });

  // 1. Carregar Perfis
  async function loadProfiles() {
    state.profiles = await window.API.getProfiles();
    const selectEl = document.getElementById('admin-profile-select');
    const profileManageSelect = document.getElementById('manage-profile-select');

    if (selectEl) {
      selectEl.innerHTML = '';
      state.profiles.forEach((p) => {
        const opt = document.createElement('option');
        opt.value = p.id;
        const childNick = p.child_nickname ? ` (${p.child_nickname})` : '';
        const guardianNick = p.guardian_nickname ? ` - Resp: ${p.guardian_nickname}` : '';
        opt.textContent = `${p.name}${childNick}${guardianNick}`;
        selectEl.appendChild(opt);
      });

      if (!state.selectedProfileId && state.profiles.length > 0) {
        state.selectedProfileId = state.profiles[0].id;
      }
      selectEl.value = state.selectedProfileId;

      selectEl.onchange = () => {
        state.selectedProfileId = parseInt(selectEl.value);
        loadCategorySymbols();
      };
    }

    if (profileManageSelect) {
      profileManageSelect.innerHTML = '';
      state.profiles.forEach((p) => {
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = `${p.name} (${p.child_nickname || 'Criança'})`;
        profileManageSelect.appendChild(opt);
      });
      profileManageSelect.value = state.selectedProfileId;
      profileManageSelect.onchange = () => {
        populateProfileForm(parseInt(profileManageSelect.value));
      };
      if (state.selectedProfileId) {
        populateProfileForm(state.selectedProfileId);
      }
    }
  }

  function populateProfileForm(profileId) {
    const p = state.profiles.find((x) => x.id === profileId);
    if (!p) return;

    const nameInput = document.getElementById('edit-profile-name');
    const childNickInput = document.getElementById('edit-child-nickname');
    const guardianNickInput = document.getElementById('edit-guardian-nickname');
    const sizeSelect = document.getElementById('edit-symbol-size');
    const pageSelect = document.getElementById('edit-page-items');
    const speedInput = document.getElementById('edit-voice-speed');

    if (nameInput) nameInput.value = p.name;
    if (childNickInput) childNickInput.value = p.child_nickname || '';
    if (guardianNickInput) guardianNickInput.value = p.guardian_nickname || '';
    if (sizeSelect) sizeSelect.value = p.symbol_size;
    if (pageSelect) pageSelect.value = p.symbols_per_page;
    if (speedInput) speedInput.value = p.voice_speed;
  }

  // 2. Carregar Categorias
  async function loadCategories() {
    state.categories = await window.API.getCategories();
    const selectEl = document.getElementById('admin-category-select');
    if (selectEl) {
      selectEl.innerHTML = '';
      state.categories.forEach((cat) => {
        const opt = document.createElement('option');
        opt.value = cat.id;
        opt.textContent = cat.name;
        selectEl.appendChild(opt);
      });

      if (!state.selectedCategoryId && state.categories.length > 0) {
        state.selectedCategoryId = state.categories[0].id;
      }
      selectEl.value = state.selectedCategoryId;

      selectEl.onchange = () => {
        state.selectedCategoryId = parseInt(selectEl.value);
        loadCategorySymbols();
      };
    }
  }

  // 3. Carregar Biblioteca de Símbolos
  async function loadLibrarySymbols() {
    const searchInput = document.getElementById('library-search-input');
    const searchTerm = searchInput ? searchInput.value : '';
    state.librarySymbols = await window.API.getLibrarySymbols(searchTerm);
    renderLibraryGrid();
  }

  function renderLibraryGrid() {
    const grid = document.getElementById('library-symbols-grid');
    if (!grid) return;
    grid.innerHTML = '';

    state.librarySymbols.forEach((sym) => {
      const card = document.createElement('div');
      card.className = `symbol-card ${state.selectedSymbolIds.has(sym.id) ? 'selected-for-drag' : ''}`;
      card.draggable = true;
      card.dataset.symbolId = sym.id;
      if (sym.bg_color) card.style.backgroundColor = sym.bg_color;

      card.innerHTML = `
        <div class="symbol-img-wrap">
          <img src="${sym.image_path}" alt="${sym.text_label}" />
        </div>
        <div class="symbol-label">${sym.text_label}</div>
      `;

      // Seleção / Deseleção
      card.addEventListener('click', (e) => {
        if (state.selectedSymbolIds.has(sym.id)) {
          state.selectedSymbolIds.delete(sym.id);
        } else {
          state.selectedSymbolIds.add(sym.id);
        }
        updateSelectionToolbar();
        renderLibraryGrid();
      });

      // Dragstart
      card.addEventListener('dragstart', (e) => {
        if (!state.selectedSymbolIds.has(sym.id)) {
          state.selectedSymbolIds.add(sym.id);
        }
        card.classList.add('dragging');
        const idsArray = Array.from(state.selectedSymbolIds);
        e.dataTransfer.setData('text/plain', JSON.stringify(idsArray));
        e.dataTransfer.effectAllowed = 'copy';
      });

      card.addEventListener('dragend', () => {
        card.classList.remove('dragging');
      });

      grid.appendChild(card);
    });
  }

  function updateSelectionToolbar() {
    const countEl = document.getElementById('selected-symbols-count');
    const addBtn = document.getElementById('btn-add-selected-to-category');
    if (countEl) countEl.textContent = `${state.selectedSymbolIds.size} selecionado(s)`;
    if (addBtn) {
      addBtn.disabled = state.selectedSymbolIds.size === 0;
      addBtn.textContent = `➕ Adicionar Selecionados (${state.selectedSymbolIds.size})`;
    }
  }

  // 4. Carregar Símbolos da Categoria do Perfil Selecionado
  async function loadCategorySymbols() {
    if (!state.selectedProfileId || !state.selectedCategoryId) return;
    state.categorySymbols = await window.API.getSymbols(state.selectedCategoryId, state.selectedProfileId);
    renderCategoryDropZone();
  }

  function renderCategoryDropZone() {
    const zone = document.getElementById('category-drop-zone');
    const catNameEl = document.getElementById('target-category-name');
    if (!zone) return;

    const currentCat = state.categories.find((c) => c.id === state.selectedCategoryId);
    if (catNameEl && currentCat) {
      catNameEl.textContent = `Prancha da Categoria: ${currentCat.name}`;
    }

    zone.innerHTML = '';
    if (state.categorySymbols.length === 0) {
      zone.innerHTML = '<div style="grid-column: 1/-1; text-align: center; color: #64748b; padding: 40px;">Arraste e solte símbolos aqui da Biblioteca ou use o botão para adicionar.</div>';
      return;
    }

    state.categorySymbols.forEach((sym, idx) => {
      const card = document.createElement('div');
      card.className = 'symbol-card';
      card.style.position = 'relative';
      if (sym.bg_color) card.style.backgroundColor = sym.bg_color;

      card.innerHTML = `
        <button class="remove-btn" title="Remover da categoria" style="position: absolute; top: -6px; right: -6px; background: #ef4444; color: white; border: none; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; cursor: pointer; display: flex; align-items: center; justify-content: center;">×</button>
        <div class="symbol-img-wrap">
          <img src="${sym.image_path}" alt="${sym.text_label}" />
        </div>
        <div class="symbol-label">${sym.text_label}</div>
      `;

      card.querySelector('.remove-btn').addEventListener('click', async (e) => {
        e.stopPropagation();
        // Remove da prancha
        const updatedIds = state.categorySymbols.filter((s) => s.id !== sym.id).map((s) => s.id);
        await window.API.assignSymbolsToProfileCategory(state.selectedProfileId, state.selectedCategoryId, updatedIds);
        loadCategorySymbols();
      });

      zone.appendChild(card);
    });
  }

  // Setup do Drop-Zone
  const dropZone = document.getElementById('category-drop-zone');
  if (dropZone) {
    dropZone.addEventListener('dragover', (e) => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'copy';
      dropZone.classList.add('drag-over');
    });

    dropZone.addEventListener('dragleave', () => {
      dropZone.classList.remove('drag-over');
    });

    dropZone.addEventListener('drop', async (e) => {
      e.preventDefault();
      dropZone.classList.remove('drag-over');

      try {
        const data = e.dataTransfer.getData('text/plain');
        const symbolIds = JSON.parse(data);
        if (Array.isArray(symbolIds) && symbolIds.length > 0) {
          await window.API.addSymbolsToProfileCategory(state.selectedProfileId, state.selectedCategoryId, symbolIds);
          state.selectedSymbolIds.clear();
          updateSelectionToolbar();
          renderLibraryGrid();
          loadCategorySymbols();
        }
      } catch (err) {
        console.error('Erro ao processar drop:', err);
      }
    });
  }

  // Botão Adicionar Selecionados
  const btnAddSelected = document.getElementById('btn-add-selected-to-category');
  if (btnAddSelected) {
    btnAddSelected.addEventListener('click', async () => {
      const ids = Array.from(state.selectedSymbolIds);
      if (ids.length > 0) {
        await window.API.addSymbolsToProfileCategory(state.selectedProfileId, state.selectedCategoryId, ids);
        state.selectedSymbolIds.clear();
        updateSelectionToolbar();
        renderLibraryGrid();
        loadCategorySymbols();
      }
    });
  }

  // Busca na Biblioteca
  const searchInput = document.getElementById('library-search-input');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      loadLibrarySymbols();
    });
  }

  // 5. Salvar Perfil Editado
  const btnSaveEdit = document.getElementById('btn-save-profile-edit');
  if (btnSaveEdit) {
    btnSaveEdit.addEventListener('click', async () => {
      const nameInput = document.getElementById('edit-profile-name');
      const childNickInput = document.getElementById('edit-child-nickname');
      const guardianNickInput = document.getElementById('edit-guardian-nickname');
      const sizeSelect = document.getElementById('edit-symbol-size');
      const pageSelect = document.getElementById('edit-page-items');
      const speedInput = document.getElementById('edit-voice-speed');

      await window.API.updateProfile(state.selectedProfileId, {
        name: nameInput.value,
        child_nickname: childNickInput.value,
        guardian_nickname: guardianNickInput.value,
        symbol_size: sizeSelect.value,
        symbols_per_page: parseInt(pageSelect.value),
        voice_speed: parseFloat(speedInput.value),
      });

      alert('Perfil atualizado com sucesso!');
      await loadProfiles();
    });
  }

  // 6. Criar Novo Perfil
  const formNewProfile = document.getElementById('form-new-profile');
  if (formNewProfile) {
    formNewProfile.addEventListener('submit', async (e) => {
      e.preventDefault();
      const childNick = document.getElementById('new-child-nickname').value;
      const guardianNick = document.getElementById('new-guardian-nickname').value;
      const fullName = document.getElementById('new-profile-name').value || childNick;
      const size = document.getElementById('new-symbol-size').value;
      const items = parseInt(document.getElementById('new-page-items').value);
      const speed = parseFloat(document.getElementById('new-voice-speed').value);

      const newP = await window.API.createProfile({
        name: fullName,
        child_nickname: childNick,
        guardian_nickname: guardianNick,
        symbol_size: size,
        symbols_per_page: items,
        voice_speed: speed,
      });

      if (newP) {
        alert(`Perfil de "${childNick}" criado com sucesso!`);
        formNewProfile.reset();
        state.selectedProfileId = newP.id;
        await loadProfiles();
        loadCategorySymbols();
      }
    });
  }

  // 7. Dashboard de Métricas
  async function loadDashboard() {
    const summary = await window.API.getMetricsSummary();
    if (!summary) return;

    const elUsers = document.getElementById('stat-active-users');
    const elMessages = document.getElementById('stat-messages-today');
    const elTouches = document.getElementById('stat-touches-today');
    const elPhrases = document.getElementById('stat-favorite-phrases');

    if (elUsers) elUsers.textContent = summary.total_active_users;
    if (elMessages) elMessages.textContent = summary.total_messages_today;
    if (elTouches) elTouches.textContent = summary.total_touches_today;
    if (elPhrases) elPhrases.textContent = summary.total_favorite_phrases;

    const topMsgContainer = document.getElementById('top-messages-list');
    if (topMsgContainer && summary.top_used_messages) {
      topMsgContainer.innerHTML = '';
      summary.top_used_messages.forEach((item) => {
        const row = document.createElement('div');
        row.style.display = 'flex';
        row.style.justifyContent = 'space-between';
        row.style.padding = '8px 0';
        row.style.borderBottom = '1px solid #f1f5f9';
        row.innerHTML = `<span>${item.phrase}</span><strong style="color: var(--primary);">${item.count}x</strong>`;
        topMsgContainer.appendChild(row);
      });
    }
  }

  // Inicializar tudo
  await loadProfiles();
  await loadCategories();
  await loadLibrarySymbols();
  await loadCategorySymbols();
  await loadDashboard();
});
