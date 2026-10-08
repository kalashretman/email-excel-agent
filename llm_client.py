"""Thin wrapper around the Claude API: one client, one helper, cost tracking."""

from dataclasses import dataclass
from functools import lru_cache

import anthropic

from config import ANTHROPIC_API_KEY, LLM_MODEL, PRICE_INPUT_PER_MTOK, PRICE_OUTPUT_PER_MTOK


@dataclass
class LLMAnswer:
    """Model reply plus token usage and estimated cost of the call."""
    text: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


@lru_cache(maxsize=1)
def get_client() -> anthropic.Anthropic:
    """Create the API client once and reuse it (lru_cache = simple singleton)."""
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY is empty: add it to your .env file")
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    """Approximate cost in USD from token counts and prices in config."""
    return (input_tokens * PRICE_INPUT_PER_MTOK + output_tokens * PRICE_OUTPUT_PER_MTOK) / 1_000_000


def text_of(response) -> str:
    """Join all text blocks of a response (a reply can contain several blocks)."""
    return "".join(block.text for block in response.content if block.type == "text")


def ask(prompt: str, system: str | None = None, max_tokens: int = 512) -> LLMAnswer:
    """Send one user message and return the text answer with usage stats."""
    kwargs = {
        "model": LLM_MODEL,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    if system:
        kwargs["system"] = system

    response = get_client().messages.create(**kwargs)
    usage = response.usage
    return LLMAnswer(
        text=text_of(response),
        input_tokens=usage.input_tokens,
        output_tokens=usage.output_tokens,
        cost_usd=estimate_cost(usage.input_tokens, usage.output_tokens),
    )