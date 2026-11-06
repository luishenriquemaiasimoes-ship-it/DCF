"""Assumptions with AI-suggested vs user values and history (spec 2.5, 7.1, 8.1–8.3)."""

from datetime import UTC, datetime
from enum import StrEnum
from typing import Self
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator

from vip.core.provenance import Confidence, ValueOrigin
from vip.core.units import Unit


class AssumptionStatus(StrEnum):
    AI_SUGGESTED = "ai_suggested"
    USER_MODIFIED = "user_modified"
    SOURCE_VERIFIED = "source_verified"
    HISTORICAL_ACTUAL = "historical_actual"
    CALCULATED = "calculated"
    NEEDS_REVIEW = "needs_review"
    UNVERIFIED = "unverified"


class AISuggestion(BaseModel):
    """Spec 7.1: everything the AI must provide with a suggested value."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    value: float
    reasoning: str
    methodology: str
    confidence: Confidence
    historical_reference: str | None = None
    industry_benchmark: str | None = None
    management_guidance: str | None = None
    evidence_source_ids: tuple[UUID, ...] = ()
    key_risks: tuple[str, ...] = ()
    alternatives: tuple[float, ...] = ()
    model_name: str | None = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class AssumptionVersion(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    version: int
    value: float | None
    origin: ValueOrigin
    changed_by: str  # user id or "ai:<agent>"
    changed_at: datetime
    reason: str | None = None


class UserApprovalRequired(PermissionError):
    """Spec 8.2: an AI value must never overwrite a user-approved assumption without authorization."""


class Assumption(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    variable_id: str
    scenario_id: str
    period_id: str | None = None  # None = applies to every forecast period
    unit: Unit
    ai_suggestion: AISuggestion | None = None
    user_value: float | None = None
    original_value: float | None = None
    status: AssumptionStatus
    user_approved: bool = False
    explanation: str | None = None
    source_ids: tuple[UUID, ...] = ()
    history: tuple[AssumptionVersion, ...] = ()

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.user_value is None and self.ai_suggestion is None and self.status != AssumptionStatus.NEEDS_REVIEW:
            raise ValueError("an assumption without any value must be NEEDS_REVIEW")
        return self

    @property
    def active_value(self) -> float | None:
        if self.user_value is not None:
            return self.user_value
        return self.ai_suggestion.value if self.ai_suggestion else None

    def _bump(self, value: float | None, origin: ValueOrigin, by: str, reason: str | None) -> tuple[AssumptionVersion, ...]:
        v = AssumptionVersion(
            version=len(self.history) + 1, value=value, origin=origin, changed_by=by, changed_at=datetime.now(UTC), reason=reason
        )
        return (*self.history, v)

    def with_user_value(self, value: float, by: str, reason: str | None = None) -> "Assumption":
        return self.model_copy(
            update={
                "user_value": value,
                "status": AssumptionStatus.USER_MODIFIED,
                "user_approved": True,
                "original_value": self.original_value if self.original_value is not None else self.active_value,
                "history": self._bump(value, ValueOrigin.USER_INPUT, by, reason),
            }
        )

    def with_ai_suggestion(self, suggestion: AISuggestion, agent: str, authorized_by_user: bool = False) -> "Assumption":
        """Records a new AI suggestion. If the user owns the active value, the suggestion is
        stored alongside but does not become active unless the user explicitly authorizes it."""
        if self.user_approved and not authorized_by_user:
            return self.model_copy(update={"ai_suggestion": suggestion, "status": self.status})
        update = {"ai_suggestion": suggestion, "history": self._bump(suggestion.value, ValueOrigin.AI_ESTIMATE, f"ai:{agent}", None)}
        if authorized_by_user:
            update |= {"user_value": None, "user_approved": False, "status": AssumptionStatus.AI_SUGGESTED}
        elif self.user_value is None:
            update["status"] = AssumptionStatus.AI_SUGGESTED
        return self.model_copy(update=update)

    def reset_to_ai(self, by: str) -> "Assumption":
        if self.ai_suggestion is None:
            raise ValueError("no AI suggestion to reset to")
        return self.model_copy(
            update={
                "user_value": None,
                "user_approved": False,
                "status": AssumptionStatus.AI_SUGGESTED,
                "history": self._bump(self.ai_suggestion.value, ValueOrigin.AI_ESTIMATE, by, "reset to AI suggestion"),
            }
        )
