from __future__ import annotations

import asyncio

from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from app.config import settings
from app.exceptions import (
    GeminiApiError,
    GeminiInvalidResponseError,
    GeminiTimeoutError,
)
from app.models.schemas import AnalysisResult

_client: genai.Client | None = None

_MERMAID_START_KEYWORDS = ("flowchart", "graph", "classdiagram")
_RETRY_BACKOFF_SECONDS = 2.0


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


def _sanity_check_mermaid(value: str, field_name: str) -> None:
    stripped = value.strip()
    first_line = stripped.splitlines()[0].strip().lower() if stripped else ""
    if not any(first_line.startswith(keyword) for keyword in _MERMAID_START_KEYWORDS):
        raise GeminiInvalidResponseError(
            f"O campo '{field_name}' não começou com uma diretiva Mermaid válida."
        )


async def _call_gemini(client: genai.Client, prompt: str):
    return await asyncio.wait_for(
        client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(url_context=types.UrlContext())],
                response_mime_type="application/json",
                response_schema=AnalysisResult,
            ),
        ),
        timeout=settings.gemini_timeout_seconds,
    )


async def generate_analysis(prompt: str) -> AnalysisResult:
    client = _get_client()

    try:
        response = await _call_gemini(client, prompt)
    except asyncio.TimeoutError as exc:
        raise GeminiTimeoutError("A análise por IA demorou demais e expirou.") from exc
    except genai_errors.ServerError:
        # Sobrecarga transitória do lado do Gemini (5xx): 1 nova tentativa, sem mais.
        await asyncio.sleep(_RETRY_BACKOFF_SECONDS)
        try:
            response = await _call_gemini(client, prompt)
        except asyncio.TimeoutError as exc:
            raise GeminiTimeoutError("A análise por IA demorou demais e expirou.") from exc
        except genai_errors.APIError as exc:
            raise GeminiApiError(f"Erro ao consultar a API do Gemini: {exc}") from exc
    except genai_errors.APIError as exc:
        raise GeminiApiError(f"Erro ao consultar a API do Gemini: {exc}") from exc

    if not response.text:
        raise GeminiInvalidResponseError("O Gemini retornou uma resposta vazia.")

    try:
        result = AnalysisResult.model_validate_json(response.text)
    except ValueError as exc:
        raise GeminiInvalidResponseError(
            "A resposta do Gemini não pôde ser interpretada como JSON válido."
        ) from exc

    _sanity_check_mermaid(result.flowchart, "flowchart")
    _sanity_check_mermaid(result.diagram, "diagram")

    return result
