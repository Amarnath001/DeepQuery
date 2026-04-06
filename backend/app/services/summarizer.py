class SummarizerService:
    """Summarizes retrieved chunks."""

    def summarize(self, chunks: list[dict]) -> str:
        if not chunks:
            return "No retrieved evidence yet. Summary placeholder."
        return "Summary placeholder generated from retrieved chunks."
