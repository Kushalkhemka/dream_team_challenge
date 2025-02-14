import numpy as np
import xgboost as xgb
from auctionengine.player import Player

class XGBoostBiddingStrategy:
    def __init__(self, model=None):
        """
        Initialize the XGBoost bidding strategy with a pre-trained model.
        If no model is provided, a default one is initialized.
        """
        self.model = model or self._train_default_model()

    def _train_default_model(self):
        """
        Train a default XGBoost model using dummy data.
        In a real scenario, this should be replaced with actual training data.
        """
        # Dummy training data
        X_train = np.random.rand(100, 3)  # 100 samples, 3 features
        y_train = np.random.rand(100) * 10  # Random target values

        model = xgb.XGBRegressor(objective='reg:squarederror')
        model.fit(X_train, y_train)
        return model

    def estimate_value(self, player: Player):
        """
        Estimate the value of a player using the XGBoost model.
        """
        features = np.array([
            player.stats.get('batting_avg', 20),
            player.stats.get('strike_rate', 120),
            player.stats.get('economy', 8)
        ]).reshape(1, -1)
        predicted_value = self.model.predict(features)[0]
        return max(predicted_value, player.base_price)

    def decide_bid(self, player: Player, current_bid: float):
        """
        Decide the bid amount based on the estimated player value.
        """
        estimated_value = self.estimate_value(player)
        if current_bid < (0.8 * estimated_value):
            return round(current_bid + 0.2, 2)
        elif current_bid < estimated_value:
            return round(current_bid + 0.1, 2)
        else:
            return current_bid 