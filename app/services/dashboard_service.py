from app.services.project_history_service import get_dashboard


def get_dashboard_data():
    """
    Return dashboard statistics from the project history.
    """

    dashboard = get_dashboard()

    return {
        "total_projects": dashboard["total_projects"],
        "average_score": dashboard["average_score"],
        "best_score": dashboard["best_score"],
        "files_reviewed": dashboard["files_reviewed"]
    }