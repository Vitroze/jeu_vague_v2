from database.function import get_scores

def sorted_score():
    scores = get_scores()
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    return scores

def print_score(scores):
    print("------ Score ------")

    for index, object in enumerate(scores):
        print(f"    {index}. {object.get("player_name")} - {object.get("score")}")

def show_score():
    scores = sorted_score()
    print_score(scores)