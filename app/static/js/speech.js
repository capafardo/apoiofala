/**
 * CAA-Lab - Módulo de Síntese de Voz (TTS Neural Microsoft / Azure)
 *
 * Estratégia em camadas:
 *  1. TTS do backend com **voz neural da Microsoft** (Azure Neural TTS via
 *     edge-tts — gratuita, sem chave de API) com cache local no servidor e
 *     cache de áudio no navegador (frases repetidas tocam instantaneamente);
 *  2. Fallback: Web Speech API local do navegador caso o backend falhe;
 *  3. Último recurso do backend (offline): espeak-ng — o som sempre toca.
 *
 * A voz neural substitui a voz robotizada do espeak/speech-dispatcher que o
 * Chromium costuma expor no Linux.
 */

class SpeechController {
  constructor() {
    // Web Speech API mantida apenas como fallback local
    this.synth = window.speechSynthesis || null;
    this.voices = [];
    this.selectedVoice = null;

    this.rate = 1.0;
    this.pitch = 1.0; // mantido para compatibilidade (usado só no fallback local)
    this.language = 'pt-BR';

    this.audioEl = null;
    this._cache = new Map(); // url da requisição → Promise<ObjectURL>

    this._initLocalFallback();
  }

  // ------------------------------------------------------------------
  // Fallback local (Web Speech API) — usado só se o backend falhar
  // ------------------------------------------------------------------
  _initLocalFallback() {
    if (!this.synth) return;

    const refresh = () => {
      this.voices = this.synth.getVoices() || [];
      this.selectedVoice =
        this.voices.find((v) => v.lang === 'pt-BR' || v.lang === 'pt_BR') ||
        this.voices.find((v) => (v.lang || '').toLowerCase().startsWith('pt')) ||
        this.voices[0] ||
        null;
    };

    refresh();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = refresh;
    }
  }

  // ------------------------------------------------------------------
  // API pública (compatível com app.js)
  // ------------------------------------------------------------------
  setSpeed(rate) {
    this.rate = Math.max(0.5, Math.min(2.0, parseFloat(rate) || 1.0));
  }

  setPitch(pitch) {
    this.pitch = Math.max(0.5, Math.min(2.0, parseFloat(pitch) || 1.0));
  }

  speak(text) {
    if (!text || !text.trim()) return Promise.resolve();
    const clean = text.trim();

    // Prioridade: voz neural da Microsoft (backend) → fallback local
    return this._speakBackend(clean).catch((err) => {
      console.warn('TTS neural indisponível; usando voz local do navegador:', err);
      return this._speakLocal(clean);
    });
  }

  // ------------------------------------------------------------------
  // Camada 1: voz neural da Microsoft via backend (com cache)
  // ------------------------------------------------------------------
  _backendUrl(text) {
    return (
      `/api/v1/speech/tts?text=${encodeURIComponent(text)}` +
      `&speed=${encodeURIComponent(this.rate)}` +
      `&language=${encodeURIComponent(this.language)}`
    );
  }

  _getAudioUrl(url) {
    if (!this._cache.has(url)) {
      this._cache.set(
        url,
        fetch(url)
          .then((res) => {
            if (!res.ok) throw new Error(`TTS backend HTTP ${res.status}`);
            return res.blob();
          })
          .then((blob) => URL.createObjectURL(blob))
          .catch((err) => {
            this._cache.delete(url); // permite nova tentativa depois
            throw err;
          })
      );
    }
    return this._cache.get(url);
  }

  _speakBackend(text) {
    return this._getAudioUrl(this._backendUrl(text)).then(
      (blobUrl) =>
        new Promise((resolve, reject) => {
          const audio = new Audio(blobUrl);
          audio.playbackRate = this.rate;

          const cleanup = () => {
            audio.onended = null;
            audio.onerror = null;
          };

          audio.onended = () => {
            cleanup();
            resolve();
          };

          audio.onerror = () => {
            cleanup();
            reject(new Error("Falha ao decodificar/reproduzir áudio do backend"));
          };

          const playPromise = audio.play();
          if (playPromise && typeof playPromise.catch === "function") {
            playPromise.catch((err) => {
              cleanup();
              reject(err);
            });
          }
        })
    );
  }

  // ------------------------------------------------------------------
  // Camada 2 (fallback): Web Speech API local do navegador
  // ------------------------------------------------------------------
  _speakLocal(text) {
    if (!this.synth) return Promise.resolve();

    return new Promise((resolve) => {
      try {
        this.synth.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = this.rate;
        utterance.pitch = this.pitch;
        utterance.lang = this.language;
        if (this.selectedVoice) utterance.voice = this.selectedVoice;

        utterance.onend = () => resolve();
        utterance.onerror = () => resolve();
        this.synth.speak(utterance);
      } catch (err) {
        console.warn("Erro ao sintetizar no navegador:", err);
        resolve();
      }
    });
  }
}

// Instância global para ser utilizada em toda a aplicação
window.speechCtrl = new SpeechController();
