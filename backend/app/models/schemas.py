from typing import Any

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User research query")
    session_id: str | None = Field(
        default=None,
        description="Optional session identifier for conversation continuity",
    )


class TokenBudgetDebug(BaseModel):
    allocated_tokens: int = 0
    used_tokens: int = 0
    remaining_tokens: int = 0
    notes: str = "Token budget manager placeholder"


class ResearchResponse(BaseModel):
    query: str
    session_id: str | None = None
    sub_questions: list[str] = Field(default_factory=list)
    retrieved_chunks: list[dict[str, Any]] = Field(default_factory=list)
    final_answer: str
    debug: TokenBudgetDebug
