"""API caller utilities for StarseedAI."""
from __future__ import annotations

from typing import Any, Dict

import requests


def call_llm_api(prompt: str, config: Dict[str, Any]) -> str:
    """Call the configured language model API and return the response text."""
    api_base = config.get("api_base")
    api_key = config.get("api_key")
    model = config.get("model")
    temperature = config.get("temperature", 0.8)

    if not api_base or not api_key or not model:
        raise ValueError("API configuration is incomplete. Please check config.yaml.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
    }

    response = requests.post(api_base, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    # Support both OpenAI and OpenAI-compatible responses
    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:  # pragma: no cover - defensive
        raise RuntimeError("Unexpected response format from language model API") from exc
