# Bharat AI Vyapari Proposal Python Engine

Python replacement for the old n8n proposal workflow. It keeps the same node-style flow, but every n8n node is now a Python workflow step. Yes, we have reinvented a small workflow engine. Humanity persists.

## Flow

Telegram `/newproposal` trigger → parse input → research company → pricing lookup → OpenRouter proposal JSON → validate/trim → Jinja2 HTML templates → Playwright PDF → Telegram approval → email delivery → Baserow log.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
cp .env.example .env
# fill .env
python main.py
```

## Structured Telegram input

```text
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
```

## Local API test

```bash
uvicorn app.server:app --reload --port 8000
```

Then POST to `/api/proposals/run` with JSON matching `sample_input.json`.

## Assets

Replace these before production:

- `assets/cover.png`
- `assets/bav-logo.png`
- `assets/icons/default.png`

## Codex task

Open `docs/CODEX_BUILD_PROMPT.md` and give it to Codex as the implementation brief.
