
"""Provider-independent interface for ARIA's LLM calls."""

import os
from typing import Callable


class LLMConfigurationError(RuntimeError):
    """Raised when the LLM provider is not configured."""


def get_openai_api_key() -> str:
    """Return the OpenAI API key from environment configuration."""
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise LLMConfigurationError(
            "OPENAI_API_KEY is missing. Configure it in your local .env file."
        )

    return api_key


class LLMClient:
    """Small LLM interface with an injectable text-generation function."""

    def __init__(
        self,
        generate_fn: Callable[[str], str] | None = None,
    ):
        self.generate_fn = generate_fn

    def generate(self, prompt: str) -> str:
        """Generate text from a prompt using the configured provider."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must not be empty.")

        if self.generate_fn is None:
            raise LLMConfigurationError("No LLM provider configured yet.")

        response = self.generate_fn(prompt)

        if not isinstance(response, str) or not response.strip():
            raise RuntimeError(
                "The LLM provider returned an empty or invalid response."
            )

        return response.strip()
