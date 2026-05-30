from pydantic import BaseModel, EmailStr, Field, HttpUrl
from typing import List, Optional


class ProposalInput(BaseModel):
    company_name: str = Field(..., min_length=1)
    company_website: Optional[str] = ""
    client_name: str = Field(..., min_length=1)
    client_email: EmailStr
    selected_services: List[str] = Field(default_factory=list)
    pricing_mode: str = "Manual"
    pricing_plan: str = "Growth"
    manual_setup_cost: str = ""
    manual_monthly_cost: str = ""
    sales_note: str = ""
