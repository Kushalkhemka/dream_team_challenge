class Team:
    def __init__(self, name, budget, max_players):
        self.name = name
        self.budget = budget
        self.max_players = max_players
        self.players = []

    def can_bid(self, amount):
        return self.budget >= amount

    def add_player(self, player, bid_amount):
        if self.can_bid(bid_amount) and len(self.players) < self.max_players:
            self.players.append(player)
            self.budget -= bid_amount

    def print_team_summary(self):
        print(f"\n--- {self.name} Summary ---")
        print(f"Remaining Budget: {self.budget} Cr")
        print(f"Players in Squad ({len(self.players)}):")
        for p in self.players:
            print(f" • {p.name} ({p.role}) for base {p.base_price} Cr")
        print("---------------------------\n")
