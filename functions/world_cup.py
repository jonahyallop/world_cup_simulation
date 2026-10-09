from itertools import combinations
import numpy as np

from match import simulate_score

# TODO: MOVE TO CONFIG FILE
GROUPS = {
    "A": ["Mexico","South Africa","South Korea","Czech Republic"],
    "B": ["Canada","Bosnia and Herzegovina","Qatar","Switzerland"],
    "C": ["Brazil","Morocco","Haiti","Scotland"],
    "D": ["United States","Paraguay","Australia","Turkey"],
    "E": ["Germany","Curaçao","Ivory Coast","Ecuador"],
    "F": ["Netherlands","Japan","Sweden","Tunisia"],
    "G": ["Belgium","Egypt","Iran","New Zealand"],
    "H": ["Spain","Cape Verde","Saudi Arabia","Uruguay"],
    "I": ["France","Senegal","Iraq","Norway"],
    "J": ["Argentina","Algeria","Austria","Jordan"],
    "K": ["Portugal","DR Congo","Uzbekistan","Colombia"],
    "L": ["England","Croatia","Ghana","Panama"]
}

def simulate_group(teams, ratings):

    table = {}

    for team in teams:

        table[team] = {
            "pts": 0,
            "gf": 0,
            "ga": 0,
            "gd": 0
        }

    for home, away in combinations(teams, 2):

        gh, ga = simulate_score(
            home,
            away,
            ratings
        )

        table[home]["gf"] += gh
        table[home]["ga"] += ga

        table[away]["gf"] += ga
        table[away]["ga"] += gh

        if gh > ga:

            table[home]["pts"] += 3

        elif ga > gh:

            table[away]["pts"] += 3

        else:

            table[home]["pts"] += 1
            table[away]["pts"] += 1

    for team in teams:

        table[team]["gd"] = (
            table[team]["gf"]
            - table[team]["ga"]
        )

    ranking = sorted(
        teams,
        key=lambda t: (
            table[t]["pts"],
            table[t]["gd"],
            table[t]["gf"]
        ),
        reverse=True
    )

    return ranking, table


def group_stage(ratings):

    winners = []
    runners_up = []
    third_place = []
    tables = []

    for group in GROUPS.values():

        ranking, table = simulate_group(
            group,
            ratings
        )

        tables.append(table)

        winners.append(ranking[0])
        runners_up.append(ranking[1])

        third_place.append(
            (
                ranking[2],
                table[ranking[2]]
            )
        )

    third_place.sort(
        key=lambda x: (
            x[1]["pts"],
            x[1]["gd"],
            x[1]["gf"]
        ),
        reverse=True
    )

    best_thirds = [
        x[0]
        for x in third_place[:8]
    ]

    return winners, runners_up, best_thirds, tables


def knockout_match(a, b, ratings):

    while True:

        ga, gb = simulate_score(
            a,
            b,
            ratings
        )

        if ga > gb:
            return a

        if gb > ga:
            return b
        

def simulate_group_stage(ratings):

    winners, runners_up, thirds, tables = (
        group_stage(ratings)
    )

    return tables


def simulate_world_cup(ratings):

    winners, runners_up, thirds, tables = (
        group_stage(ratings)
    )

    teams = (
        winners
        + runners_up
        + thirds
    )

    np.random.shuffle(teams)

    round_32 = list(
        zip(
            teams[::2],
            teams[1::2]
        )
    )

    current = [
        knockout_match(a, b, ratings)
        for a, b in round_32
    ]

    while len(current) > 1:

        matches = list(
            zip(
                current[::2],
                current[1::2]
            )
        )

        current = [
            knockout_match(a, b, ratings)
            for a, b in matches
        ]

    return current[0]
