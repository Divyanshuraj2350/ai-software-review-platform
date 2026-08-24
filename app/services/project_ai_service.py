from app.services.llm_service import client
from google.genai import types
import json


def get_project_overview(reviews):
    """
    Generate an AI overview for the whole project.
    """

    prompt = f"""
You are a senior software architect reviewing a software project.

Analyze the following file reviews:

{json.dumps(reviews, indent=2)}

Return ONLY valid JSON.

Use exactly this schema:

{{
    "health_score": 8.5,
    "architecture": "Brief assessment of project architecture.",
    "security": "Brief assessment of project security.",
    "performance": "Brief assessment of project performance.",
    "maintainability": "Brief assessment of project maintainability.",
    "priorities": [
        "Priority improvement 1",
        "Priority improvement 2",
        "Priority improvement 3",
        "Priority improvement 4",
        "Priority improvement 5"
    ]
}}

Rules:
- health_score must be between 0 and 10.
- priorities must contain up to 5 useful improvements.
- Do not use markdown.
- Do not add any text outside the JSON object.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2,
            ),
        )

        text = response.text.strip()

        # Remove markdown fences if Gemini still returns them
        if text.startswith("```"):
            lines = text.splitlines()

            if lines and lines[0].startswith("```"):
                lines = lines[1:]

            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]

            text = "\n".join(lines).strip()

        # Parse JSON
        data = json.loads(text)

        # Basic validation
        data["health_score"] = float(data.get("health_score", 0))
        data["architecture"] = data.get("architecture", "Not Available")
        data["security"] = data.get("security", "Not Available")
        data["performance"] = data.get("performance", "Not Available")
        data["maintainability"] = data.get(
            "maintainability",
            "Not Available"
        )
        data["priorities"] = data.get("priorities", [])

        print("\n========== PROJECT AI RESPONSE ==========")
        print(json.dumps(data, indent=2))
        print("=========================================\n")

        return data

    except Exception as e:

        print("\n========== PROJECT AI FAILED ==========")
        print(type(e).__name__)
        print(str(e))
        print("=======================================\n")

        return {
            "health_score": 0,
            "architecture": "Not Available",
            "security": "Not Available",
            "performance": "Not Available",
            "maintainability": "Not Available",
            "priorities": [],
        }