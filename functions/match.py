import numpy as np


def elo_to_goal_rates(team_a, team_b, ratings):

    elo_diff = ratings[team_a] - ratings[team_b]

    lambda_a = 1.35 + 0.0025 * elo_diff
    lambda_b = 1.35 - 0.0025 * elo_diff

    lambda_a = max(0.2, lambda_a)
    lambda_b = max(0.2, lambda_b)

    return lambda_a, lambda_b


def simulate_score(team_a, team_b, ratings):

    lam_a, lam_b = elo_to_goal_rates(
        team_a,
        team_b,
        ratings
    )

    goals_a = np.random.poisson(lam_a)
    goals_b = np.random.poisson(lam_b)

    return goals_a, goals_b