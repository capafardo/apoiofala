"""Testes de integração para métricas anônimas."""

import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from app.core.init_db import init_db


@pytest.fixture(autouse=True)
def setup_db():
    init_db()


@pytest.mark.asyncio
async def test_record_and_summary_metrics():
    """Valida registro e resumo de métricas técnicas."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # Registrar evento de toque
        post_res = await client.post(
            "/api/v1/metrics/event",
            json={"action_type": "touch_symbol", "reference_id": "agua"},
        )
        assert post_res.status_code == 200

        # Obter resumo
        res = await client.get("/api/v1/metrics/summary")
        assert res.status_code == 200
        data = res.json()
        assert data["total_active_users"] >= 1
        assert "usage_by_category" in data
