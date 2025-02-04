import random

class Dealer:
    def __init__(self, players, teams, strategies):
        """
        :param players: List of Player objects
        :param teams: List of Team objects
        :param strategies: Dict {team_name: BiddingStrategy object}
        """
        self.players = players
        self.teams = teams
        self.strategies = strategies

    def start_auction(self):
        # Shuffle or otherwise sort players if desired
        random.shuffle(self.players)

        for player in self.players:
            print(f"\nAuctioning {player.name} ({player.role}) - Base Price: {player.base_price} Cr")
            self.conduct_bidding(player)

    def conduct_bidding(self, player):
        current_bid = player.base_price
        highest_bidder = None

        # Simple iteration of bidding
        bidding_active = True
        while bidding_active:
            bidding_active = False
            for team in self.teams:
                if team.can_bid(current_bid) and len(team.players) < team.max_players:
                    # Use the team’s bidding strategy to decide next bid
                    next_bid = self.strategies[team.name].decide_bid(player, current_bid)
                    if next_bid > current_bid and team.budget >= next_bid:
                        current_bid = next_bid
                        highest_bidder = team
                        bidding_active = True

        if highest_bidder:
            highest_bidder.add_player(player, current_bid)
            print(f"{highest_bidder.name} wins {player.name} for {current_bid} Cr")
        else:
            print(f"No bids placed for {player.name}. Player remains unsold.")
