from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.core.normalization import normalize_category, normalize_title


class TodoCreateRequest(BaseModel):
    title: str
    category: str | None = Field(default="general")

    @field_validator("title")
    @classmethod
    def normalize_title_field(cls, value: Any) -> str:
        return normalize_title(value)

    @field_validator("category", mode="before")
    @classmethod
    def normalize_category_field(cls, value: Any) -> str:
        return normalize_category(value, default_if_empty=True, coerce_numeric=False)


class TodoUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    category: str | int | float | None = None
    is_completed: bool | None = None

    @field_validator("title", mode="before")
    @classmethod
    def normalize_optional_title(cls, value: Any) -> str | None:
        if value is None:
            return value
        return normalize_title(value)

    @field_validator("category", mode="before")
    @classmethod
    def normalize_optional_category(cls, value: Any) -> str | None:
        if value is None:
            return value
        return normalize_category(value, default_if_empty=False, coerce_numeric=True)

    @model_validator(mode="after")
    def ensure_patch_has_at_least_one_field(self) -> "TodoUpdateRequest":
        if self.title is None and self.category is None and self.is_completed is None:
            raise ValueError("At least one field is required")
        return self


class TodoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    category: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def convert_to_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
