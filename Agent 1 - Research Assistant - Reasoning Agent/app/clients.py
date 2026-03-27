from __future__ import annotations

import time
from typing import Any, Iterable

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings


class OpenAICompatibleClient:
    def __init__(self, base_url: str, api_key: str, timeout: float = 120.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    @property
    def headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
    def post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}{path}",
                headers=self.headers,
                json=payload,
            )
            response.raise_for_status()
            return response.json()


class LLMClient(OpenAICompatibleClient):
    def generate(self, question: str, contexts: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
        started = time.perf_counter()
        prompt = self._build_prompt(question, contexts)
        payload = {
            "model": settings.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a research assistant. Answer only from provided paper context. "
                        "Always cite paper titles inline in square brackets."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        }
        data = self.post("/completions", payload)
        latency_ms = (time.perf_counter() - started) * 1000.0
        answer = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        return answer, {"llm_latency_ms": latency_ms, "usage": usage}

    @staticmethod
    def _build_prompt(question: str, contexts: list[dict[str, Any]]) -> str:
        context_lines = []
        for idx, ctx in enumerate(contexts, start=1):
            context_lines.append(
                f"[{idx}] Title: {ctx['title']}\n"
                f"Published: {ctx.get('published')}\n"
                f"URL: {ctx['url']}\n"
                f"Snippet: {ctx['snippet']}"
            )
        return f"Question: {question}\n\nContexts:\n\n" + "\n\n".join(context_lines)


class EmbeddingClient(OpenAICompatibleClient):
    def embed_texts(self, texts: Iterable[str], input_type: str = "passage") -> list[list[float]]:
        payload = {
            "model": settings.embedding_model,
            "input": list(texts),
            "input_type": input_type,
        }
        data = self.post("/embeddings", payload)
        return [row["embedding"] for row in data["data"]]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_texts([text], input_type="query")[0]

    def embed_passages(self, texts: Iterable[str]) -> list[list[float]]:
        return self.embed_texts(texts, input_type="passage")


class RerankClient(OpenAICompatibleClient):
    def rerank(self, query: str, documents: list[str], top_n: int) -> list[dict[str, Any]]:
        payload = {
            "model": settings.rerank_model,
            "query": query,
            "documents": documents,
            "top_n": top_n,
        }
        try:
            data = self.post("/rerank", payload)
            return data.get("results", [])
        except Exception:
            return [{"index": i, "relevance_score": float(len(doc))} for i, doc in enumerate(documents[:top_n])]
        
