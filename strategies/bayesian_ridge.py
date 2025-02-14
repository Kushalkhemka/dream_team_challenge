from sklearn.linear_model import BayesianRidge
import numpy as np
from auctionengine.player import Player

class BayesianRidgeBiddingStrategy:
    def __init__(self, model=None, total_budget=100):
        self.total_budget = total_budget
        self.spent_budget = 0
        self.model = model or self._train_default_model()

    def _train_default_model(self):
        # Simulating realistic auction data for better training
        X_train = np.random.rand(1000, 5)  
        y_train = (X_train[:, 0] * 8) + (X_train[:, 1] * 5) + (X_train[:, 2] * 3) + (np.random.rand(1000) * 2)
        
        model = BayesianRidge(alpha_1=1e-6, lambda_1=1e-6)  
        model.fit(X_train, y_train)
        return model

    def extract_features(self, player: Player):
        """Extracts enhanced features for valuation."""
        return np.array([
            player.stats.get('batting_avg', 20) / 50,  
            player.stats.get('strike_rate', 120) / 200,  
            player.stats.get('economy', 8) / 15,  
            player.stats.get('stars', 5) / 10,  # Star rating scaled
            np.clip(player.base_price / 5, 0, 1)  # Normalize base price
        ]).reshape(1, -1)

    def estimate_value(self, player: Player):
        features = self.extract_features(player)
        predicted_value = self.model.predict(features)[0]
        
        # Introduce a market adjustment factor based on demand
        market_factor = np.random.uniform(0.9, 1.1)
        return max(predicted_value * market_factor, player.base_price)

    def decide_bid(self, player: Player, current_bid: float):
        estimated_value = self.estimate_value(player)
        remaining_budget = self.total_budget - self.spent_budget
        max_allowed = min(estimated_value, remaining_budget)

        # Adaptive bidding: More aggressive early, conservative later
        if current_bid < 0.7 * max_allowed:
            new_bid = round(current_bid + np.random.uniform(0.2, 0.5), 2)
        elif current_bid < max_allowed:
            new_bid = round(current_bid + np.random.uniform(0.05, 0.2), 2)
        else:
            new_bid = current_bid

        return min(new_bid, max_allowed)

    def update_spent(self, winning_bid):
        self.spent_budget += winning_bid
