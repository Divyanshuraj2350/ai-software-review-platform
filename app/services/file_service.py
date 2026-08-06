from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(exist_ok=True)

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB
MAX_FILES = 10

# ==========================
# Supported Languages
# ==========================

SUPPORTED_LANGUAGES = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".html": "HTML",
    ".css": "CSS",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".php": "PHP",
    ".rb": "Ruby",
    ".rs": "Rust",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".sql": "SQL",
    ".sh": "Shell"
}

# ZIP is handled separately
ALLOWED_EXTENSIONS = set(SUPPORTED_LANGUAGES.keys()) | {".zip"}


def validate_upload(upload_file) -> str:
    """
    Validate uploaded file.
    """

    filename = Path(upload_file.filename or "").name

    if not filename or filename in {".", ".."}:
        raise ValueError("Invalid filename")

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "Unsupported file type.\n\n"
            "Supported:\n"
            + ", ".join(sorted(ALLOWED_EXTENSIONS))
        )

    upload_file.file.seek(0, 2)
    size = upload_file.file.tell()
    upload_file.file.seek(0)

    if size == 0:
        raise ValueError("Empty file is not allowed")

    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"File exceeds the {MAX_FILE_SIZE // (1024 * 1024)} MB size limit"
        )

    return filename


def save_file(upload_file):
    """
    Save uploaded file.
    """

    filename = validate_upload(upload_file)

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


def read_file(file_path):
    """
    Read source code file.
    """

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def get_language(file_path):
    """
    Return programming language based on extension.
    """

    extension = Path(file_path).suffix.lower()

    return SUPPORTED_LANGUAGES.get(extension, "Unknown")


def delete_file(file_path):
    """
    Delete uploaded file.
    """

    Path(file_path).unlink(missing_ok=True)