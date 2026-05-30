from app.workflow.context import WorkflowContext
from app.services.email_service import send_proposal_email


async def send_email(ctx: WorkflowContext) -> WorkflowContext:
    meta = ctx.proposal_json.get("proposalMeta", {})
    await send_proposal_email(
        to_email=ctx.client_email or meta.get("clientEmail"),
        client_name=meta.get("clientName") or ctx.normalized_input.get("client_name"),
        company_name=meta.get("clientCompanyName") or ctx.normalized_input.get("company_name"),
        pdf_path=ctx.pdf_path,
    )
    ctx.status = "sent"
    return ctx
