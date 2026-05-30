import httpx
from app.config import settings


async def call_openrouter(system_prompt: str, user_prompt: str, model: str | None = None, json_mode: bool = True) -> str:
    if not settings.OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not configured")

    api_key = settings.OPENROUTER_API_KEY
    if api_key.startswith("Bearer "):
        api_key = api_key[7:]

    payload = {
        "model": model or settings.OPENROUTER_DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    async with httpx.AsyncClient(timeout=100) as client:
        response = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": settings.APP_BASE_URL,
                "X-Title": "Bharat AI Vyapari Proposal Engine",
            },
            json=payload,
        )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]
