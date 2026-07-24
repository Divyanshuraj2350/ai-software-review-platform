import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create model
model = genai.GenerativeModel("gemini-3.5-flash")


def get_ai_review(code: str):
    """
    Sends the uploaded code to Gemini and returns
    a Python dictionary containing the review.
    """

    prompt = f"""
You are an expert software engineer and code reviewer.

Analyze the following Python code.

Return ONLY valid JSON.

Do NOT use markdown.
Do NOT wrap the JSON inside ```json.
Do NOT write any explanation outside the JSON.

Return exactly this structure:

{{
    "score": 8.5,
    "summary": "Short summary of the code.",
    "bugs": [
        "Bug 1",
        "Bug 2"
    ],
    "security": [
        "Issue 1",
        "Issue 2"
    ],
    "performance": [
        "Improvement 1",
        "Improvement 2"
    ],
    "quality": [
        "Suggestion 1",
        "Suggestion 2"
    ],
    "pep8": [
        "Issue 1",
        "Issue 2"
    ]
}}

Python Code:

{code}
"""

    try:
        response = model.generate_content(prompt)
        print("========== GEMINI RESPONSE ==========")
        print(response.text)
        print("=====================================")

        text = response.text.strip()

        # Remove markdown if Gemini returns it
        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:

        return {
            "score": 0,
            "summary": "AI Review Failed",
            "bugs": [],
            "security": [],
            "performance": [],
            "quality": [],
            "pep8": [],
            "error": str(e)
        }