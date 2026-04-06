import json
import re
from pathlib import Path

from app.models.schemas import RetrievedChunk


class RetrieverService:
    """Retrieves relevant chunks for planned sub-questions from a local JSON corpus."""

    def __init__(self) -> None:
        self._corpus_cache: list[dict] | None = None

    def retrieve(self, query: str, sub_questions: list[str], top_k: int = 5) -> list[RetrievedChunk]:
        corpus = self.load_corpus()
        query_tokens = self.tokenize(query)
        sq_tokens = set()
        for sq in sub_questions:
            sq_tokens |= self.tokenize(sq)

        scored: list[RetrievedChunk] = []
        for item in corpus:
            score = self.score_chunk(query_tokens=query_tokens, sub_question_tokens=sq_tokens, item=item)
            if score <= 0:
                continue
            scored.append(
                RetrievedChunk(
                    id=item["id"],
                    title=item["title"],
                    region=item["region"],
                    topic=item["topic"],
                    content=item["content"],
                    score=score,
                )
            )

        scored.sort(key=lambda c: c.score, reverse=True)
        if scored:
            return scored[:top_k]

        # Fallback: if everything scores zero, return a few items with very low scores.
        fallback = corpus[:3]
        return [
            RetrievedChunk(
                id=item["id"],
                title=item["title"],
                region=item["region"],
                topic=item["topic"],
                content=item["content"],
                score=0.01,
            )
            for item in fallback
        ]

    def load_corpus(self) -> list[dict]:
        if self._corpus_cache is not None:
            return self._corpus_cache

        backend_dir = Path(__file__).resolve().parents[2]
        corpus_path = backend_dir / "data" / "processed" / "sample_corpus.json"
        raw = corpus_path.read_text(encoding="utf-8")
        data = json.loads(raw)
        if not isinstance(data, list):
            raise ValueError("sample_corpus.json must be a JSON array")

        self._corpus_cache = data
        return data

    def tokenize(self, text: str) -> set[str]:
        tokens = re.findall(r"[a-z0-9]+", (text or "").lower())
        stopwords = {
            "the",
            "and",
            "or",
            "a",
            "an",
            "to",
            "for",
            "of",
            "in",
            "on",
            "with",
            "by",
            "across",
            "how",
            "do",
            "are",
            "is",
            "what",
            "most",
            "each",
        }
        return {t for t in tokens if t not in stopwords and len(t) > 2}

    def score_chunk(self, query_tokens: set[str], sub_question_tokens: set[str], item: dict) -> float:
        haystack = " ".join(
            [
                str(item.get("title", "")),
                str(item.get("region", "")),
                str(item.get("topic", "")),
                str(item.get("content", "")),
            ]
        )
        chunk_tokens = self.tokenize(haystack)
        if not chunk_tokens:
            return 0.0

        overlap_query = len(chunk_tokens & query_tokens)
        overlap_sq = len(chunk_tokens & sub_question_tokens)

        # Favor direct query overlap, but let sub-questions contribute meaningfully.
        return (2.0 * overlap_query) + (1.0 * overlap_sq)
