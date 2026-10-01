import json
import re

from fastapi import APIRouter
from pydantic import BaseModel, Field

from config import settings

router = APIRouter(prefix="/api")

class StoryRequest(BaseModel):
    idea: str = Field(min_length=1)
    characters: str = ""
    style: str = "funny"
    panels: int = Field(default=4, ge=2, le=8)

def clean_json_text(text: str) -> str:
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()

@router.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}

@router.post("/generate")
def generate_story(payload: StoryRequest):
    if not settings.gemini_api_key:
        return {
            "ok": False,
            "message": "Gemini API key is missing. Add GEMINI_API_KEY to the root .env file.",
        }

    try:
        from google import genai
        client = genai.Client(api_key=settings.gemini_api_key)

        prompt = f"""
Create a short comic story.

Story idea: {payload.idea}
Characters: {payload.characters or "Create suitable characters"}
Style: {payload.style}
Number of panels: {payload.panels}

Return ONLY valid JSON. Do not use Markdown or code fences.

Use exactly this structure:
{{
  "title": "string",
  "summary": "string",
  "panels": [
    {{
      "panel": 1,
      "scene": "string",
      "dialogue": "string"
    }}
  ]
}}

The panels array must contain exactly {payload.panels} panels.
"""

        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        raw = clean_json_text(response.text or "")
        result = json.loads(raw)

        if not isinstance(result, dict) or not isinstance(result.get("panels"), list):
            raise ValueError("Gemini returned an unexpected response format.")

        return {"ok": True, "result": result}

    except json.JSONDecodeError:
        return {
            "ok": False,
            "message": "Gemini returned invalid JSON. Please try Generate Comic again.",
        }
    except Exception as exc:
        return {"ok": False, "message": str(exc)}
