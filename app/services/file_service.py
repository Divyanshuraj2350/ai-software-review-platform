from pathlib import Path
import shutil

UPLOAD_DIR = Path("uploads")

UPLOAD_DIR.mkdir(exist_ok=True)


def save_file(upload_file):
    """
    Save uploaded file to uploads folder.
    """

    file_path = UPLOAD_DIR / upload_file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return file_path


def read_file(file_path):
    """
    Read uploaded source code.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def delete_file(file_path):
    """
    Delete uploaded file.
    """

    Path(file_path).unlink(missing_ok=True)