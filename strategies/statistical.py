import random

class StatisticalBiddingStrategy:
    # A default player combination for a team of maximum 11 players.
    DEFAULT_ROSTER_REQUIREMENTS = {
    "batsman": 4,
    "bowler": 4,
    "allrounder": 2,
    "wicketkeeper": 1
}
    def __init__(self, total_budget):
        """
        total_budget: total capital available (in Cr)
        """
        self.total_budget = total_budget

        # Pull in the default roster requirements.
        roster_requirements = StatisticalBiddingStrategy.DEFAULT_ROSTER_REQUIREMENTS

        total_players = sum(roster_requirements.values())

        # Budget allocation per position: proportionally allocate the budget.
        self.position_budget = {pos: (total_budget * count / total_players) 
                                  for pos, count in roster_requirements.items()}
        # Start with no spending for any position.
        self.spent_budget = {pos: 0 for pos in roster_requirements}

    def predict_price(self, player):
        """
        A statistical pricing model. The idea is to start with the player's base price and add:
          - An adjustment based on performance relative to a baseline
          - A premium/discount based on the player's 'stars' rating.
        It assumes that the player object provides:
          player.base_price     (the player's baseline price)
          player.stats          (a dictionary with key metrics related to performance)
          player.role       (a string: 'batsman', 'bowler', 'allrounder', or 'wicketkeeper')
        """
        base = player.base_price
        stars = player.stats.get('stars', 5)  # use a default of 5 if not provided.
        pos = player.role.lower()
        adjustment = 0

        # For batsmen and wicketkeepers: emphasize batting metrics.
        if pos in ['batsman', 'wicketkeeper']:
            bat_avg = player.stats.get('bat_avg', 30)
            strike_rate = player.stats.get('strike_rate', 120)
            # Each 10 runs above a baseline average (30) gives a premium
            # and each 50 points in strike rate above 120 gives additional value.
            adjustment = ((bat_avg - 30) / 10) + ((strike_rate - 120) / 50)
        # For bowlers: emphasize lower bowling average and economy.
        elif pos == 'bowler':
            bowl_avg = player.stats.get('avg', 30)  # lower average is better.
            economy = player.stats.get('economy', 8)
            adjustment = ((30 - bowl_avg) / 10) + ((8 - economy) / 2)
        # For allrounders: combine batting and bowling metrics.
        elif pos == 'allrounder':
            bat_avg = player.stats.get('bat_avg', 25)
            strike_rate = player.stats.get('strike_rate', 120)
            bowl_avg = player.stats.get('bowl_avg', 30)
            economy = player.stats.get('economy', 8)
            batting_adj = ((bat_avg - 25) / 10) + ((strike_rate - 120) / 50)
            bowling_adj = ((30 - bowl_avg) / 10) + ((8 - economy) / 2)
            adjustment = (batting_adj + bowling_adj) / 2

        # Premium based on stars relative to a benchmark rating (5 out of 10).
        star_factor = (stars - 5) * 0.2  # 0.2 Cr premium per star above 5, discount if below.
        predicted = base + adjustment + star_factor
        # Ensure the predicted price is at least the base price.
        return max(predicted, base)

    def allowed_bid(self, player, current_bid):
        """
        Determine the maximum allowed bid for a player using:
          - The predicted price (statistical value)
          - The remaining allocated budget for the player's position.
        """
        pos = player.role.lower()
        predicted = self.predict_price(player)
        remaining = self.position_budget.get(pos, self.total_budget) - self.spent_budget.get(pos, 0)
        # Use the lower of predicted price and remaining allocated budget.
        allowed = min(predicted, remaining)
        return allowed

    def decide_bid(self, player, current_bid):
        """
        Given a player and the auction's current bid, decide how to bid.
        Strategy details:
         - If the current bid is less than 80% of the allowed bid, increase by 0.2 Cr.
         - Otherwise, sometimes add a 0.1 Cr increment if it does not exceed the allowed bid,
           or hold the bid.
        """
        allowed = self.allowed_bid(player, current_bid)
        if current_bid < 0.8 * allowed:
            new_bid = round(min(current_bid + 0.2, allowed), 2)
        elif current_bid < allowed and random.random() < 0.3:
            new_bid = round(min(current_bid + 0.1, allowed), 2)
        else:
            new_bid = current_bid
        return new_bid

    def update_spent(self, player, winning_bid):
        """
        After winning a bid for a player, update the spent budget for that player's position.
        """
        pos = player.role.lower()
        if pos in self.spent_budget:
            self.spent_budget[pos] += winning_bid
        else:
            self.spent_budget[pos] = winning_bid

    def evaluate_strategy(self, acquired_players):
        """
        Evaluates the bidding strategy by calculating:
         - The total predicted value of acquired players based on our statistical model.
         - The total spent budget and the spent per position.
         - The efficiency ratio (total predicted value divided by money spent).
         
        acquired_players: list of player objects that were acquired.
          Each player object should have an attribute 'winning_bid' which was paid to acquire them.
        """
        total_predicted_value = 0
        total_spent = 0
        position_spent = {}
        for player in acquired_players:
            predicted = self.predict_price(player)
            total_predicted_value += predicted
            # Expect player to have an attribute 'winning_bid'; fallback to base_price if missing.
            spent = getattr(player, 'winning_bid', player.base_price)
            total_spent += spent
            pos = player.role.lower()
            if pos not in position_spent:
                position_spent[pos] = 0
            position_spent[pos] += spent

        efficiency = total_predicted_value / total_spent if total_spent > 0 else 0.0
        evaluation = {
            "total_predicted_value": total_predicted_value,
            "total_spent": total_spent,
            "position_spent": position_spent,
            "efficiency": efficiency,
        }
        return evaluation
