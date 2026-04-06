class TokenBudgetManager:
    """Tracks token budget placeholders for debug visibility."""

    def __init__(self, allocated_tokens: int = 4000) -> None:
        self.allocated_tokens = allocated_tokens
        self.used_tokens = 0

    def get_debug_snapshot(self) -> dict:
        return {
            "allocated_tokens": self.allocated_tokens,
            "used_tokens": self.used_tokens,
            "remaining_tokens": max(self.allocated_tokens - self.used_tokens, 0),
            "notes": "Token accounting is a placeholder in Milestone 1.",
        }
