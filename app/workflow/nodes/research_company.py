import json
from app.workflow.context import WorkflowContext
from app.services.research_service import fetch_website_text
from app.services.openrouter_service import call_openrouter
from app.utils.safe_json import parse_json_safely
from app.config import settings


async def research_company(ctx: WorkflowContext) -> WorkflowContext:
    company = ctx.normalized_input.get("company_name", "")
    website = ctx.normalized_input.get("company_website", "")
    website_text = await fetch_website_text(website)

    system_prompt = """
You are a company research assistant. Return only valid JSON. Do not invent facts. If a fact is unavailable, use an empty string or empty array.
"""
    user_prompt = f"""
Research this company for a business automation proposal.

Company Name: {company}
Website: {website}

Website text:
{website_text[:7000]}

Return JSON exactly:
{{
  "companyName": "",
  "industry": "",
  "productsServices": [],
  "targetCustomers": [],
  "location": "",
  "businessType": "",
  "digitalGaps": [],
  "growthOpportunities": [],
  "shortSummary": ""
}}
"""
    output = await call_openrouter(
        system_prompt, 
        user_prompt, 
        model=settings.OPENROUTER_DEFAULT_MODEL, 
        json_mode=True
    )
    ctx.research_summary = parse_json_safely(output)
    ctx.status = "researched"
    return ctx
