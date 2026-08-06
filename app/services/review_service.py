from pathlib import Path

from app.services.file_service import get_language
from app.services.llm_service import get_ai_review


def review_code(code: str, filename: str):
    """
    Review source code using AI.

    The programming language is detected automatically
    from the file extension.
    """

    language = get_language(Path(filename))

    return get_ai_review(
        code=code,
        language=language
    )