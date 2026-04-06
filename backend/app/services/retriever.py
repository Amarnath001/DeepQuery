class RetrieverService:
    """Retrieves relevant chunks for planned sub-questions."""

    def retrieve(self, sub_questions: list[str]) -> list[dict]:
        # Placeholder: later milestones will query a vector store or search API.
        first_sub_question = sub_questions[0] if sub_questions else "No sub-question provided."
        return [
            {
                "source": "mock_source",
                "title": "Mock Retrieved Document",
                "content": f"Placeholder chunk related to: {first_sub_question}",
                "score": 0.92,
            }
        ]
