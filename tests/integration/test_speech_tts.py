"""Testes de integração para o endpoint de TTS (voz neural Microsoft + fallback espeak-ng)."""

import shutil

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services import neural_tts

ESPEAK = shutil.which("espeak-ng") or shutil.which("espeak")

pytestmark = pytest.mark.skipif(
    ESPEAK is None, reason="Sintetizador espeak-ng não instalado no sistema"
)


@pytest.mark.asyncio
async def test_tts_default_returns_audio():
    """Valida se GET /api/v1/speech/tts retorna MP3 (neural) ou WAV (fallback)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/speech/tts", params={"text": "olá, eu quero água"})
        assert res.status_code == 200
        content_type = res.headers["content-type"]
        assert content_type in ("audio/mpeg", "audio/wav")

        if content_type == "audio/mpeg":
            # Voz neural da Microsoft (ou cache em disco)
            assert res.headers.get("x-tts-engine") == "edge-neural"
        else:
            # Fallback offline (espeak-ng)
            assert res.content[:4] == b"RIFF"


@pytest.mark.asyncio
async def test_tts_neural_engine_returns_mp3(monkeypatch):
    """Com engine=neural, usa a voz neural da Microsoft (MP3), sem rede real."""
    async def fake_synthesize(text, language="pt-BR", speed=1.0):
        return b"ID3\x03\x00fake-mp3-audio", "audio/mpeg", "edge-neural"

    monkeypatch.setattr(neural_tts, "synthesize_async", fake_synthesize)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(
            "/api/v1/speech/tts",
            params={"text": "teste neural", "engine": "neural"},
        )
        assert res.status_code == 200
        assert res.headers["content-type"] == "audio/mpeg"
        assert res.headers.get("x-tts-engine") == "edge-neural"


@pytest.mark.asyncio
async def test_tts_neural_failure_falls_back_to_espeak(monkeypatch):
    """Sem conectividade neural, o modo 'auto' cai para o espeak-ng offline (WAV)."""
    async def broken_synthesize(text, language="pt-BR", speed=1.0):
        raise RuntimeError("sem conexão com o serviço de TTS")

    monkeypatch.setattr(neural_tts, "synthesize_async", broken_synthesize)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/speech/tts", params={"text": "fallback offline"})
        assert res.status_code == 200
        assert res.headers["content-type"] == "audio/wav"
        assert res.headers.get("x-tts-engine") == "espeak-ng"
        assert res.content[:4] == b"RIFF"


@pytest.mark.asyncio
async def test_tts_neural_failure_strict_engine_fails(monkeypatch):
    """Com engine=neural, falha do serviço retorna 503 (sem fallback silencioso)."""
    async def broken_synthesize(text, language="pt-BR", speed=1.0):
        raise RuntimeError("sem conexão com o serviço de TTS")

    monkeypatch.setattr(neural_tts, "synthesize_async", broken_synthesize)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(
            "/api/v1/speech/tts",
            params={"text": "fallback offline", "engine": "neural"},
        )
        assert res.status_code == 503


@pytest.mark.asyncio
async def test_tts_espeak_engine_returns_wav():
    """Com engine=espeak, usa síntese 100% offline (WAV via espeak-ng)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(
            "/api/v1/speech/tts",
            params={"text": "teste offline", "engine": "espeak", "speed": 1.5},
        )
        assert res.status_code == 200
        assert res.headers["content-type"] == "audio/wav"
        assert res.content[:4] == b"RIFF"


@pytest.mark.asyncio
async def test_tts_rejects_blank_text():
    """Valida rejeição de texto vazio/branco."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get("/api/v1/speech/tts", params={"text": "   "})
        assert res.status_code == 400


@pytest.mark.asyncio
async def test_tts_rejects_invalid_engine():
    """Valida rejeição de motor inválido (enum do FastAPI)."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.get(
            "/api/v1/speech/tts",
            params={"text": "oi", "engine": "xyz"},
        )
        assert res.status_code == 422


def test_neural_rate_mapping_and_cache(monkeypatch, tmp_path):
    """Valida mapeamento de velocidade, voz pt-BR e cache em disco do provedor neural."""
    class FakeCommunicate:
        def __init__(self, text, voice="pt-BR-FranciscaNeural", rate="+0%"):
            self.text = text
            self.voice = voice
            self.rate = rate

        async def stream(self):
            yield {"type": "audio", "data": b"mp3-bytes"}

    monkeypatch.setattr(neural_tts.edge_tts, "Communicate", FakeCommunicate)
    monkeypatch.setattr(neural_tts, "_cache_dir", lambda: tmp_path)

    # 1ª chamada: sintetiza (voz pt-BR padrão, rate mapeado de 1.5 → +50%)
    audio, media_type, engine = neural_tts.synthesize("bom dia", "pt-BR", 1.5)
    assert engine == "edge-neural"
    assert media_type == "audio/mpeg"
    assert audio == b"mp3-bytes"

    # 2ª chamada: servida do cache em disco (sem nova síntese)
    audio2, _, engine2 = neural_tts.synthesize("bom dia", "pt-BR", 1.5)
    assert engine2 == "edge-neural"
    assert audio2 == b"mp3-bytes"
    assert len(list(tmp_path.glob("*.mp3"))) == 1


def test_offline_mode_bypasses_network_to_espeak(monkeypatch, tmp_path):
    """Com TTS_OFFLINE_MODE=True, a síntese pula requisições de rede e vai direto ao espeak."""
    monkeypatch.setattr(neural_tts.settings, "TTS_OFFLINE_MODE", True)
    monkeypatch.setattr(neural_tts, "_cache_dir", lambda: tmp_path)

    audio, media_type, engine = neural_tts.synthesize("frase nova sem cache", "pt-BR", 1.0)
    assert engine == "espeak-ng"
    assert media_type == "audio/wav"
    assert audio[:4] == b"RIFF"


def test_circuit_breaker_bypasses_after_failure(monkeypatch, tmp_path):
    """Após falha na tentativa online, as chamadas subsequentes caem direto no espeak sem esperar."""
    monkeypatch.setattr(neural_tts, "_cache_dir", lambda: tmp_path)
    # Simula última falha recente (5 segundos atrás)
    monkeypatch.setattr(neural_tts, "_LAST_NETWORK_FAILURE", neural_tts.time.monotonic() - 5.0)

    audio, media_type, engine = neural_tts.synthesize("outra frase", "pt-BR", 1.0)
    assert engine == "espeak-ng"
    assert media_type == "audio/wav"
