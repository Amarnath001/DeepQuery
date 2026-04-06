class PlannerService:
    """Creates sub-questions from the user query."""

    def plan(self, query: str) -> list[str]:
        q = query.strip().rstrip("?")
        if not q:
            q = "EV battery recycling"

        comparison = (
            f"How do approaches differ across the US, EU, and China for {q} "
            "(policy, infrastructure, and industry players)?"
        )
        policy = f"What regulations and government policies most shape outcomes for {q} in each region?"
        market = f"What market trends, risks, and supply-chain constraints are emerging for {q} across regions?"

        return [comparison, policy, market]
