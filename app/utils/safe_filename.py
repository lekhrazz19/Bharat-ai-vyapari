import re


def safe_filename(value: str) -> str:
    value = value or "proposal"
    value = re.sub(r"[^a-zA-Z0-9_-]+", "-", value).strip("-")
    return value[:80] or "proposal"
