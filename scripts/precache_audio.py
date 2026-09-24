"""
Script de Pré-aquecimento do Cache de Áudio TTS.

Executado durante a instalação (quando ainda há conexão com a internet) para
gerar e armazenar em cache (assets/audio/tts-cache/) os arquivos MP3 das vozes
neurais para todos os símbolos da biblioteca e frases rápidas padrão.

Isso garante que, mesmo quando a máquina for utilizada 100% offline, os áudios
neurais dos mais de 80 símbolos e das frases comuns toquem imediatamente a partir
do disco local, com qualidade natural e sem latência.
"""

import sys
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.core.database import SessionLocal
from app.models.symbol import Symbol
from app.models.quick_phrase import QuickPhrase
from app.services import neural_tts


def precache_all():
    print("[INFO] Verificando pré-cache de síntese de voz (TTS)...")

    db = SessionLocal()
    try:
        # Coletar textos únicos de símbolos e frases rápidas
        symbols = db.query(Symbol).all()
        phrases = db.query(QuickPhrase).all()

        texts_to_cache = set()
        for s in symbols:
            text = s.spoken_text or s.text_label
            if text and text.strip():
                texts_to_cache.add(text.strip())
        for p in phrases:
            text = p.spoken_text or p.text
            if text and text.strip():
                texts_to_cache.add(text.strip())

        if not texts_to_cache:
            print("[INFO] Nenhum símbolo ou frase encontrada no banco para pré-cache.")
            return

        print(f"[INFO] {len(texts_to_cache)} expressões identificadas para verificação de áudio.")

        cached_count = 0
        generated_count = 0
        failed_count = 0

        for text in sorted(texts_to_cache):
            voice = neural_tts._voice_for_language("pt-BR")
            rate = neural_tts._rate_percent(1.0)
            cache_file = neural_tts._cache_path(text, voice, rate)

            if cache_file.is_file() and cache_file.stat().st_size > 0:
                cached_count += 1
                continue

            try:
                audio, media_type, engine = neural_tts.synthesize(text, language="pt-BR", speed=1.0)
                if engine == "edge-neural":
                    generated_count += 1
                else:
                    failed_count += 1
            except Exception:
                failed_count += 1

        print(
            f"[INFO] Resumo do pré-cache TTS: {cached_count} já existiam em disco, "
            f"{generated_count} recém-gerados, {failed_count} offline/não gerados."
        )
        if generated_count > 0 or cached_count > 0:
            print("[SUCESSO] Cache de áudio local pronto para operação offline!")
        else:
            print("[AVISO] Não foi possível conectar ao serviço de voz neural neste momento.")
            print("[INFO] O sistema operará normalmente usando espeak-ng/síntese do navegador.")

    except Exception as e:
        print(f"[AVISO] Falha ao executar pré-cache de áudio: {e}")
        print("[INFO] Continuando instalação (a aplicação continuará funcional via fallback local).")
    finally:
        db.close()


if __name__ == "__main__":
    precache_all()
