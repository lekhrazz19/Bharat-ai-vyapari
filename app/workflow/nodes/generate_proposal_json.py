import json
from datetime import datetime
from app.workflow.context import WorkflowContext
from app.services.openrouter_service import call_openrouter
from app.utils.safe_json import parse_json_safely


async def generate_proposal_json(ctx: WorkflowContext) -> WorkflowContext:
    selected = ctx.normalized_input.get("selected_services") or []
    system_prompt = """
You are a precise proposal content generator for Bharat AI Vyapari.
Return ONLY valid JSON. No markdown. No explanations.
Generate concise content that fits fixed HTML proposal templates.
Create one services[] object for each selected service. Do not drop services.
Respect these limits: serviceSectionLabel max 4 words; serviceName max 7; tagline max 12; whoItsForDescription max 35; industry max 3 words each; useCaseSummary max 45; resultStatement max 40; step titles max 5; step descriptions max 20; step bullets max 5; outcomes max 5; before/after max 8; problemText max 22; agitationText max 22; solutionText max 26; nextStep max 12.
"""
    today = datetime.now().strftime("%d %B %Y")
    year = datetime.now().strftime("%Y")
    user_prompt = f"""
Generate a Bharat AI Vyapari proposal JSON.

Input:
{json.dumps(ctx.normalized_input, ensure_ascii=False)}

Research:
{json.dumps(ctx.research_summary, ensure_ascii=False)}

Pricing:
{json.dumps(ctx.pricing_data, ensure_ascii=False)}

Proposal ID: {ctx.proposal_id}
Proposal Date: {today}
Proposal Year: {year}
Selected services: {json.dumps(selected, ensure_ascii=False)}

Return JSON exactly with this shape:
{{
  "proposalMeta": {{
    "proposalId": "{ctx.proposal_id}",
    "clientCompanyName": "",
    "clientName": "",
    "clientEmail": "",
    "clientWebsite": "",
    "proposalDate": "{today}",
    "proposalYear": "{year}",
    "pricingMode": "",
    "currency": "₹"
  }},
  "services": [
    {{
      "serviceKey": "",
      "serviceSectionLabel": "",
      "serviceName": "",
      "serviceTagline": "",
      "whoItsForTitle": "Who It’s For",
      "whoItsForDescription": "",
      "industry1": "", "industry2": "", "industry3": "", "industry4": "", "industry5": "", "industry6": "",
      "industry7": "", "industry8": "", "industry9": "", "industry10": "", "industry11": "", "industry12": "",
      "useCaseTitle": "Use Case Summary / Result",
      "useCaseSummary": "",
      "resultTitle": "Result",
      "resultStatement": "",
      "workflowTitle": "Workflow",
      "step1Title": "", "step1Description": "", "step1Bullet1": "", "step1Bullet2": "", "step1Bullet3": "",
      "step2Title": "", "step2Description": "", "step2Bullet1": "", "step2Bullet2": "", "step2Bullet3": "", "step2Bullet4": "",
      "step3Title": "", "step3Description": "", "step3Bullet1": "", "step3Bullet2": "", "step3Bullet3": "",
      "step4Title": "", "step4Description": "", "step4Bullet1": "", "step4Bullet2": "", "step4Bullet3": "",
      "step5Title": "", "step5Description": "", "step5Bullet1": "", "step5Bullet2": "", "step5Bullet3": "", "step5Bullet4": "",
      "benefitsTitle": "Key Benefits / Outcomes",
      "pasTitle": "PAS Framework",
      "outcomeHeader": "Outcome", "beforeHeader": "Before AutoVyapari", "afterHeader": "After AI Deployment",
      "outcome1": "", "before1": "", "after1": "",
      "outcome2": "", "before2": "", "after2": "",
      "outcome3": "", "before3": "", "after3": "",
      "outcome4": "", "before4": "", "after4": "",
      "outcome5": "", "before5": "", "after5": "",
      "outcome6": "", "before6": "", "after6": "",
      "problemTitle": "Problem", "problemText": "",
      "agitationTitle": "Agitation", "agitationText": "",
      "solutionTitle": "Solution", "solutionText": "",
      "pricingPlan": "", "setupCost": "", "monthlyCost": "", "timeline": "", "nextStep": ""
    }}
  ],
  "combinedPricing": {{
    "pricingPlan": "",
    "setupCostTotal": "",
    "monthlyCostTotal": "",
    "timeline": "",
    "includedServices": [],
    "nextStep": "Approve proposal and schedule kickoff."
  }}
}}
"""
    output = await call_openrouter(system_prompt, user_prompt, json_mode=True)
    ctx.proposal_json = parse_json_safely(output)
    ctx.status = "proposal_json_generated"
    return ctx
