import pandas as pd

INITIAL_RATING = 1500
K = 30


def expected_score(ra, rb):
    return 1 / (1 + 10 ** ((rb - ra) / 400))


def build_elo_ratings(results_file):

    matches = pd.read_csv(results_file)

    matches["date"] = pd.to_datetime(matches["date"])
    matches = matches.sort_values("date")

    ratings = {}

    def get_rating(team):
        return ratings.get(team, INITIAL_RATING)

    for _, row in matches.iterrows():

        home = row["home_team"]
        away = row["away_team"]

        ra = get_rating(home)
        rb = get_rating(away)

        ea = expected_score(ra, rb)
        eb = 1 - ea

        if row["home_score"] > row["away_score"]:
            sa, sb = 1, 0

        elif row["home_score"] < row["away_score"]:
            sa, sb = 0, 1

        else:
            sa, sb = 0.5, 0.5

        ratings[home] = ra + K * (sa - ea)
        ratings[away] = rb + K * (sb - eb)

    return ratings
