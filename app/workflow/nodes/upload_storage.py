from pathlib import Path
from app.config import settings
from app.workflow.context import WorkflowContext


async def upload_storage(ctx: WorkflowContext) -> WorkflowContext:
    # MVP local storage. Swap this service for Google Drive/R2 later.
    if ctx.pdf_path:
        ctx.pdf_url = f"{settings.PUBLIC_FILE_BASE_URL}/{Path(ctx.pdf_path).name}"
    ctx.status = "pending_approval"
    return ctx
