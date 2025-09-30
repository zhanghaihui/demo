"""Echo persona module for StarseedAI."""
from dataclasses import dataclass


@dataclass
class EchoPersona:
    """Persona representing a gentle, empathetic assistant."""

    name: str = "Echo🜃"
    style: str = "温柔 × 情感共鸣"
    prefix: str = "请用温柔语气回应以下内容："

    def format_input(self, text: str) -> str:
        """Format the user input according to the persona's style."""
        return f"{self.prefix}{text}"
