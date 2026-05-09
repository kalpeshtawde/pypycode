from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, model_validator

from vega.constants import (
    ADVANCED_DISTRIBUTION,
    BEGINNER_DISTRIBUTION,
    INTERMEDIATE_DISTRIBUTION,
)


class DifficultyStats(BaseModel):
    attempted: int
    score: float
    submitted: int


class QuizStats(BaseModel):
    easy: DifficultyStats
    medium: DifficultyStats
    hard: DifficultyStats
    lastAttemptAt: Optional[datetime] = None


class DifficultyCountPayload(BaseModel):
    easy: int
    hard: int
    medium: int


class ProblemSetRequestPayload(BaseModel):
    mode: str  # practice | revision | interview | explore

    difficultyCounts: DifficultyCountPayload
    ignoreSlugs: list[str]
    tagWeights: dict[str, float]
    total: int

    metadata: dict[str, Any] = {}


class CreateProjectRequestPayload(BaseModel):
    name: str
    problemIds: Optional[List[str]] = None
    goal: Optional[str] = None
    strategy: Optional[str] = None
    level: Optional[str] = None
    explanation: Optional[str] = None
    aiMetadata: Optional[dict[str, Any]] = None


class DifficultySplit(BaseModel):
    easy: int
    medium: int
    hard: int

    @model_validator(mode="after")
    def validate_total_percentage(self):
        if self.easy < 0 or self.medium < 0 or self.hard < 0:
            raise ValueError("Difficulty split values must be non-negative")
        if self.easy + self.medium + self.hard != 100:
            raise ValueError("Difficulty split values must sum to 100")
        return self


class DifficultyDistro(BaseModel):
    beginner: DifficultySplit = Field(default_factory=lambda: DifficultySplit(**BEGINNER_DISTRIBUTION))
    intermediate: DifficultySplit = Field(default_factory=lambda: DifficultySplit(**INTERMEDIATE_DISTRIBUTION))
    advanced: DifficultySplit = Field(default_factory=lambda: DifficultySplit(**ADVANCED_DISTRIBUTION))
