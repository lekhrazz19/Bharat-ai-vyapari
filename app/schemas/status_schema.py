from enum import Enum


class ProposalStatus(str, Enum):
    STARTED = "Started"
    GENERATING = "Generating"
    RESEARCHED = "Researched"
    JSON_GENERATED = "JSON Generated"
    PDF_GENERATED = "PDF Generated"
    PENDING_APPROVAL = "Pending Approval"
    APPROVED = "Approved"
    SENT = "Sent"
    FAILED = "Failed"
