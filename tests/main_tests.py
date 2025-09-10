import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_chat_async():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://localhost:8000") as ac:
        response = await ac.post("/chat", json={"user_input": "please show me all the users"})
    assert response.status_code == 200