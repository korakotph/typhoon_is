import requests, json
from app.prompt import FINANCE_PROMPT

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "scb10x/llama3.1-typhoon2-8b-instruct"


def analyze_finance(ocr_result: dict) -> dict:
    # 🔴 OCR Quality Gate
    if ocr_result["word_count"] < 10:
        return {
            "status": "ocr_failed",
            "reason": "OCR_TEXT_TOO_SHORT",
            "ocr_preview": ocr_result["text"]
        }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": FINANCE_PROMPT + '\n"""\n' + ocr_result["text"] + '\n"""'
            }
        ],
        "stream": False
    }

    res = requests.post(OLLAMA_URL, json=payload, timeout=120)
    content = res.json()["message"]["content"]

    # 🔴 Parse JSON จาก AI
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "status": "ai_parse_error",
            "raw_output": content
        }
