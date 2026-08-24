from app.services.llm_service import client
import json


def get_project_overview(reviews):
    """
    Generate an AI overview for the whole project.
    """

    prompt = f"""
You are a senior software architect.

Below are reviews for multiple Python files.

{json.dumps(reviews, indent=2)}

Write ONLY valid JSON.

Return exactly:

{{
    "health_score": 8.5,

    "architecture": "...",

    "security": "...",

    "performance": "...",

    "maintainability": "...",

    "priorities":[
        "...",
        "...",
        "...",
        "...",
        "..."
    ]
}}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()

        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception:

        return {

            "health_score": 0,

            "architecture": "Not Available",

            "security": "Not Available",

            "performance": "Not Available",

            "maintainability": "Not Available",

            "priorities": []

        }