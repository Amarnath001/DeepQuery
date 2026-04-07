class PlannerService:
    """Creates sub-questions from the user query."""

    def plan(self, query: str) -> list[str]:
        topic = query.strip().rstrip("?")
        if not topic:
            topic = "EV battery recycling"

        comparison = "How do the US, EU, and China differ in policy, infrastructure, and industry approach?"
        policy = f"Which regulations and government policy signals are most relevant to {topic}?"
        market = f"What market trends, risks, and supply-chain constraints are shaping {topic}?"

        return [comparison, policy, market]
