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
            "type": "number"
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
                    "type": "number"
                },
                "performance": {
                    "type": "number"
                },
                "security": {
                    "type": "number"
                },
                "maintainability": {
                    "type": "number"
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


def get_ai_review(code: str, language: str):

    prompt = f"""
You are a Senior {language} Software Engineer with 15+ years of experience.

Review the following {language} code professionally.

Analyze:

- overall code quality
- readability
- performance
- security
- maintainability
- bugs
- security vulnerabilities
- performance problems
- PEP8/style problems
- concrete improvement suggestions

Return the review using the requested JSON structure.

Code:

{code}
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": REVIEW_SCHEMA
            }
        )

        text = response.text.strip()

        print("\n========== GEMINI RESPONSE ==========")
        print(text)
        print("=====================================\n")

        if not text:
            raise Exception("Gemini returned an empty response.")

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