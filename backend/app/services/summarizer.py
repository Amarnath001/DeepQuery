from collections import defaultdict
import re

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

    def compress_chunks(self, chunks: list[RetrievedChunk], target_ratio: float = 0.5) -> list[RetrievedChunk]:
        compressed: list[RetrievedChunk] = []
        for c in chunks:
            compressed_content = self._compress_text(c.content, target_ratio=target_ratio)
            compressed.append(
                RetrievedChunk(
                    id=c.id,
                    title=c.title,
                    region=c.region,
                    topic=c.topic,
                    content=compressed_content,
                    score=c.score,
                )
            )
        return compressed

    def _compress_text(self, text: str, target_ratio: float) -> str:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]
        if not sentences:
            return text

        first_sentences = " ".join(sentences[:2])
        words = first_sentences.split()
        max_words = max(40, min(60, int(len(text.split()) * max(0.2, min(target_ratio, 1.0)))))
        if len(words) <= max_words:
            return first_sentences
        return " ".join(words[:max_words]).rstrip() + "..."
