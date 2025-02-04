class Player:
    def __init__(self, name, role, age, nationality, stats, base_price):
        self.name = name
        self.role = role
        self.age = age
        self.nationality = nationality
        self.stats = stats  # Dictionary of relevant stats (batting avg, economy, strike rate, etc.)
        self.base_price = base_price

    def __str__(self):
        return f"{self.name} - {self.role}"
