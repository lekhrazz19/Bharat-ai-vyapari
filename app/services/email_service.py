import smtplib
from email.message import EmailMessage
from pathlib import Path
from app.config import settings


async def send_proposal_email(to_email: str, client_name: str, company_name: str, pdf_path: str):
    if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASS, settings.SMTP_FROM]):
        raise RuntimeError("SMTP is not configured")
    if not pdf_path:
        raise RuntimeError("PDF path missing")

    msg = EmailMessage()
    msg["Subject"] = f"AI Automation Proposal for {company_name}"
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg.set_content(f"""
Hi {client_name},

Thank you for your time and discussion with Bharat AI Vyapari.

Please find attached your AI automation proposal prepared for {company_name}.

The proposal includes recommended automation systems, expected outcomes, implementation direction, and pricing summary.

Regards,
Bharat AI Vyapari
""")
    path = Path(pdf_path)
    msg.add_attachment(path.read_bytes(), maintype="application", subtype="pdf", filename=path.name)

    with smtplib.SMTP(settings.SMTP_HOST, int(settings.SMTP_PORT)) as server:
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg)
