from collections import Counter
from tqdm import tqdm

from elo import build_elo_ratings
from world_cup import simulate_world_cup, simulate_group_stage

ratings = build_elo_ratings(
    "data/results.csv"
)

GROUP_STANDINGS = simulate_group_stage(ratings)

N_SIMS = 10000

champions = Counter()

for i in tqdm(range(N_SIMS)):


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