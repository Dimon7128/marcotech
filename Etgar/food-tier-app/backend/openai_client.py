"""
External-API tier: a thin wrapper around the OpenAI Chat Completions API.

The wrapper is deliberately small. It:
  1. Loads the API key from the environment (populated from .env).
  2. Sends the fixed nutrition-classifier prompt.
  3. Validates that the model returned the exact JSON shape we expect.

If anything goes wrong (missing key, network error, malformed JSON, invalid
tier) we raise `OpenAIClassificationError` with a clear message. The API
layer in main.py turns that into a 4xx/5xx HTTP response.
"""

from __future__ import annotations

import json 
import os
from typing import Tuple

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# The exact prompt requested in the spec. We use `.format(food=...)` to
# inject the user's input at call time. The trailing instruction to return
# JSON only is critical — combined with `response_format={"type":"json_object"}`
# it gives us a reliable, parseable answer.
PROMPT_TEMPLATE = """You are a simple nutrition classifier for educational purposes.

Classify the given food into one of three tiers:

A = generally nutritious / good everyday option
B = okay / depends on context / moderate option
C = less nutritious / should be limited

Return only valid JSON in this format:
{{
  "tier": "A" | "B" | "C",
  "explanation": "one short sentence explaining why"
}}

Food:
{food}"""


class OpenAIClassificationError(Exception):
    """Raised when we cannot get a valid classification from OpenAI."""


def _get_client() -> OpenAI:
    """Build a fresh client and verify the API key is present.

    We build the client lazily (instead of at import time) so that the
    backend can still boot and serve `/health` even if the key is missing —
    the failure is only surfaced when somebody actually calls the API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("sk-your-"):
        raise OpenAIClassificationError(
            "OPENAI_API_KEY is not set. Copy backend/.env.example to "
            "backend/.env and paste your real key."
        )
    return OpenAI(api_key=api_key)


def classify(food: str) -> Tuple[str, str]:
    """Ask OpenAI to classify `food` and return (tier, explanation).

    Raises:
        OpenAIClassificationError: on any failure (network, parsing,
            validation). The message is safe to forward to the user.
    """
    client = _get_client()
    prompt = PROMPT_TEMPLATE.format(food=food)

    try:
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            # Force the model to return a JSON object so json.loads cannot
            # be tricked by stray prose around the JSON block.
            response_format={"type": "json_object"},
            temperature=0,
        )
    except OpenAIError as exc:
        raise OpenAIClassificationError(f"OpenAI request failed: {exc}") from exc

    content = (response.choices[0].message.content or "").strip()
    if not content:
        raise OpenAIClassificationError("OpenAI returned an empty response.")

    try:
        payload = json.loads(content)
    except json.JSONDecodeError as exc:
        raise OpenAIClassificationError(
            f"OpenAI returned non-JSON content: {content!r}"
        ) from exc

    tier = payload.get("tier")
    explanation = payload.get("explanation")

    if tier not in {"A", "B", "C"}:
        raise OpenAIClassificationError(
            f"Invalid tier {tier!r} from OpenAI; expected 'A', 'B' or 'C'."
        )
    if not isinstance(explanation, str) or not explanation.strip():
        raise OpenAIClassificationError(
            "OpenAI response is missing a non-empty 'explanation' string."
        )

    return tier, explanation.strip()
