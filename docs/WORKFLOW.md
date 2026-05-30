# Workflow

| n8n Node | Python Module |
|---|---|
| Telegram Trigger | app/telegram/bot.py |
| Parse Message | app/telegram/parser.py |
| Research Agent | app/workflow/nodes/research_company.py |
| AI Agent Proposal | app/workflow/nodes/generate_proposal_json.py |
| Structured Parser | app/schemas/proposal_schema.py |
| Code Trim Node | app/workflow/nodes/validate_trim_json.py |
| Template Renderer | app/renderer/html_renderer.py |
| PDF Export | app/renderer/pdf_renderer.py |
| Gmail | app/services/email_service.py |
| Status DB | app/services/baserow_service.py |
