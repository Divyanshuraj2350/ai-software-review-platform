import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3.5-flash")


def get_ai_review(code: str, language: str):

    prompt = f"""
You are a Senior {language} Software Engineer with 15+ years of experience.

Review this {language} code professionally.

Return ONLY valid JSON.

Return exactly this schema:

{{
    "score": 8.5,
    "summary": "",
    "strengths": [],
    "weaknesses": [],
    "suggestions": [],
    "quality": {{
        "readability": 8,
        "performance": 8,
        "security": 8,
        "maintainability": 8
    }},
    "bugs": [],
    "security": [],
    "performance": [],
    "pep8": []
}}

Code:

{code}
"""

    try:

        response = model.generate_content(prompt)

        text = getattr(response, "text", "")

        print("\n========== GEMINI RESPONSE ==========")
        print(text)
        print("=====================================\n")

        if not text:
            raise Exception("Gemini returned an empty response.")

        text = text.strip()

        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        text = text.strip()

        return json.loads(text)

    except Exception as e:

        print("\n========== AI REVIEW FAILED ==========")
        print(type(e).__name__)
        print(str(e))
        print("======================================\n")

        return {
            "score": 0,
            "summary": "AI Review Failed",
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "quality": {
                "readability": 0,
                "performance": 0,
                "security": 0,
                "maintainability": 0
            },
            "bugs": [],
            "security": [],
            "performance": [],
            "pep8": [],
            "error": f"{type(e).__name__}: {e}"
        }