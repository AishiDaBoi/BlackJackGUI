import random
from PIL import Image, ImageTk

class Deck:
    SUITS = ["Herz", "Karo", "Pik", "Kreuz"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]
    VALUES = {str(i): i for i in range(2, 11)}
    VALUES.update({"Bube": 10, "Dame": 10, "König": 10, "Ass": 11})

    def __init__(self):
        """Erstellt ein gemischtes Kartendeck."""
        self.cards = [{"suit": suit, "rank": rank, "value": self.VALUES[rank]} for suit in self.SUITS for rank in self.RANKS]
        random.shuffle(self.cards)

    def draw_card(self):
        """Zieht eine Karte."""
        return self.cards.pop() if self.cards else None

    def load_card_image(self, card):
        """Lädt das Kartenbild aus dem assets/cards/ Ordner."""
        path = f"assets/cards/{card['suit']}/{card['rank']}.png"
        image = Image.open(path).resize((71, 96))
        return ImageTk.PhotoImage(image)
