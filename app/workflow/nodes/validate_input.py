from app.workflow.context import WorkflowContext
from app.schemas.input_schema import ProposalInput


async def validate_input(ctx: WorkflowContext) -> WorkflowContext:
    data = ctx.normalized_input or ctx.raw_input
    parsed = ProposalInput(**data)
    ctx.normalized_input = parsed.model_dump()
    ctx.client_email = parsed.client_email
    ctx.status = "input_validated"
    return ctx
