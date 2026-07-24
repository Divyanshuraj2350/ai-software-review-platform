from app.services.llm_service import get_ai_review


def review_code(code: str):
    return get_ai_review(code)