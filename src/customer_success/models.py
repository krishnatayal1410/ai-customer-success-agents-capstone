from __future__ import annotations

from pydantic import BaseModel, Field


class CustomerAccount(BaseModel):
    account_id: str
    company: str
    plan: str
    licensed_seats: int = Field(gt=0)
    active_seats: int = Field(ge=0)
    days_since_login: int = Field(ge=0)
    feature_adoption: float = Field(ge=0, le=1)
    nps: int = Field(ge=-100, le=100)
    open_tickets: int = Field(ge=0)
    high_priority_tickets: int = Field(ge=0)
    renewal_days: int = Field(ge=0)
    arr_usd: int = Field(ge=0)
    owner: str


class HealthAssessment(BaseModel):
    account_id: str
    company: str
    health_score: int = Field(ge=0, le=100)
    risk_level: str
    risk_drivers: list[str]
    positive_signals: list[str]
    recommended_actions: list[str]


class InterventionPlan(BaseModel):
    account_id: str
    objective: str
    actions: list[str]
    owner: str
    due_in_days: int = Field(gt=0)
    requires_human_approval: bool = True


class AccountHealthReport(BaseModel):
    account_id: str
    executive_summary: str
    health: HealthAssessment
    intervention: InterventionPlan
    product_guidance: list[str]
    support_summary: str
    follow_up_message: str
