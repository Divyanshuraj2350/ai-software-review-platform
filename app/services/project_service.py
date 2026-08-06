def build_project_summary(reviews):
    """
    Generate overall project statistics from
    all reviewed files.
    """

    if not reviews:
        return {
            "total_files": 0,
            "average_score": 0,
            "total_bugs": 0,
            "total_security": 0,
            "total_performance": 0,
            "total_pep8": 0
        }

    total_score = 0
    total_bugs = 0
    total_security = 0
    total_performance = 0
    total_pep8 = 0

    for item in reviews:

        review = item["review"]

        total_score += review.get("score", 0)

        total_bugs += len(review.get("bugs", []))

        total_security += len(review.get("security", []))

        total_performance += len(review.get("performance", []))

        total_pep8 += len(review.get("pep8", []))

    return {

        "total_files": len(reviews),

        "average_score": round(
            total_score / len(reviews),
            2
        ),

        "total_bugs": total_bugs,

        "total_security": total_security,

        "total_performance": total_performance,

        "total_pep8": total_pep8

    }