from app.workflow.context import WorkflowContext
from app.services.baserow_service import upsert_proposal_status
from app.utils.logger import logger


async def log_status(ctx: WorkflowContext) -> WorkflowContext:
    logger.info("Proposal %s status: %s", ctx.proposal_id, ctx.status)
    try:
        await upsert_proposal_status(ctx)
    except Exception as e:
        logger.warning("Baserow log skipped/failed: %s", e)
    return ctx
