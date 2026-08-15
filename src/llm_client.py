"""Shared Gemini client used by the application."""

from google import genai


_client: genai.Client | None = None


def get_genai_client() -> genai.Client:
    """Return the single Gemini client instance for this process."""
    global _client
    if _client is None:
        _client = genai.Client()
    return _client
