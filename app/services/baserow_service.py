import httpx
from typing import Any

from app.config import settings
from app.workflow.context import WorkflowContext


def _headers() -> dict[str, str]:
    return {"Authorization": f"Token {settings.BASEROW_API_TOKEN}"}


async def _find_existing_row_id(client: httpx.AsyncClient, proposal_id: str) -> int | None:
    url = f"{settings.BASEROW_API_URL}/database/rows/table/{settings.BASEROW_TABLE_ID}/"
    response = await client.get(
        url,
        headers=_headers(),
        params={
            "user_field_names": "true",
            f"filter__field_{settings.BASEROW_PROPOSAL_ID_FIELD}__equal": proposal_id,
            "size": 1,
        },
    )
    response.raise_for_status()
    data: dict[str, Any] = response.json()
    results = data.get("results", [])
    if not results:
        return None
    return results[0].get("id")


async def upsert_proposal_status(ctx: WorkflowContext) -> None:
    if not settings.BASEROW_API_TOKEN or not settings.BASEROW_TABLE_ID:
        return
    base_url = f"{settings.BASEROW_API_URL}/database/rows/table/{settings.BASEROW_TABLE_ID}/"
    payload = {
        "proposal_id": ctx.proposal_id,
        "status": ctx.status,
        "company_name": ctx.normalized_input.get("company_name", ""),
        "client_name": ctx.normalized_input.get("client_name", ""),
        "client_email": ctx.normalized_input.get("client_email", ""),
        "pdf_url": ctx.pdf_url or "",
        "proposal_json": ctx.proposal_json,
    }
    async with httpx.AsyncClient(timeout=30) as client:
        row_id = await _find_existing_row_id(client, ctx.proposal_id)
        if row_id:
            url = f"{base_url}{row_id}/?user_field_names=true"
            response = await client.patch(url, headers=_headers(), json=payload)
        else:
            url = f"{base_url}?user_field_names=true"
            response = await client.post(url, headers=_headers(), json=payload)
        response.raise_for_status()
