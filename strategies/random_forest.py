import numpy as np
from sklearn.ensemble import RandomForestRegressor
from auctionengine.player import Player

class RandomForestBiddingStrategy:
    def __init__(self, model=None, n_estimators=100):
        self.model = model or self._train_default_model(n_estimators)

    def _train_default_model(self, n_estimators):
        X_train = np.random.rand(500, 3)
        y_train = np.random.rand(500) * 10  

        model = RandomForestRegressor(n_estimators=n_estimators)
        model.fit(X_train, y_train)
        return model

    def estimate_value(self, player: Player):
        features = np.array([
            player.stats.get('batting_avg', 20) / 50,
            player.stats.get('strike_rate', 120) / 200,
            player.stats.get('economy', 8) / 15
        ]).reshape(1, -1)

        predicted_value = self.model.predict(features)[0]
        return max(predicted_value, player.base_price)

    def decide_bid(self, player: Player, current_bid: float):
        estimated_value = self.estimate_value(player)
        if current_bid < (0.85 * estimated_value):
            return round(current_bid + 0.15, 2)
        elif current_bid < estimated_value:
            return round(current_bid + 0.05, 2)
        return current_bid
