class AnswererService:
    """Produces the final user-facing answer."""

    def answer(self, query: str, summary: str) -> str:
        return (
            f"Placeholder final answer for query: '{query}'. "
            f"Current synthesized summary: '{summary}'. "
            "A full answer synthesis pipeline will be added in later milestones."
        )
