from app.services.history_service import get_review


def compare_reviews(index1: int, index2: int):

    review1 = get_review(index1)
    review2 = get_review(index2)

    if review1 is None or review2 is None:
        return None

    score1 = review1["review"]["score"]
    score2 = review2["review"]["score"]

    if score1 > score2:
        winner = review1["filename"]
    elif score2 > score1:
        winner = review2["filename"]
    else:
        winner = "Tie"

    return {
        "review1": review1,
        "review2": review2,
        "winner": winner,
        "difference": abs(score1 - score2)
    }