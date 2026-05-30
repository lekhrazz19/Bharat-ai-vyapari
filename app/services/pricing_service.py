async def get_pricing_for_services(selected_services: list[str], pricing_plan: str) -> dict:
    # Hook this to Google Sheet/Baserow later. MVP returns a safe placeholder.
    return {
        "pricingPlan": pricing_plan or "Growth",
        "setupCost": "Custom Quote",
        "monthlyCost": "Custom Quote",
        "timeline": "To be discussed",
        "source": "placeholder",
    }
