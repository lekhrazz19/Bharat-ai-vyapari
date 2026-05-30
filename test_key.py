import httpx
import asyncio
from app.config import settings

async def verify_key():
    key = settings.OPENROUTER_API_KEY
    # Strip Bearer prefix if it somehow got included
    if key.startswith("Bearer "):
        key = key[7:]
        
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "google/gemini-2.5-flash",
        "messages": [{"role": "user", "content": "hi"}],
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            if response.status_code == 401:
                print("\n[WARNING] The OpenRouter API Key provided appears to be invalid or expired (401 Unauthorized).")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_key())
