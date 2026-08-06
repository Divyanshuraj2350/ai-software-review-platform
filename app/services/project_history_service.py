import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

PROJECT_FILE = Path("app/data/projects.json")


def get_projects():
    """
    Return all saved projects.
    """

    if not PROJECT_FILE.exists():
        PROJECT_FILE.parent.mkdir(parents=True, exist_ok=True)
        PROJECT_FILE.write_text("[]")

    try:
        with open(PROJECT_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_project(project_data):
    """
    Save one complete project.
    """

    projects = get_projects()

    project = {
        "project_id": str(uuid4()),

        "project_name": project_data["project_name"],

        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M"),

        "summary": project_data["summary"],

        "project_ai": project_data["project_ai"],

        "project_risk": project_data["project_risk"],

        "reviews": project_data["reviews"]
    }

    projects.insert(0, project)

    with open(PROJECT_FILE, "w", encoding="utf-8") as file:
        json.dump(projects, file, indent=4)

    return project


def get_project(project_id):
    """
    Return one project by ID.
    """

    for project in get_projects():

        if project["project_id"] == project_id:
            return project

    return None


def delete_project(project_id):
    """
    Delete one project.
    """

    projects = [
        project
        for project in get_projects()
        if project["project_id"] != project_id
    ]

    with open(PROJECT_FILE, "w", encoding="utf-8") as file:
        json.dump(projects, file, indent=4)


def get_dashboard():
    """
    Dashboard statistics.
    """

    projects = get_projects()

    if not projects:

        return {
            "total_projects": 0,
            "average_score": 0,
            "best_score": 0,
            "files_reviewed": 0
        }

    total_score = 0
    total_files = 0
    best_score = 0

    for project in projects:

        summary = project["summary"]

        total_score += summary["average_score"]

        total_files += summary["total_files"]

        best_score = max(best_score, summary["average_score"])

    return {

        "total_projects": len(projects),

        "average_score": round(
            total_score / len(projects),
            2
        ),

        "best_score": best_score,

        "files_reviewed": total_files

    }