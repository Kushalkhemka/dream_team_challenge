"""
This module implements the main auction functionality for a cricket team auction system.
It loads player data, sets up teams with budgets, and runs the auction process using
different bidding strategies for each team.

The auction system supports different types of players (batsmen, bowlers, all-rounders,
and wicket-keepers) and allows teams to bid based on either basic or statistical strategies.
"""

import pandas as pd
from auctionengine.dealer import Dealer
from auctionengine.team import Team
from auctionengine.utils import load_players
from strategies.base import BiddingStrategy
from strategies.statistical import StatisticalBiddingStrategy
from strategies.mlp_strategy import MLPBiddingStrategy
from strategies.xgboost_strategy import XGBoostBiddingStrategy
from strategies.bayesian_ridge import BayesianRidgeBiddingStrategy
from strategies.random_forest import RandomForestBiddingStrategy

def main():
    """
    Main function that orchestrates the auction process.
    Loads player data, initializes teams, and runs the auction.
    """
    # Load data for all categories of players from CSV files
    batsmen = load_players("dataset/batsmen.csv", role="batsman")
    bowlers = load_players("dataset/bowlers.csv", role="bowler")
    allrounders = load_players("dataset/allrounders.csv", role="allrounder")
    wicket_keepers = load_players("dataset/wicketkeepers.csv", role="wicketkeeper")

    # Combine all player categories into one list for auction
    all_players = batsmen + bowlers + allrounders + wicket_keepers

    # Initialize team budgets (in millions)
    team_budgets = {
        "Team A": 40.0,
        "Team B": 40.0,
        "Team C": 40.0,
        "Team D": 40.0
    }

    # Set maximum players allowed per team
    max_players = 11

    # Create team objects with their respective budgets and player limits
    team_a = Team(name="Team A", budget=team_budgets["Team A"], max_players=max_players)
    team_b = Team(name="Team B", budget=team_budgets["Team B"], max_players=max_players)
    team_c = Team(name="Team C", budget=team_budgets["Team C"], max_players=max_players)
    team_d = Team(name="Team D", budget=team_budgets["Team D"], max_players=max_players)
    teams = [team_a, team_b, team_c, team_d]

    # Assign bidding strategies to teams
    bidding_strategies = {
        "Team A": RandomForestBiddingStrategy(),
        "Team B": XGBoostBiddingStrategy(),
        "Team C": StatisticalBiddingStrategy(total_budget=team_c.budget),
        "Team D": BayesianRidgeBiddingStrategy(total_budget=team_d.budget)
    }
    
    # Initialize dealer with players, teams and their strategies
    dealer = Dealer(players=all_players, teams=teams, strategies=bidding_strategies)

    # Execute the auction process
    dealer.start_auction()

    # Display final team compositions and statistics
    for t in teams:
        t.print_team_summary()
        total_stars = sum(player.stats.get('stars', 0) for player in t.players)
        print(f"Total Stars Collected by {t.name}: {total_stars}")

    # Determine the winning team based on total stars
    winning_team = max(teams, key=lambda team: sum(player.stats.get('stars', 0) for player in team.players))
    print(f"\nWinning Team: {winning_team.name} with {sum(player.stats.get('stars', 0) for player in winning_team.players)} stars")

if __name__ == "__main__":
    main()
