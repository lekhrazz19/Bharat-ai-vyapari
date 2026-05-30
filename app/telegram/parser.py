import re


def _field(text: str, names: list[str]) -> str:
    for name in names:
        match = re.search(rf"^{re.escape(name)}\s*:\s*(.+)$", text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def parse_proposal_message(text: str) -> dict:
    services_raw = _field(text, ["Services", "Selected Services", "Service"])
    selected_services = [s.strip() for s in services_raw.split(",") if s.strip()]
    return {
        "company_name": _field(text, ["Company Name", "Company"]),
        "company_website": _field(text, ["Website", "Company Website", "Company Website URL"]),
        "client_name": _field(text, ["Client Name", "Client"]),
        "client_email": _field(text, ["Client Email", "Email"]),
        "selected_services": selected_services,
        "pricing_mode": _field(text, ["Pricing Mode"]) or "Manual",
        "pricing_plan": _field(text, ["Pricing Plan"]) or "Growth",
        "manual_setup_cost": _field(text, ["Setup Cost", "Manual One-Time Setup Cost"]),
        "manual_monthly_cost": _field(text, ["Monthly Cost", "Manual Monthly Retainer Cost"]),
        "sales_note": _field(text, ["Sales Note", "Internal Sales Note", "Note"]),
    }
