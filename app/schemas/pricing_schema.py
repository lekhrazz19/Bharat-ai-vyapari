from pydantic import BaseModel


class PricingData(BaseModel):
    pricing_plan: str = "Growth"
    setup_cost: str = "Custom Quote"
    monthly_cost: str = "Custom Quote"
    timeline: str = "To be discussed"
    currency: str = "₹"
