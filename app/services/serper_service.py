import httpx
from app.config import settings


async def serper_search(query: str) -> dict:
    if not settings.SERPER_API_KEY:
        return {}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            "https://google.serper.dev/search",
            headers={"X-API-KEY": settings.SERPER_API_KEY, "Content-Type": "application/json"},
            json={"q": query, "num": 5},
        )
    response.raise_for_status()
    return response.json()
