"""Routes for external AI assistant integration."""
import json
import logging
import os
from datetime import datetime, timezone

import requests
from fastapi import APIRouter, HTTPException

from .. import config
from ..schemas import KimiRequest, KimiResponse

router = APIRouter(prefix="/api", tags=["assistant"])
logger = logging.getLogger(__name__)

ASSISTANT_PROMPT_TEMPLATE = """You are an airline customer experience analyst.
Analyze the following passenger data and prediction result.

Focus on the main complaint, root cause, and likely improvement area.
Return a concise but useful summary in plain language.

Passenger data:
{message}
"""


def build_assistant_prompt(message: str) -> str:
    """Build the backend prompt used for the LLM request."""
    return ASSISTANT_PROMPT_TEMPLATE.format(message=message.strip())


def save_assistant_answer(answer: str, model: str, used_image: bool, original_message: str) -> None:
    """Persist the AI assistant response as JSON for later review."""
    try:
        data = []
        if config.ASSISTANT_LOG_PATH.exists():
            with config.ASSISTANT_LOG_PATH.open("r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []

        record = {
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "used_image": used_image,
            "message": original_message,
            "answer": answer,
        }
        data.append(record)

        with config.ASSISTANT_LOG_PATH.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except Exception:
        logger.exception("Failed to save assistant response to JSON log")


@router.post("/assistant", response_model=KimiResponse)
async def call_kimi(request: KimiRequest) -> KimiResponse:
    """Send a text or image prompt to the configured OpenAI-compatible endpoint and return the answer."""
    api_key = config.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="OPENAI_API_KEY is missing. Set it in the environment before calling this endpoint.",
        )

    content = build_assistant_prompt(request.message)
    if request.image_url:
        content = [
            {"type": "text", "text": content},
            {"type": "image_url", "image_url": {"url": request.image_url}},
        ]

    payload = {
        "model": config.OPENAI_MODEL,
        "messages": [{"role": "user", "content": content}],
        "max_tokens": 300,
        "temperature": 0.3,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            config.OPENAI_API_URL,
            headers=headers,
            json=payload,
            timeout=(10, 60),
        )
        response.raise_for_status()
        data = response.json()
        raw_content = data["choices"][0]["message"]["content"]
        if isinstance(raw_content, list):
            answer = "".join(part.get("text", "") for part in raw_content if isinstance(part, dict))
        else:
            answer = str(raw_content)

        save_assistant_answer(
            answer=answer,
            model=config.OPENAI_MODEL,
            used_image=bool(request.image_url),
            original_message=request.message,
        )

        return KimiResponse(
            answer=answer,
            model=config.OPENAI_MODEL,
            used_image=bool(request.image_url),
        )
    except requests.exceptions.Timeout as exc:
        logger.exception("OpenAI request timed out")
        raise HTTPException(
            status_code=504,
            detail="OpenAI request timed out. The provider may be slow or temporarily unavailable.",
        ) from exc
    except requests.exceptions.RequestException as exc:
        logger.exception("OpenAI request failed")
        raise HTTPException(status_code=502, detail=f"OpenAI request failed: {exc}") from exc
    except (KeyError, IndexError, ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=502,
            detail="Unexpected response format from the OpenAI API.",
        ) from exc
