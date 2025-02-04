import pandas as pd
from auctionengine.dealer import Dealer
from auctionengine.team import Team
from auctionengine.utils import load_players
from strategies.strategy import BiddingStrategy

def main():
    # Load data for all categories of players
    batsmen = load_players("dataset/batsmen.csv", role="Batsman")
    bowlers = load_players("dataset/bowlers.csv", role="Bowler")
    allrounders = load_players("dataset/allrounders.csv", role="All-rounder")
    wicket_keepers = load_players("dataset/wicketkeepers.csv", role="Wicket-Keeper")

    # Combine all into one list for auction
    all_players = batsmen + bowlers + allrounders + wicket_keepers

    # Define the participant teams
    team_a = Team(name="Team A", budget=80.0, max_players=18)
    team_b = Team(name="Team B", budget=80.0, max_players=18)
    team_c = Team(name="Team C", budget=80.0, max_players=18)
    teams = [team_a, team_b, team_c]

    # Create dealers and bidding strategies
    bidding_strategies = {
        "Team A": BiddingStrategy(),
        "Team B": BiddingStrategy(),
        "Team C": BiddingStrategy(),
    }
    dealer = Dealer(players=all_players, teams=teams, strategies=bidding_strategies)

    # Run the auction
    dealer.start_auction()

    # Post-auction analytics
    for t in teams:
        t.print_team_summary()

if __name__ == "__main__":
    main()
