from app.workflow.context import WorkflowContext
from app.renderer.html_renderer import render_all_pages


async def render_html(ctx: WorkflowContext) -> WorkflowContext:
    ctx.rendered_html_files = render_all_pages(ctx.proposal_json, ctx.proposal_id)
    ctx.status = "html_rendered"
    return ctx
