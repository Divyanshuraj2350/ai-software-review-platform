import zipfile
import shutil
from pathlib import Path
from uuid import uuid4

from app.services.file_service import SUPPORTED_LANGUAGES

TEMP_DIR = Path("temp_projects")
TEMP_DIR.mkdir(exist_ok=True)

# -----------------------------
# Folders to Ignore
# -----------------------------

IGNORE_FOLDERS = {
    ".git",
    ".github",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    "target",
    "bin",
    "obj",
    ".idea",
    ".vscode",
    "coverage",
    ".pytest_cache"
}

# -----------------------------
# Files to Ignore
# -----------------------------

IGNORE_FILES = {
    "README.md",
    "LICENSE",
    ".gitignore",
    "package-lock.json",
    "yarn.lock",
    "poetry.lock",
    "Pipfile.lock"
}

# -----------------------------
# Maximum AI Reviews
# -----------------------------

MAX_REVIEW_FILES = 20

# -----------------------------
# Priority Files
# -----------------------------

PRIORITY_FILES = {
    "main.py",
    "app.py",
    "server.py",
    "run.py",
    "manage.py",
    "index.js",
    "app.js",
    "main.js",
    "main.java",
    "Main.java",
    "Program.cs",
    "main.go",
    "index.html"
}


def extract_zip(zip_path: Path):
    """
    Extract ZIP into a temporary folder.
    """

    project_folder = TEMP_DIR / str(uuid4())

    project_folder.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(project_folder)

    return project_folder


def get_source_files(project_folder: Path):
    """
    Return important source files and project statistics.
    """

    source_files = []
    skipped_files = 0

    for file in project_folder.rglob("*"):

        if not file.is_file():
            continue

        # Ignore unwanted folders
        if any(part in IGNORE_FOLDERS for part in file.parts):
            skipped_files += 1
            continue

        # Ignore unwanted filenames
        if file.name in IGNORE_FILES:
            skipped_files += 1
            continue

        # Keep only supported languages
        if file.suffix.lower() not in SUPPORTED_LANGUAGES:
            skipped_files += 1
            continue

        source_files.append(file)

    # -----------------------------
    # Prioritize important files
    # -----------------------------

    source_files.sort(
        key=lambda f: (
            f.name not in PRIORITY_FILES,
            len(f.parts),
            f.name.lower()
        )
    )

    reviewed_files = source_files[:MAX_REVIEW_FILES]

    skipped_files += max(
        0,
        len(source_files) - MAX_REVIEW_FILES
    )

    return {
        "files": reviewed_files,
        "reviewed": len(reviewed_files),
        "skipped": skipped_files,
        "total": len(source_files)
    }


def delete_project(project_folder: Path):
    """
    Delete extracted project.
    """

    if project_folder.exists():
        shutil.rmtree(project_folder)