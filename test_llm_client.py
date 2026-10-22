
import os
import unittest
from unittest.mock import patch

from llm_client import (
    LLMClient,
    LLMConfigurationError,
    get_openai_api_key,
)


class TestLLMClient(unittest.TestCase):
    def test_returns_generated_text(self):
        client = LLMClient(
            generate_fn=lambda prompt: "  Research summary  "
        )

        self.assertEqual(
            client.generate("Summarize these papers"),
            "Research summary",
        )

    def test_rejects_empty_prompt(self):
        client = LLMClient(
            generate_fn=lambda prompt: "response"
        )

        with self.assertRaises(ValueError):
            client.generate("  ")

    def test_requires_provider(self):
        client = LLMClient()

        with self.assertRaises(LLMConfigurationError):
            client.generate("Summarize these papers")

    def test_rejects_empty_provider_response(self):
        client = LLMClient(
            generate_fn=lambda prompt: "   "
        )

        with self.assertRaises(RuntimeError):
            client.generate("Summarize these papers")

    def test_rejects_non_string_provider_response(self):
        client = LLMClient(
            generate_fn=lambda prompt: None
        )

        with self.assertRaises(RuntimeError):
            client.generate("Summarize these papers")

    def test_requires_openai_api_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with patch("dotenv.load_dotenv"):
                with self.assertRaises(LLMConfigurationError):
                    get_openai_api_key()


if __name__ == "__main__":
    unittest.main()
