from app.workflow.context import WorkflowContext
from app.workflow.nodes.validate_input import validate_input
from app.workflow.nodes.log_status import log_status
from app.workflow.nodes.research_company import research_company
from app.workflow.nodes.pricing_lookup import pricing_lookup
from app.workflow.nodes.generate_proposal_json import generate_proposal_json
from app.workflow.nodes.validate_trim_json import validate_trim_json
from app.workflow.nodes.render_html import render_html
from app.workflow.nodes.generate_pdf import generate_pdf
from app.workflow.nodes.upload_storage import upload_storage
from app.workflow.nodes.send_approval import send_approval
from app.workflow.store import save_workflow_context
from app.utils.logger import logger


async def run_proposal_workflow(ctx: WorkflowContext) -> WorkflowContext:
    steps = [
        validate_input,
        log_status,
        research_company,
        pricing_lookup,
        generate_proposal_json,
        validate_trim_json,
        render_html,
        generate_pdf,
        upload_storage,
        log_status,
        send_approval,
    ]

    for step in steps:
        try:
            logger.info("Running step: %s", step.__name__)
            ctx = await step(ctx)
            save_workflow_context(ctx)
        except Exception as e:
            logger.exception("Workflow step failed: %s", step.__name__)
            ctx.status = "failed"
            ctx.errors.append(f"{step.__name__}: {str(e)}")
            await log_status(ctx)
            save_workflow_context(ctx)
            break

    return ctx
