from copy import deepcopy
from typing import Dict, Optional

from app.workflow.context import WorkflowContext


_WORKFLOW_STORE: Dict[str, WorkflowContext] = {}


def save_workflow_context(ctx: WorkflowContext) -> None:
    _WORKFLOW_STORE[ctx.proposal_id] = ctx.model_copy(deep=True)


def get_workflow_context(proposal_id: str) -> Optional[WorkflowContext]:
    ctx = _WORKFLOW_STORE.get(proposal_id)
    return ctx.model_copy(deep=True) if ctx else None


def reset_for_regeneration(ctx: WorkflowContext) -> WorkflowContext:
    regenerated = deepcopy(ctx)
    regenerated.status = "generating"
    regenerated.research_summary = {}
    regenerated.pricing_data = {}
    regenerated.proposal_json = {}
    regenerated.rendered_html_files = []
    regenerated.pdf_path = None
    regenerated.pdf_url = None
    regenerated.errors = []
    return regenerated
