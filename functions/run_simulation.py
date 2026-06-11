from collections import Counter

from elo import build_elo_ratings
from world_cup import simulate_world_cup


ratings = build_elo_ratings(
    "data/results.csv"
)

N_SIMS = 10000

champions = Counter()

for i in range(N_SIMS):


    winner = simulate_world_cup(
        ratings
    )

    champions[winner] += 1

print("\nChampion probabilities:\n")

for team, wins in champions.most_common():

    print(
        f"{team:<20}"
        f"{100*wins/N_SIMS:.2f}%"
    )