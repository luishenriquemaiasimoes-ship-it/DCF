"""Parameter records: every legal, tax or market value is dated and sourced.

Rules (spec 29 + session instruction): values are never filled from memory. A record
may carry a value only when status is VERIFIED, which requires a successful retrieval of
an official source with a retrieval timestamp and a named verifier."""

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ParamStatus(StrEnum):
    VERIFIED = "verified"
    NEEDS_VERIFICATION = "needs_verification"
    SUPERSEDED = "superseded"


class RetrievalStatus(StrEnum):
    OK = "ok"
    FAILED = "failed"
    NOT_ATTEMPTED = "not_attempted"


class ValueType(StrEnum):
    RATE = "rate"  # fraction: 0.15 == 15%
    AMOUNT = "amount"
    BOOLEAN = "boolean"
    TEXT = "text"


class ParamSource(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    url: str
    title: str
    issuer: str
    is_official: bool
    locator: str | None = None  # article / paragraph / table
    retrieval_status: RetrievalStatus
    attempted_at: datetime | None = None
    retrieved_at: datetime | None = None
    content_sha256: str | None = None
    retrieval_note: str | None = None

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.retrieval_status == RetrievalStatus.OK and not (self.retrieved_at and self.content_sha256):
            raise ValueError("a successful retrieval needs retrieved_at and content_sha256")
        if self.retrieval_status != RetrievalStatus.OK and self.retrieved_at:
            raise ValueError("retrieved_at is set only for successful retrievals")
        if self.retrieval_status == RetrievalStatus.FAILED and not self.attempted_at:
            raise ValueError("failed retrievals must record attempted_at")
        return self


class ParameterRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str = Field(pattern=r"^[a-z0-9_.:@-]+$")  # unique record id, e.g. "br.tax.csll.standard_rate@2026-01-01"
    key: str = Field(pattern=r"^[a-z0-9_.]+$")  # logical key; several records over time
    jurisdiction: str
    description: str
    value_type: ValueType
    value: Decimal | bool | str | None = None
    unit_note: str | None = None
    valid_from: date | None = None
    valid_to: date | None = None  # inclusive; None = open-ended
    applies_to: str | None = None  # condition text, e.g. regime or entity type
    status: ParamStatus
    sources: tuple[ParamSource, ...] = Field(min_length=1)
    verified_by: str | None = None
    verified_at: datetime | None = None
    spec_reference: str | None = None  # spec section and any figure the spec states (not a verified value)
    open_questions: tuple[str, ...] = ()
    supersedes: str | None = None

    @model_validator(mode="after")
    def _check(self) -> Self:
        if self.valid_from and self.valid_to and self.valid_to < self.valid_from:
            raise ValueError(f"{self.id}: valid_to before valid_from")
        if self.status == ParamStatus.VERIFIED:
            if self.value is None:
                raise ValueError(f"{self.id}: verified record needs a value")
            if not any(s.is_official and s.retrieval_status == RetrievalStatus.OK for s in self.sources):
                raise ValueError(f"{self.id}: verified record needs a successfully retrieved official source")
            if not (self.verified_by and self.verified_at and self.valid_from):
                raise ValueError(f"{self.id}: verified record needs verified_by, verified_at and valid_from")
        else:
            if self.status == ParamStatus.NEEDS_VERIFICATION and self.value is not None:
                raise ValueError(f"{self.id}: unverified records must not carry a value (never fill from memory)")
        return self
