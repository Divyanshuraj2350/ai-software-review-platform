import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4


PROJECT_FILE = Path("app/data/projects.json")


def _normalize_score(score):
    """
    Convert legacy percentage-style scores to the current 0-10 scale.

    Current valid scores:
        0 <= score <= 10

    Legacy scores:
        0 < score <= 100
        Example: 70 -> 7.0
    """

    if not isinstance(score, (int, float)):
        return 0

    if score > 10:
        score = score / 10

    return round(max(0, min(score, 10)), 2)


def _normalize_project(project):
    """
    Normalize legacy score values inside one project.

    This updates:
    - summary.average_score
    - project_ai.health_score
    - reviews[].review.score
    - reviews[].review.quality.*
    """

    changed = False

    # -------------------------
    # Summary score
    # -------------------------

    if "summary" in project:

        old_score = project["summary"].get("average_score", 0)
        new_score = _normalize_score(old_score)

        if old_score != new_score:
            project["summary"]["average_score"] = new_score
            changed = True

    # -------------------------
    # Project AI health score
    # -------------------------

    if "project_ai" in project:

        old_score = project["project_ai"].get("health_score", 0)
        new_score = _normalize_score(old_score)

        if old_score != new_score:
            project["project_ai"]["health_score"] = new_score
            changed = True

    # -------------------------
    # Individual reviews
    # -------------------------

    for review_entry in project.get("reviews", []):

        review = review_entry.get("review", {})

        # Main review score
        old_score = review.get("score", 0)
        new_score = _normalize_score(old_score)

        if old_score != new_score:
            review["score"] = new_score
            changed = True

        # Quality dimensions
        quality = review.get("quality", {})

        for dimension in [
            "readability",
            "performance",
            "security",
            "maintainability"
        ]:

            if dimension in quality:

                old_value = quality[dimension]
                new_value = _normalize_score(old_value)

                if old_value != new_value:
                    quality[dimension] = new_value
                    changed = True

    return changed


def _normalize_projects(projects):
    """
    Normalize all projects and return whether anything changed.
    """

    changed = False

    for project in projects:

        if _normalize_project(project):
            changed = True

    return changed


def get_projects():
    """
    Return all saved projects.

    Also repairs legacy percentage-style scores so that
    historical data follows the current 0-10 scoring system.
    """

    if not PROJECT_FILE.exists():

        PROJECT_FILE.parent.mkdir(parents=True, exist_ok=True)
        PROJECT_FILE.write_text("[]", encoding="utf-8")

    try:

        with open(PROJECT_FILE, "r", encoding="utf-8") as file:
            projects = json.load(file)

    except json.JSONDecodeError:

        return []

    # Repair old scores if necessary.
    if _normalize_projects(projects):

        with open(PROJECT_FILE, "w", encoding="utf-8") as file:

            json.dump(
                projects,
                file,
                indent=4
            )

    return projects


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

    # Make sure newly saved projects also use 0-10 scores.
    _normalize_project(project)

    projects.insert(0, project)

    with open(PROJECT_FILE, "w", encoding="utf-8") as file:

        json.dump(
            projects,
            file,
            indent=4
        )

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

        json.dump(
            projects,
            file,
            indent=4
        )


def get_dashboard():
    """
    Return dashboard statistics using the normalized 0-10 scores.
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

        summary = project.get("summary", {})

        score = _normalize_score(
            summary.get("average_score", 0)
        )

        total_score += score

        total_files += summary.get(
            "total_files",
            0
        )

        best_score = max(
            best_score,
            score
        )

    return {

        "total_projects": len(projects),

        "average_score": round(
            total_score / len(projects),
            2
        ),

        "best_score": round(
            best_score,
            2
        ),

        "files_reviewed": total_files
    }