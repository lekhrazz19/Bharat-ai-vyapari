from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class WorkflowContext(BaseModel):
    proposal_id: str
    status: str = "started"
    raw_input: Dict[str, Any] = Field(default_factory=dict)
    normalized_input: Dict[str, Any] = Field(default_factory=dict)
    research_summary: Dict[str, Any] = Field(default_factory=dict)
    pricing_data: Dict[str, Any] = Field(default_factory=dict)
    proposal_json: Dict[str, Any] = Field(default_factory=dict)
    rendered_html_files: List[str] = Field(default_factory=list)
    pdf_path: Optional[str] = None
    pdf_url: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    client_email: Optional[str] = None
    errors: List[str] = Field(default_factory=list)
