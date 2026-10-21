"""Pydantic models for student and skill-assessment APIs."""
from __future__ import annotations

import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

PlacementStatus = Literal["placed", "in_process", "not_placed", "opted_out"]
Department = Literal["CSE", "IT", "AIDS", "ECE"]


class _StudentFields(BaseModel):
    model_config = ConfigDict(extra="forbid")

    usn: str
    full_name: str = Field(min_length=1, max_length=200)
    email: str | None = Field(default=None, max_length=320)
    department: Department
    batch_year: int
    tenth_pct: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    twelfth_pct: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    cgpa: float | None = Field(default=None, ge=0, le=10, allow_inf_nan=False)
    aptitude_score: int | None = Field(default=None, ge=0, le=100)
    technical_score: int | None = Field(default=None, ge=0, le=100)
    communication_score: int | None = Field(default=None, ge=0, le=100)
    internships: int = Field(default=0, ge=0)
    projects: int = Field(default=0, ge=0)
    certifications: int = Field(default=0, ge=0)
    backlogs: int = Field(default=0, ge=0)
    extracurricular: bool = False
    placement_training: bool = False
    placement_status: PlacementStatus = "in_process"
    company: str | None = Field(default=None, max_length=200)
    package_lpa: float | None = Field(default=None, ge=0, le=9999.99, allow_inf_nan=False)

    @field_validator("usn", mode="before")
    @classmethod
    def normalize_usn(cls, value):
        if not isinstance(value, str):
            raise ValueError("USN must be text")
        normalized = value.strip().upper()
        if not normalized or len(normalized) > 50:
            raise ValueError("USN must contain 1–50 characters")
        return normalized

    @field_validator("full_name", "company", mode="before")
    @classmethod
    def trim_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value):
        if value is None or value == "":
            return None
        if not isinstance(value, str):
            raise ValueError("Email must be text")
        value = value.strip()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Invalid email address")
        return value.lower()


class StudentCreate(_StudentFields):
    """Validated student creation/import payload."""


class StudentUpdate(BaseModel):
    """Partial student update payload; every field is optional."""
    model_config = ConfigDict(extra="forbid")

    usn: str | None = None
    full_name: str | None = Field(default=None, min_length=1, max_length=200)
    email: str | None = Field(default=None, max_length=320)
    department: Department | None = None
    batch_year: int | None = None
    tenth_pct: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    twelfth_pct: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    cgpa: float | None = Field(default=None, ge=0, le=10, allow_inf_nan=False)
    aptitude_score: int | None = Field(default=None, ge=0, le=100)
    technical_score: int | None = Field(default=None, ge=0, le=100)
    communication_score: int | None = Field(default=None, ge=0, le=100)
    internships: int | None = Field(default=None, ge=0)
    projects: int | None = Field(default=None, ge=0)
    certifications: int | None = Field(default=None, ge=0)
    backlogs: int | None = Field(default=None, ge=0)
    extracurricular: bool | None = None
    placement_training: bool | None = None
    placement_status: PlacementStatus | None = None
    company: str | None = Field(default=None, max_length=200)
    package_lpa: float | None = Field(default=None, ge=0, le=9999.99, allow_inf_nan=False)

    @field_validator("usn", mode="before")
    @classmethod
    def normalize_usn(cls, value):
        if value is None:
            return value
        if not isinstance(value, str):
            raise ValueError("USN must be text")
        value = value.strip().upper()
        if not value or len(value) > 50:
            raise ValueError("USN must contain 1–50 characters")
        return value

    @field_validator("full_name", "company", mode="before")
    @classmethod
    def trim_text(cls, value):
        return value.strip() if isinstance(value, str) else value

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, value):
        if value is None or value == "":
            return None
        if not isinstance(value, str):
            raise ValueError("Email must be text")
        value = value.strip()
        if not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value):
            raise ValueError("Invalid email address")
        return value.lower()


class StudentOut(_StudentFields):
    """Student row returned by the API."""
    id: str
    created_by: str | None = None
    created_at: datetime
    updated_at: datetime


class SkillAssessmentIn(BaseModel):
    """Input for a new skill assessment."""
    model_config = ConfigDict(extra="forbid")

    dsa: int = Field(ge=0, le=100)
    system_design: int = Field(ge=0, le=100)
    core_cs: int = Field(ge=0, le=100)
    aptitude: int = Field(ge=0, le=100)
    communication: int = Field(ge=0, le=100)
    source: str | None = Field(default="manual", max_length=100)
