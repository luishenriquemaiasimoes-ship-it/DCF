"""Provenance (spec 2.3, 2.5, 3/Engine A): every value knows where it came from."""

from datetime import date, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class ValueOrigin(StrEnum):
    """Spec 2.3: the seven distinguishable kinds of value, plus parameter-store values."""

    REPORTED = "reported"  # historical, from filings
    MANAGEMENT_GUIDANCE = "management_guidance"
    MARKET_DATA = "market_data"
    ANALYST_ESTIMATE = "analyst_estimate"
    USER_INPUT = "user_input"
    AI_ESTIMATE = "ai_estimate"
    CALCULATED = "calculated"
    PARAMETER = "parameter"  # from the dated, sourced parameter store (docs/parameter-store.md)


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SourceRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: UUID = Field(default_factory=uuid4)
    title: str
    publisher: str | None = None
    url: str | None = None
    document_date: date | None = None
    retrieved_at: datetime | None = None
    locator: str | None = None  # page, table, note, article
    content_sha256: str | None = None  # hash of the raw document as retrieved
    notes: str | None = None
