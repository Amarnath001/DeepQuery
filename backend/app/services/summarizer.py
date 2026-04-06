from collections import defaultdict

from app.models.schemas import RetrievedChunk


class SummarizerService:
    """Summarizes retrieved chunks deterministically (no LLM)."""

    def summarize(self, chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return "No relevant evidence was retrieved from the local corpus."

        by_region: dict[str, list[RetrievedChunk]] = defaultdict(list)
        for c in chunks:
            by_region[c.region].append(c)

        lines: list[str] = []
        for region in sorted(by_region.keys()):
            region_chunks = sorted(by_region[region], key=lambda x: x.score, reverse=True)
            topics = sorted({c.topic for c in region_chunks})
            key_points = []
            for c in region_chunks[:2]:
                first_sentence = c.content.split(".")[0].strip()
                if first_sentence:
                    key_points.append(first_sentence)

            topic_str = ", ".join(topics) if topics else "general"
            points_str = "; ".join(key_points) if key_points else "Evidence available but content was sparse."
            lines.append(f"- {region} ({topic_str}): {points_str}.")

        return "\n".join(lines)
