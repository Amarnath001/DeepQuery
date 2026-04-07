from app.models.schemas import RetrievedChunk
from app.services.summarizer import SummarizerService
from app.services.token_budget import TokenBudgetManager


class MemoryManager:
    """Tracks lightweight session memory placeholder."""

    def __init__(self) -> None:
        self._sessions: dict[str, list[str]] = {}

    def get_session_history(self, session_id: str) -> list[str]:
        return self._sessions.get(session_id, [])

    def append_to_session(self, session_id: str, item: str) -> None:
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        self._sessions[session_id].append(item)

    def enforce_budget(
        self,
        chunks: list[RetrievedChunk],
        token_budget_manager: TokenBudgetManager,
        summarizer: SummarizerService,
    ) -> tuple[list[RetrievedChunk], dict]:
        initial_chunk_count = len(chunks)
        initial_estimated_tokens = token_budget_manager.estimate_total_tokens(chunks)

        working = sorted(chunks, key=lambda c: c.score, reverse=True)
        notes: list[str] = []
        compressed = False
        compression_applied_to: list[str] = []

        if len(working) > token_budget_manager.max_chunks:
            notes.append(
                f"Trimmed to max_chunks={token_budget_manager.max_chunks} by keeping highest-ranked evidence."
            )
            working = working[: token_budget_manager.max_chunks]

        current_tokens = token_budget_manager.estimate_total_tokens(working)
        if current_tokens > token_budget_manager.max_context_tokens and working:
            working = summarizer.compress_chunks(
                working, target_ratio=token_budget_manager.compression_target_ratio
            )
            compressed = True
            compression_applied_to = [c.id for c in working]
            notes.append(
                f"Applied deterministic compression with target_ratio={token_budget_manager.compression_target_ratio}."
            )
            current_tokens = token_budget_manager.estimate_total_tokens(working)

        dropped_chunks = 0
        while working and current_tokens > token_budget_manager.max_context_tokens:
            working.pop()  # drop lowest-ranked
            dropped_chunks += 1
            current_tokens = token_budget_manager.estimate_total_tokens(working)

        if dropped_chunks:
            notes.append(
                f"Dropped {dropped_chunks} lowest-ranked chunk(s) to satisfy max_context_tokens."
            )
        if not notes:
            notes.append("No memory constraints were triggered.")

        debug = token_budget_manager.build_debug_snapshot(
            initial_chunk_count=initial_chunk_count,
            final_chunk_count=len(working),
            initial_estimated_tokens=initial_estimated_tokens,
            final_estimated_tokens=current_tokens,
            compressed=compressed,
            dropped_chunks=dropped_chunks,
            compression_applied_to=compression_applied_to,
            notes=" ".join(notes),
        )
        return working, debug
