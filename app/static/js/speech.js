/**
 * CAA-Lab - Módulo de Síntese de Voz (TTS Local / Offline)
 * Utiliza a Web Speech API nativa do navegador com controle de tom e velocidade.
 */

class SpeechController {
  constructor() {
    this.synth = window.speechSynthesis || null;
    this.voices = [];
    this.selectedVoice = null;
    this.rate = 1.0;
    this.pitch = 1.0;
    this.language = 'pt-BR';

    this.initVoices();
  }

  initVoices() {
    if (!this.synth) {
      console.warn('Web Speech API não disponível neste navegador.');
      return;
    }

    const updateVoices = () => {
      this.voices = this.synth.getVoices();
      // Priorizar voz em português do Brasil
      this.selectedVoice =
        this.voices.find((v) => v.lang === 'pt-BR' || v.lang === 'pt_BR') ||
        this.voices.find((v) => v.lang.startsWith('pt')) ||
        this.voices[0] ||
        null;
    };

    updateVoices();
    if (this.synth.onvoiceschanged !== undefined) {
      this.synth.onvoiceschanged = updateVoices;
    }
  }

  setSpeed(rate) {
    this.rate = Math.max(0.5, Math.min(2.0, parseFloat(rate) || 1.0));
  }

  setPitch(pitch) {
    this.pitch = Math.max(0.5, Math.min(2.0, parseFloat(pitch) || 1.0));
  }

  speak(text) {
    if (!text || !text.trim()) return Promise.resolve();

    return new Promise((resolve, reject) => {
      if (!this.synth) {
        console.log(`[Áudio Simulado]: ${text}`);
        resolve();
        return;
      }

      // Cancela qualquer fala anterior em andamento para evitar sobreposição
      this.synth.cancel();

      const utterance = new SpeechSynthesisUtterance(text.trim());
      utterance.rate = this.rate;
      utterance.pitch = this.pitch;
      utterance.lang = this.language;

      if (this.selectedVoice) {
        utterance.voice = this.selectedVoice;
      }

      utterance.onend = () => resolve();
      utterance.onerror = (err) => {
        console.warn('Erro na síntese de fala local:', err);
        resolve(); // Não quebra o fluxo em caso de falha de áudio
      };

      this.synth.speak(utterance);
    });
  }
}

// Instância global para ser utilizada em toda a aplicação
window.speechCtrl = new SpeechController();
