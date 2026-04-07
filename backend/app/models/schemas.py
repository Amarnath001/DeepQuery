from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User research query")
    session_id: str | None = Field(
        default=None,
        description="Optional session identifier for conversation continuity",
    )


class TokenBudgetDebug(BaseModel):
    max_context_tokens: int
    initial_chunk_count: int
    final_chunk_count: int
    initial_estimated_tokens: int
    final_estimated_tokens: int
    compressed: bool
    dropped_chunks: int
    compression_applied_to: list[str] = Field(default_factory=list)
    notes: str


class RetrievedChunk(BaseModel):
    id: str
    title: str
    region: str
    topic: str
    content: str
    score: float


class ResearchResponse(BaseModel):
    query: str
    session_id: str | None = None
    sub_questions: list[str] = Field(default_factory=list)
    retrieved_chunks: list[RetrievedChunk] = Field(default_factory=list)
    final_answer: str
    debug: TokenBudgetDebug
