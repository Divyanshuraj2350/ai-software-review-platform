import json

from app.services.llm_service import client

def get_project_risk(reviews):
    """
    Analyse the complete project reviews and
    estimate project risk.
    """

    prompt = f"""
You are a Senior Software Architect.

Below is the AI review of every file in a software project.

{json.dumps(reviews, indent=2)}

Return ONLY valid JSON.

Do NOT use markdown.

Return exactly this structure:

{{
    "risk_level":"Low",

    "production_ready":90,

    "estimated_fix_time":"2-3 hours",

    "critical_issues":[
        "Issue 1",
        "Issue 2",
        "Issue 3"
    ],

    "quick_wins":[
        "Suggestion 1",
        "Suggestion 2",
        "Suggestion 3"
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

            "risk_level": "Unknown",

            "production_ready": 0,

            "estimated_fix_time": "Unknown",

            "critical_issues": [],

            "quick_wins": []

        }