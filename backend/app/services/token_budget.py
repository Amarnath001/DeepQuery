import re

from app.models.schemas import RetrievedChunk


class TokenBudgetManager:
    """Estimates context cost and builds memory-budget debug information."""

    def __init__(
        self,
        max_context_tokens: int = 1200,
        max_chunks: int = 4,
        compression_target_ratio: float = 0.5,
    ) -> None:
        self.max_context_tokens = max_context_tokens
        self.max_chunks = max_chunks
        self.compression_target_ratio = compression_target_ratio

    def estimate_text_tokens(self, text: str) -> int:
        # Lightweight approximation: roughly 1 token ~= 0.75 words.
        words = re.findall(r"\S+", text or "")
        return max(1, int(len(words) * 1.33))

    def estimate_chunk_tokens(self, chunk: RetrievedChunk) -> int:
        text_blob = " ".join([chunk.title, chunk.region, chunk.topic, chunk.content])
        return self.estimate_text_tokens(text_blob)

    def estimate_total_tokens(self, chunks: list[RetrievedChunk]) -> int:
        return sum(self.estimate_chunk_tokens(c) for c in chunks)

    def build_debug_snapshot(
        self,
        initial_chunk_count: int,
        final_chunk_count: int,
        initial_estimated_tokens: int,
        final_estimated_tokens: int,
        compressed: bool,
        dropped_chunks: int,
        compression_applied_to: list[str],
        notes: str,
    ) -> dict:
        return {
            "max_context_tokens": self.max_context_tokens,
            "initial_chunk_count": initial_chunk_count,
            "final_chunk_count": final_chunk_count,
            "initial_estimated_tokens": initial_estimated_tokens,
            "final_estimated_tokens": final_estimated_tokens,
            "compressed": compressed,
            "dropped_chunks": dropped_chunks,
            "compression_applied_to": compression_applied_to,
            "notes": notes,
        }
