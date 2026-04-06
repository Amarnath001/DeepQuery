class PlannerService:
    """Creates sub-questions from the user query."""

    def plan(self, query: str) -> list[str]:
        return [
            f"What are the key themes in: {query}?",
            "What supporting facts should be collected?",
            "What constraints or trade-offs should be considered?",
        ]
