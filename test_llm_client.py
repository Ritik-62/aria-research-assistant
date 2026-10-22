
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from llm_client import (
    LLMClient,
    LLMConfigurationError,
    LLMProviderError,
    get_openai_api_key,
    generate_with_openai,
    create_openai_llm_client,
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
        client = LLMClient(generate_fn=lambda prompt: "   ")
        with self.assertRaises(RuntimeError):
            client.generate("Summarize these papers")

    def test_rejects_non_string_provider_response(self):
        client = LLMClient(generate_fn=lambda prompt: None)
        with self.assertRaises(RuntimeError):
            client.generate("Summarize these papers")

    def test_requires_openai_api_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with patch("llm_client.load_dotenv"):
                with self.assertRaises(LLMConfigurationError):
                    get_openai_api_key()


class TestOpenAIProvider(unittest.TestCase):
    @patch("llm_client.OpenAI")
    @patch("llm_client.get_openai_api_key", return_value="test-key")
    def test_generates_text(self, mock_key, mock_openai):
        mock_openai.return_value.responses.create.return_value = (
            SimpleNamespace(output_text="A useful research summary.")
        )

        result = generate_with_openai("Summarize this paper")

        self.assertEqual(result, "A useful research summary.")
        mock_openai.return_value.responses.create.assert_called_once()

    @patch("llm_client.OpenAI")
    @patch("llm_client.get_openai_api_key", return_value="test-key")
    def test_reports_provider_failure(self, mock_key, mock_openai):
        mock_openai.return_value.responses.create.side_effect = (
            RuntimeError("simulated failure")
        )

        with self.assertRaises(LLMProviderError):
            generate_with_openai("Summarize this paper")

    @patch("llm_client.OpenAI")
    @patch("llm_client.get_openai_api_key", return_value="test-key")
    def test_rejects_empty_openai_response(self, mock_key, mock_openai):
        mock_openai.return_value.responses.create.return_value = (
            SimpleNamespace(output_text="  ")
        )

        with self.assertRaises(LLMProviderError):
            generate_with_openai("Summarize this paper")

    def test_creates_configured_client(self):
        client = create_openai_llm_client()

        self.assertIsInstance(client, LLMClient)
        self.assertIsNotNone(client.generate_fn)


if __name__ == "__main__":
    unittest.main()
