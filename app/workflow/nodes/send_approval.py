from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from app.config import settings
from app.workflow.context import WorkflowContext


async def send_approval(ctx: WorkflowContext) -> WorkflowContext:
    if not settings.TELEGRAM_BOT_TOKEN or not settings.ADMIN_TELEGRAM_CHAT_ID:
        ctx.status = "pending_approval"
        return ctx

    bot = Bot(settings.TELEGRAM_BOT_TOKEN)
    meta = ctx.proposal_json.get("proposalMeta", {})
    cp = ctx.proposal_json.get("combinedPricing", {})

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Approve & Send", callback_data=f"approve:{ctx.proposal_id}")],
        [InlineKeyboardButton("Reject", callback_data=f"reject:{ctx.proposal_id}")],
        [InlineKeyboardButton("Regenerate", callback_data=f"regenerate:{ctx.proposal_id}")],
    ])

    await bot.send_message(
        chat_id=settings.ADMIN_TELEGRAM_CHAT_ID,
        text=(
            f"Proposal ready for approval.\n\n"
            f"ID: {ctx.proposal_id}\n"
            f"Company: {meta.get('clientCompanyName')}\n"
            f"Client: {meta.get('clientName')}\n"
            f"Setup: {cp.get('setupCostTotal')}\n"
            f"Monthly: {cp.get('monthlyCostTotal')}\n"
            f"PDF: {ctx.pdf_url or ctx.pdf_path}"
        ),
        reply_markup=keyboard,
    )
    ctx.status = "pending_approval"
    return ctx
