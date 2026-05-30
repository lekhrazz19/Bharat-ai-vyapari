from app.workflow.context import WorkflowContext
from app.renderer.pdf_renderer import html_files_to_pdf


async def generate_pdf(ctx: WorkflowContext) -> WorkflowContext:
    ctx.pdf_path = await html_files_to_pdf(ctx.rendered_html_files, ctx.proposal_id)
    ctx.status = "pdf_generated"
    return ctx
