
from typing import Literal

from pydantic import BaseModel, Field

ServiceCategory = Literal[
    "AI Automation",
    "Software Development",
    "CRM Integration",
    "Document Processing",
    "Voice AI",
    "Other",
    "Unclear",
]


class LeadExtraction(BaseModel):
    service_category: ServiceCategory
    business_goal: str
    budget: str | None = None
    timeline: str | None = None
    integrations: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    draft_reply: str


class LeadAnalysis(LeadExtraction):
    priority: Literal["High", "Medium", "Low"]
    priority_score: int = Field(ge=0, le=10)
    priority_reasons: list[str] = Field(default_factory=list)
    analysis_mode: Literal["Live Gemini", "Demo fallback"] = "Live Gemini"
    analysis_note: str | None = None
