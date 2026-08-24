import os
import json

from google import genai
from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


REVIEW_SCHEMA = {
    "type": "object",
    "properties": {

        "score": {
            "type": "number",
            "minimum": 0,
            "maximum": 10
        },

        "summary": {
            "type": "string"
        },

        "strengths": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "weaknesses": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "suggestions": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },

        "quality": {
            "type": "object",
            "properties": {

                "readability": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 10
                },

                "performance": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 10
                },

                "security": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 10
                },

                "maintainability": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 10
                }

            },
            "required": [
                "readability",
                "performance",
                "security",
                "maintainability"
            ]
        },

        "bugs": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "line": {
                        "type": "integer"
                    },
                    "message": {
                        "type": "string"
                    }
                },
                "required": [
                    "line",
                    "message"
                ]
            }
        },

        "security": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "line": {
                        "type": "integer"
                    },
                    "message": {
                        "type": "string"
                    }
                },
                "required": [
                    "line",
                    "message"
                ]
            }
        },

        "performance": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "line": {
                        "type": "integer"
                    },
                    "message": {
                        "type": "string"
                    }
                },
                "required": [
                    "line",
                    "message"
                ]
            }
        },

        "pep8": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "line": {
                        "type": "integer"
                    },
                    "message": {
                        "type": "string"
                    }
                },
                "required": [
                    "line",
                    "message"
                ]
            }
        }
    },

    "required": [
        "score",
        "summary",
        "strengths",
        "weaknesses",
        "suggestions",
        "quality",
        "bugs",
        "security",
        "performance",
        "pep8"
    ]
}


def normalize_score(value):
    """
    Keep every score between 0 and 10.
    """

    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0

    if score > 10:
        score = score / 10

    return round(max(0.0, min(score, 10.0)), 2)


def get_ai_review(code: str, language: str):

    prompt = f"""
You are a Senior {language} Software Engineer with 15+ years of
professional software development experience.

Review the following {language} code carefully.

Analyze:

- correctness
- actual bugs
- readability
- performance
- security
- maintainability
- code quality
- style / PEP8 where applicable
- concrete improvement suggestions

IMPORTANT:

1. Do not invent bugs.
2. Only report a bug when there is a real technical problem.
3. Distinguish between a genuine bug and a recommendation.
4. Consider the actual code before assigning each quality score.
5. Be conservative when uncertain.
6. Do not penalize simple code merely because it is simple.
7. Do not assume production requirements that are not present in the code.
8. The same code should receive essentially the same evaluation every time.

QUALITY SCORING:

- readability: 0 to 10
- performance: 0 to 10
- security: 0 to 10
- maintainability: 0 to 10

The application calculates the final score from these four values.
Therefore, do NOT use a percentage and do NOT return a score above 10.

Return ONLY valid JSON matching the provided schema.

Code:

{code}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": REVIEW_SCHEMA,

                # Reduce randomness.
                "temperature": 0,

                # Best-effort reproducibility.
                "seed": 42
            }
        )

        text = response.text.strip()

        print("\n========== GEMINI RESPONSE ==========")
        print(text)
        print("=====================================\n")

        if not text:
            raise Exception("Gemini returned an empty response.")

        data = json.loads(text)

        # -------------------------------------------------
        # Normalize the four AI quality dimensions
        # -------------------------------------------------

        quality = data.get("quality", {})

        readability = normalize_score(
            quality.get("readability", 0)
        )

        performance = normalize_score(
            quality.get("performance", 0)
        )

        security = normalize_score(
            quality.get("security", 0)
        )

        maintainability = normalize_score(
            quality.get("maintainability", 0)
        )

        data["quality"] = {
            "readability": readability,
            "performance": performance,
            "security": security,
            "maintainability": maintainability
        }

        # -------------------------------------------------
        # Application-controlled final score
        # -------------------------------------------------

        data["score"] = round(
            (
                readability
                + performance
                + security
                + maintainability
            ) / 4,
            2
        )

        return data

    except Exception as e:

        print("\n========== AI REVIEW FAILED ==========")
        print(type(e).__name__)
        print(str(e))
        print("======================================\n")

        return {
            "score": 0.0,

            "summary": "AI Review Failed",

            "strengths": [],

            "weaknesses": [],

            "suggestions": [],

            "quality": {
                "readability": 0.0,
                "performance": 0.0,
                "security": 0.0,
                "maintainability": 0.0
            },

            "bugs": [],

            "security": [],

            "performance": [],

            "pep8": [],

            "error": f"{type(e).__name__}: {e}"
        }