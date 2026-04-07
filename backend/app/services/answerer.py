from app.models.schemas import RetrievedChunk


class AnswererService:
    """Produces the final user-facing answer."""

    def answer(
        self,
        query: str,
        summary: str,
        chunks: list[RetrievedChunk],
        constrained: bool = False,
    ) -> str:
        regions = sorted({c.region for c in chunks}) if chunks else []
        topics = sorted({c.topic for c in chunks}) if chunks else []

        region_str = ", ".join(regions) if regions else "no specific regions (low-signal retrieval)"
        topic_str = ", ".join(topics) if topics else "no specific topics"

        evidence_highlights = []
        for c in sorted(chunks, key=lambda x: x.score, reverse=True)[:3]:
            evidence_highlights.append(f"{c.region}/{c.topic}: {c.title}")

        highlights_str = "; ".join(evidence_highlights) if evidence_highlights else "No strong evidence highlights."
        evidence_note = (
            "Evidence was compressed and/or trimmed to satisfy the context budget. "
            if constrained
            else ""
        )

        return (
            f"Query: {query}\n\n"
            f"{evidence_note}"
            f"Summary (from local corpus):\n{summary}\n\n"
            f"Evidence coverage: regions={region_str}; topics={topic_str}.\n"
            f"Top evidence highlights: {highlights_str}."
        )
