from app.workflow.context import WorkflowContext


async def pricing_lookup(ctx: WorkflowContext) -> WorkflowContext:
    data = ctx.normalized_input
    if data.get("pricing_mode", "").lower() == "manual":
        ctx.pricing_data = {
            "pricingPlan": data.get("pricing_plan", "Growth"),
            "setupCost": data.get("manual_setup_cost") or "Custom Quote",
            "monthlyCost": data.get("manual_monthly_cost") or "Custom Quote",
            "timeline": "To be discussed",
            "currency": "₹",
            "source": "manual",
        }
    else:
        # Replace this with Google Sheet or Baserow pricing later.
        ctx.pricing_data = {
            "pricingPlan": data.get("pricing_plan", "Growth"),
            "setupCost": "Custom Quote",
            "monthlyCost": "Custom Quote",
            "timeline": "To be discussed",
            "currency": "₹",
            "source": "config_placeholder",
        }
    ctx.status = "pricing_ready"
    return ctx
