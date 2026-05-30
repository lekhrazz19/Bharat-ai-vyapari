from datetime import datetime
import secrets


def generate_proposal_id() -> str:
    stamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    rand = secrets.token_hex(3).upper()
    return f"BAV-{stamp}-{rand}"
