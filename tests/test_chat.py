import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app

@pytest.mark.asyncio
async def test_send_and_history(async_client, auth_header):
    payload = {"title": "Demo", "message": "Olá", "model": "gpt-4o", "temperature": 0.7, "max_tokens": 512}
    send_res = await async_client.post("/api/chat/send", json=payload, headers=auth_header)
    assert send_res.status_code == 200
    conv_id = send_res.json()["conversation_id"]

    history_res = await async_client.get(f"/api/chat/history/{conv_id}", headers=auth_header)
    assert history_res.status_code == 200
    assert len(history_res.json()) >= 2