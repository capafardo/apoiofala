/**
 * CAA-Lab - Cliente de API REST Local
 */

const API = {
  async getCategories() {
    try {
      const res = await fetch('/api/v1/categories');
      if (!res.ok) throw new Error('Erro ao obter categorias');
      return await res.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  async getSymbols(categoryId = null, profileId = null, search = '') {
    try {
      let url = '/api/v1/symbols?';
      if (categoryId) url += `category_id=${categoryId}&`;
      if (profileId) url += `profile_id=${profileId}&`;
      if (search) url += `search=${encodeURIComponent(search)}&`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Erro ao obter símbolos');
      return await res.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  async getLibrarySymbols(search = '') {
    try {
      let url = '/api/v1/symbols/library';
      if (search) url += `?search=${encodeURIComponent(search)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Erro ao obter biblioteca de símbolos');
      return await res.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  async assignSymbolsToProfileCategory(profileId, categoryId, symbolIds) {
    try {
      const res = await fetch(`/api/v1/symbols/profiles/${profileId}/categories/${categoryId}/assign`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol_ids: symbolIds }),
      });
      return await res.json();
    } catch (e) {
      console.error(e);
      return { status: 'error' };
    }
  },

  async addSymbolsToProfileCategory(profileId, categoryId, symbolIds) {
    try {
      const res = await fetch(`/api/v1/symbols/profiles/${profileId}/categories/${categoryId}/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol_ids: symbolIds }),
      });
      return await res.json();
    } catch (e) {
      console.error(e);
      return { status: 'error' };
    }
  },

  async getQuickPhrases(profileId = null) {
    try {
      let url = '/api/v1/quick-phrases';
      if (profileId) url += `?profile_id=${profileId}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Erro ao obter frases rápidas');
      return await res.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  async getProfiles() {
    try {
      const res = await fetch('/api/v1/profiles');
      if (!res.ok) throw new Error('Erro ao obter perfis');
      return await res.json();
    } catch (e) {
      console.error(e);
      return [];
    }
  },

  async createProfile(data) {
    try {
      const res = await fetch('/api/v1/profiles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error('Erro ao criar perfil');
      return await res.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  },

  async updateProfile(profileId, data) {
    try {
      const res = await fetch(`/api/v1/profiles/${profileId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      return await res.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  },

  async getMetricsSummary() {
    try {
      const res = await fetch('/api/v1/metrics/summary');
      if (!res.ok) throw new Error('Erro ao obter métricas');
      return await res.json();
    } catch (e) {
      console.error(e);
      return null;
    }
  },

  async recordMetric(actionType, referenceId = null, categoryId = null) {
    try {
      await fetch('/api/v1/metrics/event', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          action_type: actionType,
          reference_id: String(referenceId || ''),
          category_id: categoryId,
        }),
      });
    } catch (e) {
      // Falha de métrica é silenciosa
    }
  },
};

window.API = API;
