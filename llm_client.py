
"""LLM client interface and OpenAI provider for ARIA."""

import os
from typing import Callable

from dotenv import load_dotenv
from openai import OpenAI


class LLMConfigurationError(RuntimeError):
    """Raised when the LLM provider is not configured."""


class LLMProviderError(RuntimeError):
    """Raised when the LLM provider request fails."""


def get_openai_api_key() -> str:
    """Return the OpenAI API key from environment configuration."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY", "").strip()

    if not api_key:
        raise LLMConfigurationError(
            "OPENAI_API_KEY is missing. Configure it in your local .env file."
        )

    return api_key


def generate_with_openai(prompt: str) -> str:
    """Generate text using the OpenAI Responses API."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must not be empty.")

    api_key = get_openai_api_key()
    load_dotenv()

    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
    if not model:
        model = "gpt-4.1-mini"

    try:
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model,
            input=prompt.strip(),
        )
        text = response.output_text

        if not isinstance(text, str) or not text.strip():
            raise LLMProviderError(
                "The OpenAI provider returned an empty or invalid response."
            )

        return text.strip()

    except LLMProviderError:
        raise
    except Exception:
        raise LLMProviderError(
            "The OpenAI request failed. Check your API configuration, "
            "model access, network connection, and billing settings."
        ) from None


def create_openai_llm_client() -> "LLMClient":
    """Create an LLMClient configured to use OpenAI."""
    return LLMClient(generate_fn=generate_with_openai)


class LLMClient:
    """Small LLM interface with injectable text generation."""

    def __init__(
        self,
        generate_fn: Callable[[str], str] | None = None,
    ):
        self.generate_fn = generate_fn

    def generate(self, prompt: str) -> str:
        """Generate text using the configured provider."""
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("Prompt must not be empty.")

        if self.generate_fn is None:
            raise LLMConfigurationError("No LLM provider configured yet.")

        response = self.generate_fn(prompt.strip())

        if not isinstance(response, str) or not response.strip():
            raise RuntimeError(
                "The LLM provider returned an empty or invalid response."
            )

        return response.strip()
