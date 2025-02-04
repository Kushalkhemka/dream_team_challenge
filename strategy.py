import random
import numpy as np
from sklearn.linear_model import LinearRegression

class BiddingStrategy:
    # For demonstration, we’ll load or create a trained model in memory.
    # Extend this with advanced ML or RL as needed.

    def __init__(self):
        # Placeholder for a trained model
        # For illustration, we create a simple linear model with fake coefficients.
        self.model = LinearRegression()
        self.model.coef_ = np.array([0.1, 0.05, 0.2])  # Fake coefficients for demonstration
        self.model.intercept_ = 1.0  # Fake intercept

    def estimate_value(self, player):
        # Placeholder: we assume "stats" has simplified keys: [bat_avg, strike_rate, economy]
        # This is purely illustrative. You should tailor it to your dataset’s actual keys.
        bat_avg = player.stats.get('bat_avg', 20)
        strike_rate = player.stats.get('strike_rate', 120)
        economy = player.stats.get('economy', 8)

        # Convert to a single data point array
        X = np.array([[bat_avg, strike_rate, economy]])
        predicted_value = self.model.predict(X)[0]
        return max(predicted_value, player.base_price)

    def decide_bid(self, player, current_bid):
        # Estimate the ideal value
        estimated_value = self.estimate_value(player)

        # Simple rule: if current_bid < 80% of estimated_value, increase bid by 0.2 Cr
        if current_bid < (0.8 * estimated_value):
            return round(current_bid + 0.2, 2)
        else:
            # Randomly add a small increment or pass
            if random.random() < 0.3:
                return round(current_bid + 0.1, 2)
            else:
                return current_bid
