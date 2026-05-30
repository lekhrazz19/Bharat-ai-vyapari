from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from app.config import settings
from app.telegram.parser import parse_proposal_message
from app.telegram.approval import approval_callback
from app.workflow.context import WorkflowContext
from app.workflow.proposal_workflow import run_proposal_workflow
from app.workflow.store import save_workflow_context
from app.utils.generate_id import generate_proposal_id

EXAMPLE = """Send proposal data like this:

/newproposal
Company Name: Nirav Tools
Website: https://example.com
Client Name: Mahendra G
Client Email: sales@example.com
Services: AI SDR / Lead Generation Automation, WhatsApp Automate
Pricing Mode: Manual
Pricing Plan: Growth
Setup Cost: ₹75000
Monthly Cost: ₹25000
Sales Note: Met at expo. Wants B2B leads from manufacturers.
"""


def _is_allowed(user_id: int) -> bool:
    allowed = [x.strip() for x in settings.ALLOWED_TELEGRAM_USER_IDS.split(",") if x.strip()]
    return not allowed or str(user_id) in allowed


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Bharat AI Vyapari Proposal Bot is ready. Use /newproposal.")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(EXAMPLE)


async def newproposal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text("You are not allowed to use this bot.")
        return

    text = update.message.text or ""
    if "Company Name:" not in text:
        await update.message.reply_text(EXAMPLE)
        return

    parsed = parse_proposal_message(text)
    ctx = WorkflowContext(
        proposal_id=generate_proposal_id(),
        raw_input={"telegram_text": text},
        normalized_input=parsed,
        telegram_chat_id=str(update.effective_chat.id),
        client_email=parsed.get("client_email"),
        status="generating",
    )
    save_workflow_context(ctx)
    await update.message.reply_text(f"Proposal generation started. ID: {ctx.proposal_id}")
    result = await run_proposal_workflow(ctx)
    save_workflow_context(result)
    if result.status == "failed":
        await update.message.reply_text(f"Proposal failed: {result.errors[-1] if result.errors else 'Unknown error'}")
    else:
        await update.message.reply_text(f"Proposal generated. PDF: {result.pdf_url or result.pdf_path}")


def start_bot() -> None:
    if not settings.TELEGRAM_BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not configured")
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("newproposal", newproposal))
    app.add_handler(CallbackQueryHandler(approval_callback))
    app.run_polling()
