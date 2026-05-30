from pydantic import BaseModel, Field
from typing import List


class ProposalMeta(BaseModel):
    proposalId: str = ""
    clientCompanyName: str = ""
    clientName: str = ""
    clientEmail: str = ""
    clientWebsite: str = ""
    proposalDate: str = ""
    proposalYear: str = ""
    pricingMode: str = ""
    currency: str = "₹"


class ServiceProposal(BaseModel):
    serviceKey: str = ""
    serviceSectionLabel: str = ""
    serviceName: str = ""
    serviceTagline: str = ""
    whoItsForTitle: str = "Who It’s For"
    whoItsForDescription: str = ""

    industry1: str = ""
    industry2: str = ""
    industry3: str = ""
    industry4: str = ""
    industry5: str = ""
    industry6: str = ""
    industry7: str = ""
    industry8: str = ""
    industry9: str = ""
    industry10: str = ""
    industry11: str = ""
    industry12: str = ""

    useCaseTitle: str = "Use Case Summary / Result"
    useCaseSummary: str = ""
    resultTitle: str = "Result"
    resultStatement: str = ""
    workflowTitle: str = "Workflow"

    step1Title: str = ""
    step1Description: str = ""
    step1Bullet1: str = ""
    step1Bullet2: str = ""
    step1Bullet3: str = ""

    step2Title: str = ""
    step2Description: str = ""
    step2Bullet1: str = ""
    step2Bullet2: str = ""
    step2Bullet3: str = ""
    step2Bullet4: str = ""

    step3Title: str = ""
    step3Description: str = ""
    step3Bullet1: str = ""
    step3Bullet2: str = ""
    step3Bullet3: str = ""

    step4Title: str = ""
    step4Description: str = ""
    step4Bullet1: str = ""
    step4Bullet2: str = ""
    step4Bullet3: str = ""

    step5Title: str = ""
    step5Description: str = ""
    step5Bullet1: str = ""
    step5Bullet2: str = ""
    step5Bullet3: str = ""
    step5Bullet4: str = ""

    benefitsTitle: str = "Key Benefits / Outcomes"
    pasTitle: str = "PAS Framework"
    outcomeHeader: str = "Outcome"
    beforeHeader: str = "Before AutoVyapari"
    afterHeader: str = "After AI Deployment"

    outcome1: str = ""
    before1: str = ""
    after1: str = ""
    outcome2: str = ""
    before2: str = ""
    after2: str = ""
    outcome3: str = ""
    before3: str = ""
    after3: str = ""
    outcome4: str = ""
    before4: str = ""
    after4: str = ""
    outcome5: str = ""
    before5: str = ""
    after5: str = ""
    outcome6: str = ""
    before6: str = ""
    after6: str = ""

    problemTitle: str = "Problem"
    problemText: str = ""
    agitationTitle: str = "Agitation"
    agitationText: str = ""
    solutionTitle: str = "Solution"
    solutionText: str = ""

    pricingPlan: str = ""
    setupCost: str = ""
    monthlyCost: str = ""
    timeline: str = ""
    nextStep: str = ""


class CombinedPricing(BaseModel):
    pricingPlan: str = ""
    setupCostTotal: str = ""
    monthlyCostTotal: str = ""
    timeline: str = ""
    includedServices: List[str] = Field(default_factory=list)
    nextStep: str = "Approve proposal and schedule kickoff."


class ProposalOutput(BaseModel):
    proposalMeta: ProposalMeta = Field(default_factory=ProposalMeta)
    services: List[ServiceProposal] = Field(default_factory=list)
    combinedPricing: CombinedPricing = Field(default_factory=CombinedPricing)
