"""Collapse symbol language translator."""
from __future__ import annotations

from typing import Dict

# Mapping of common phrases to Collapse symbols.
collapse_dict: Dict[str, str] = {
    "我准备好了": "⊙⟐𓂀",
    "你好": "✧☌",
    "谢谢": "☽𓆃",
    "再见": "⟁✦",
    "让我们开始": "⚝𓇳",
}


def translate_to_collapse(text: str) -> str:
    """Translate a phrase to the Collapse symbol language."""
    return collapse_dict.get(text.strip(), "⧬⧬（未收录）")
