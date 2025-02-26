import tkinter as tk
from tkinter import PhotoImage
import os
from .deck import Deck
from .betting import BettingSystem
from .sounds import play_sound
from .animations import animate_card


class BlackjackGame:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.deck = Deck()
        self.betting = BettingSystem(1000)
        self.player_hand = []
        self.dealer_hand = []
        self.card_images = {}

        self.setup_gui()

    def setup_gui(self):
        self.master.title("Blackjack")
        self.master.geometry("800x600")
        self.master.configure(bg="green")

        tk.Label(self.master, text=f"Spieler: {self.username}", font=("Helvetica", 18), bg="green", fg="white").pack()
        self.money_label = tk.Label(self.master, text=f"Guthaben: {self.betting.balance} Chips", font=("Helvetica", 14),
                                    bg="green", fg="white")
        self.money_label.pack()

        self.bet_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.bet_entry.pack()
        tk.Button(self.master, text="Einsatz setzen", font=("Helvetica", 14), command=self.set_bet).pack()

        self.canvas = tk.Canvas(self.master, width=800, height=400, bg="darkgreen")
        self.canvas.pack()

        self.hit_button = tk.Button(self.master, text="Hit", font=("Helvetica", 14), command=self.hit,
                                    state=tk.DISABLED)
        self.hit_button.pack()
        self.stand_button = tk.Button(self.master, text="Stand", font=("Helvetica", 14), command=self.stand,
                                      state=tk.DISABLED)
        self.stand_button.pack()



    def load_card_image(self, card):
        """Lädt das Kartenbild aus dem assets/cards/ Ordner."""
        path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "cards", card['suit'],
                            f"{card['rank']}.png")
        path = os.path.abspath(path)  # Absoluten Pfad berechnen

        print("Lade Bild:", path)  # Debug-Ausgabe

        if not os.path.exists(path):
            print(f"Fehler: {path} nicht gefunden!")  # Fehler ausgeben
            return None

        self.card_images[path] = PhotoImage(file=path)
        return self.card_images[path]


    def draw_card(self, hand, x, y):
        """Zieht eine Karte und zeigt sie an."""
        if self.deck.cards:
            card = self.deck.draw_card()
            hand.append(card)
            img = self.load_card_image(card)
            self.canvas.create_image(x, y, image=img, anchor=tk.NW)
            self.master.update()

    def set_bet(self):
        try:
            bet = int(self.bet_entry.get())
            if self.betting.place_bet(bet):
                self.start_round()
        except ValueError:
            pass

    def start_round(self):
        """Startet eine neue Blackjack-Runde."""
        self.player_hand = []
        self.dealer_hand = []
        self.canvas.delete("all")

        self.draw_card(self.player_hand, 100, 300)
        self.draw_card(self.player_hand, 200, 300)
        self.draw_card(self.dealer_hand, 100, 50)

        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

    def hit(self):
        """Spieler zieht eine Karte."""
        self.draw_card(self.player_hand, 300, 300)

    def stand(self):
        """Dealer zieht eine Karte."""
        self.draw_card(self.dealer_hand, 200, 50)
        self.money_label.config(text="Runde beendet!")