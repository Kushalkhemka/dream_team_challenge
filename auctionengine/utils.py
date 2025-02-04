import pandas as pd
from auctionengine.player import Player

def load_players(filepath, role):
    df = pd.read_csv(filepath)
    players = []

    # Adjust column names and data extraction logic based on your CSV structure
    # Example for a batsman CSV with columns: Player, Stars, Nationality, Age, ...
    for _, row in df.iterrows():
        # Gather relevant stats into a dictionary
        stats_dict = {
            "bat_avg": float(row.get("Average", 0)),
            "strike_rate": float(row.get("Strike Rates", 0)),
            "economy": float(row.get("Economy", 0)),  # for bowlers/allrounders
            # You can add more fields here
        }
        player_obj = Player(
            name=row.get("Player"),
            role=role,
            age=row.get("Age"),
            nationality=row.get("Nationality"),
            stats=stats_dict,
            base_price=float(row.get("Base Price (Cr)", 0.5))
        )
        players.append(player_obj)

    return players
