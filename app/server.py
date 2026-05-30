from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.workflow.context import WorkflowContext
from app.workflow.proposal_workflow import run_proposal_workflow
from app.utils.generate_id import generate_proposal_id

app = FastAPI(title="Bharat AI Vyapari Proposal Engine")
app.mount("/files", StaticFiles(directory="storage/pdf"), name="files")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/proposals/run")
async def run_proposal(payload: dict):
    ctx = WorkflowContext(
        proposal_id=generate_proposal_id(),
        raw_input=payload,
        normalized_input=payload,
        client_email=payload.get("client_email"),
        status="generating",
    )
    result = await run_proposal_workflow(ctx)
    return result.model_dump()
