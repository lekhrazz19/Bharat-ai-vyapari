from telegram import Update
from telegram.ext import ContextTypes

from app.workflow.nodes.log_status import log_status
from app.workflow.nodes.send_email import send_email
from app.workflow.proposal_workflow import run_proposal_workflow
from app.workflow.store import get_workflow_context, reset_for_regeneration, save_workflow_context


async def approval_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    action, proposal_id = query.data.split(":", 1)
    ctx = get_workflow_context(proposal_id)
    if not ctx:
        await query.edit_message_text(f"Proposal not found: {proposal_id}")
        return

    if action == "approve":
        ctx.status = "approved"
        await log_status(ctx)
        try:
            ctx = await send_email(ctx)
        except Exception as e:
            ctx.status = "email_failed"
            ctx.errors.append(str(e))
            await log_status(ctx)
            save_workflow_context(ctx)
            await query.edit_message_text(f"Approved, but email failed for {proposal_id}: {e}")
            return
        await log_status(ctx)
        save_workflow_context(ctx)
        await query.edit_message_text(f"Approved and sent: {proposal_id}")
    elif action == "reject":
        ctx.status = "rejected"
        await log_status(ctx)
        save_workflow_context(ctx)
        await query.edit_message_text(f"Rejected: {proposal_id}")
    elif action == "regenerate":
        await query.edit_message_text(f"Regeneration started: {proposal_id}")
        regenerated = reset_for_regeneration(ctx)
        save_workflow_context(regenerated)
        result = await run_proposal_workflow(regenerated)
        save_workflow_context(result)
        if result.status == "failed":
            await query.message.reply_text(f"Regeneration failed: {proposal_id}")
        else:
            await query.message.reply_text(f"Regenerated: {proposal_id}\nPDF: {result.pdf_url or result.pdf_path}")
