from datetime import datetime
from app.workflow.context import WorkflowContext
from app.schemas.proposal_schema import ProposalOutput
from app.utils.trim_words import trim_words


def trim_service(service: dict) -> dict:
    limits = {
        "serviceSectionLabel": 4, "serviceName": 7, "serviceTagline": 12,
        "whoItsForDescription": 35, "useCaseSummary": 45, "resultStatement": 40,
        "problemText": 22, "agitationText": 22, "solutionText": 26,
        "nextStep": 12, "timeline": 5,
    }
    for key, limit in limits.items():
        service[key] = trim_words(service.get(key, ""), limit)

    for i in range(1, 13):
        service[f"industry{i}"] = trim_words(service.get(f"industry{i}", ""), 3)

    for i in range(1, 6):
        service[f"step{i}Title"] = trim_words(service.get(f"step{i}Title", ""), 5)
        service[f"step{i}Description"] = trim_words(service.get(f"step{i}Description", ""), 20)
        for b in range(1, 5):
            key = f"step{i}Bullet{b}"
            if key in service:
                service[key] = trim_words(service.get(key, ""), 5)

    for i in range(1, 7):
        service[f"outcome{i}"] = trim_words(service.get(f"outcome{i}", ""), 5)
        service[f"before{i}"] = trim_words(service.get(f"before{i}", ""), 8)
        service[f"after{i}"] = trim_words(service.get(f"after{i}", ""), 8)

    return service


async def validate_trim_json(ctx: WorkflowContext) -> WorkflowContext:
    proposal = ctx.proposal_json or {}
    proposal.setdefault("proposalMeta", {})
    proposal.setdefault("services", [])
    proposal.setdefault("combinedPricing", {})

    meta = proposal["proposalMeta"]
    meta["proposalId"] = ctx.proposal_id
    meta.setdefault("proposalDate", datetime.now().strftime("%d %B %Y"))
    meta.setdefault("proposalYear", datetime.now().strftime("%Y"))
    meta.setdefault("currency", "₹")
    meta.setdefault("clientCompanyName", ctx.normalized_input.get("company_name", ""))
    meta.setdefault("clientName", ctx.normalized_input.get("client_name", ""))
    meta.setdefault("clientEmail", ctx.normalized_input.get("client_email", ""))
    meta.setdefault("clientWebsite", ctx.normalized_input.get("company_website", ""))
    meta.setdefault("pricingMode", ctx.normalized_input.get("pricing_mode", ""))

    proposal["services"] = [trim_service(dict(s)) for s in proposal.get("services", [])]

    if not proposal["services"]:
        # Minimal safe fallback, because blank PDFs are business-cardboard sadness.
        for service in ctx.normalized_input.get("selected_services", []) or ["AI Automation"]:
            proposal["services"].append(trim_service({
                "serviceKey": service.lower().replace(" ", "_"),
                "serviceSectionLabel": service.upper()[:24],
                "serviceName": service,
                "serviceTagline": "Automate growth and customer engagement.",
                "whoItsForTitle": "Who It’s For",
                "whoItsForDescription": "Built for businesses that want consistent leads, faster responses, and better operational visibility.",
                "useCaseTitle": "Use Case Summary / Result",
                "useCaseSummary": "AutoVyapari connects inputs, automates workflows, tracks outcomes, and supports measurable business growth.",
                "resultTitle": "Result",
                "resultStatement": "Faster execution, fewer manual tasks, and a cleaner sales pipeline.",
                "workflowTitle": "Workflow",
                "benefitsTitle": "Key Benefits / Outcomes",
                "pasTitle": "PAS Framework",
                "problemTitle": "Problem", "problemText": "Manual work slows sales and follow-ups.",
                "agitationTitle": "Agitation", "agitationText": "Delayed action lets competitors capture active buyers.",
                "solutionTitle": "Solution", "solutionText": "AutoVyapari automates outreach, replies, tracking, and reporting.",
            }))

    cp = proposal["combinedPricing"]
    cp.setdefault("pricingPlan", ctx.pricing_data.get("pricingPlan", ctx.normalized_input.get("pricing_plan", "Growth")))
    cp.setdefault("setupCostTotal", ctx.pricing_data.get("setupCost", "Custom Quote"))
    cp.setdefault("monthlyCostTotal", ctx.pricing_data.get("monthlyCost", "Custom Quote"))
    cp.setdefault("timeline", ctx.pricing_data.get("timeline", "To be discussed"))
    cp.setdefault("includedServices", [s.get("serviceName", "") for s in proposal["services"]])
    cp.setdefault("nextStep", "Approve proposal and schedule kickoff.")

    validated = ProposalOutput(**proposal)
    ctx.proposal_json = validated.model_dump()
    ctx.status = "proposal_json_validated"
    return ctx
