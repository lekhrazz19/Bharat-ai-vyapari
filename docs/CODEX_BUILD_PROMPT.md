X`# Codex Build Prompt

You are building a Python replacement for an n8n proposal workflow. Keep the n8n-style node pipeline, but implement each node as a Python module/function.

## Goal

Build Bharat AI Vyapari Proposal Engine:

Telegram bot trigger → company research via OpenRouter → proposal JSON via OpenRouter → validate/trim JSON → Jinja2 HTML templates → Playwright PDF → Telegram approval → email → Baserow status.

## Current scaffold

The project already has folders, schemas, workflow context, Telegram bot, OpenRouter service, Jinja2 templates, and Playwright renderer.

## Your tasks

1. Run the app locally.
2. Fix any import/runtime issues.
3. Test `/api/proposals/run` with `sample_input.json`.
4. Test Telegram `/newproposal` structured message.
5. Improve Baserow upsert so it updates by `proposal_id` instead of always creating rows.
6. Wire approval callback:
   - approve → send email and update Baserow status
   - reject → update status
   - regenerate → rerun workflow
7. Add Google Drive or S3 upload if needed.
8. Add Serper search into `research_company` if `SERPER_API_KEY` exists.
9. Polish PDF templates to match Bharat AI Vyapari PPT/PDF exactly.
10. Add unit tests for Telegram parser, trim_json, and renderer.

## Do not

- Do not use n8n.
- Do not use Google Slides.
- Do not use external PDF APIs.
- Do not commit `.env`.

## Run commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
uvicorn app.server:app --reload --port 8000
```

Telegram bot:

```bash
python main.py
```
