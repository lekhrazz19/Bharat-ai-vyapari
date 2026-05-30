import httpx
from bs4 import BeautifulSoup


async def fetch_website_text(url: str) -> str:
    if not url:
        return ""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
            response = await client.get(url, headers={"User-Agent": "BAVProposalBot/1.0"})
        response.raise_for_status()
    except Exception as e:
        return f"Website fetch failed: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style", "noscript", "svg"]):
        tag.extract()
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    meta_desc = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        meta_desc = meta["content"].strip()
    text = " ".join(soup.get_text(separator=" ").split())
    return f"Title: {title}\nMeta: {meta_desc}\nText: {text[:10000]}"
