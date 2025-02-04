"""
Player class represents a cricket player in the auction system.
"""

class Player:
    def __init__(self, name, role, age, nationality, stats, base_price):
        """
        Initialize a new Player instance.

        Args:
            name (str): Full name of the player
            role (str): Player's role (e.g., batsman, bowler, all-rounder)
            age (int): Player's age
            nationality (str): Player's country of origin
            stats (dict): Dictionary containing player's performance statistics
            base_price (float): Starting bid price for the player
        """
        self.name = name
        self.role = role
        self.age = age
        self.nationality = nationality
        self.stats = stats  # Dictionary of relevant stats (batting avg, economy, strike rate, etc.)
        self.base_price = base_price

    def __str__(self):
        """
        Returns a string representation of the Player.

        Returns:
            str: Player's name and role in format 'name - role'
        """
        return f"{self.name} - {self.role}"
    