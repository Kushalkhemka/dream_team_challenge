import pandas as pd
from auctionengine.dealer import Dealer
from auctionengine.team import Team
from auctionengine.utils import load_players
from strategies.base import BiddingStrategy
from strategies.statistical import StatisticalBiddingStrategy

def main():
    # Load data for all categories of players
    batsmen = load_players("dataset/batsmen.csv", role="batsman")
    bowlers = load_players("dataset/bowlers.csv", role="bowler")
    allrounders = load_players("dataset/allrounders.csv", role="allrounder")
    wicket_keepers = load_players("dataset/wicketkeepers.csv", role="wicketkeeper")

    # Combine all into one list for auction
    all_players = batsmen + bowlers + allrounders + wicket_keepers

    # Set the budget for each team
    team_budgets = {
        "Team A": 25.0,
        "Team B": 25.0,
        "Team C": 25.0,
        "Team D": 25.0
    }

    # Set the max players
    max_players = 11

    # Define the participant teams
    team_a = Team(name="Team A", budget=team_budgets["Team A"], max_players=max_players)
    team_b = Team(name="Team B", budget=team_budgets["Team B"], max_players=max_players)
    team_c = Team(name="Team C", budget=team_budgets["Team C"], max_players=max_players)
    team_d = Team(name="Team D", budget=team_budgets["Team D"], max_players=max_players)
    teams = [team_a, team_b, team_c, team_d]

    # Create dealers and bidding strategies
    bidding_strategies = {
        "Team A": BiddingStrategy(),
        "Team B": BiddingStrategy(),
        "Team C": StatisticalBiddingStrategy(total_budget=team_c.budget),
        "Team D": StatisticalBiddingStrategy(total_budget=team_d.budget)
    }
    dealer = Dealer(players=all_players, teams=teams, strategies=bidding_strategies)

    # Run the auction
    dealer.start_auction()

    # Post-auction analytics
    for t in teams:
        t.print_team_summary()

if __name__ == "__main__":
    main()
