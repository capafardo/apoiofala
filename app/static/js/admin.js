/**
 * CAA-Lab - Modo Profissional (Lógica de Gestão e Dashboard)
 */

document.addEventListener('DOMContentLoaded', async () => {
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

  // Carregar Métricas do Painel
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

    // Mensagens mais usadas
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

  // Carregar Vocabulário para Gestão
  async function loadVocabularyManagement() {
    const vocabGrid = document.getElementById('admin-vocab-grid');
    if (!vocabGrid) return;

    const symbols = await window.API.getSymbols();
    vocabGrid.innerHTML = '';

    symbols.forEach((sym) => {
      const card = document.createElement('div');
      card.className = 'symbol-card';
      card.style.position = 'relative';
      if (sym.bg_color) card.style.backgroundColor = sym.bg_color;

      card.innerHTML = `
        <div class="symbol-img-wrap">
          <img src="${sym.image_path}" alt="${sym.text_label}" />
        </div>
        <div class="symbol-label">${sym.text_label}</div>
      `;

      vocabGrid.appendChild(card);
    });
  }

  // Carregar Perfil para Edição
  async function loadProfileSettings() {
    const profiles = await window.API.getProfiles();
    if (!profiles || profiles.length === 0) return;

    const profile = profiles[0]; // João Pedro
    const nameInput = document.getElementById('profile-name');
    const sizeSelect = document.getElementById('profile-symbol-size');
    const pageItemsSelect = document.getElementById('profile-page-items');
    const speedInput = document.getElementById('profile-voice-speed');

    if (nameInput) nameInput.value = profile.name;
    if (sizeSelect) sizeSelect.value = profile.symbol_size;
    if (pageItemsSelect) pageItemsSelect.value = profile.symbols_per_page;
    if (speedInput) speedInput.value = profile.voice_speed;

    const saveBtn = document.getElementById('btn-save-profile');
    if (saveBtn) {
      saveBtn.addEventListener('click', async () => {
        await window.API.updateProfile(profile.id, {
          name: nameInput ? nameInput.value : profile.name,
          symbol_size: sizeSelect ? sizeSelect.value : profile.symbol_size,
          symbols_per_page: pageItemsSelect ? parseInt(pageItemsSelect.value) : profile.symbols_per_page,
          voice_speed: speedInput ? parseFloat(speedInput.value) : profile.voice_speed,
        });
        alert('Configurações do perfil salvas com sucesso!');
      });
    }
  }

  await loadDashboard();
  await loadVocabularyManagement();
  await loadProfileSettings();
});
