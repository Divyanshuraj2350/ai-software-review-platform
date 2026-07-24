import json
from pathlib import Path
from datetime import datetime

HISTORY_FILE = Path("app/data/history.json")


def save_review(filename, review):

    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text("[]")

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    history.insert(0, {
        "filename": filename,
        "score": review["score"],
        "summary": review["summary"],
        "date": datetime.now().strftime("%d-%m-%Y %H:%M")
    })

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)


def get_history():

    if not HISTORY_FILE.exists():
        return []

    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def delete_review(index: int):

    history = get_history()

    if 0 <= index < len(history):
        history.pop(index)

        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)