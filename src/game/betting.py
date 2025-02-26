class BettingSystem:
    def __init__(self, balance):
        """Initialisiert das Wettsystem mit einem Startguthaben."""
        self.balance = balance
        self.current_bet = 0

    def place_bet(self, amount):
        """Setzt einen Einsatz."""
        if amount > 0 and amount <= self.balance:
            self.current_bet = amount
            self.balance -= amount
            return True
        return False

    def win_bet(self):
        """Spieler gewinnt die Runde (2:1 Auszahlung)."""
        self.balance += self.current_bet * 2

    def push_bet(self):
        """Unentschieden: Einsatz wird zurückgegeben."""
        self.balance += self.current_bet
