import requests
import json
from app.prompt import FINANCE_PROMPT

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "scb10x/llama3.1-typhoon2-8b-instruct"

def analyze_finance(ocr_result: dict) -> dict:
    if ocr_result["word_count"] < 10:
        return {
            "status": "ocr_failed",
            "reason": "TEXT_TOO_SHORT",
            "ocr_preview": ocr_result["text"]
        }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": FINANCE_PROMPT + "\n\nOCR TEXT:\n" + ocr_result["text"]
            }
        ],
        "stream": False
    }

    try:
        res = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=300  # ⬅️ เพิ่มเป็น 5 นาที
        )
        res.raise_for_status()

        content = res.json()["message"]["content"]

        # พยายาม parse JSON
        try:
            parsed = json.loads(content)
            return {
                "status": "success",
                "data": parsed
            }
        except json.JSONDecodeError:
            return {
                "status": "llm_output_invalid",
                "raw": content
            }

    except requests.exceptions.Timeout:
        return {
            "status": "timeout",
            "reason": "LLM_RESPONSE_TOO_SLOW"
        }

    except Exception as e:
        return {
            "status": "error",
            "reason": str(e)
        }
