import tkinter as tk
from tkinter import PhotoImage
import os
from PIL import Image, ImageTk
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

        self.master.title("Blackjack")
        self.master.geometry("800x600")
        self.master.configure(bg="green")
        self.master.resizable(False, False)  # Windowed Mode (nicht skalierbar)

        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.master, text=f"Spieler: {self.username}", font=("Helvetica", 18), bg="green", fg="white").pack()
        self.money_label = tk.Label(self.master, text=f"Guthaben: {self.betting.balance} Chips", font=("Helvetica", 14), bg="green", fg="white")
        self.money_label.pack()

        self.dealer_label = tk.Label(self.master, text="Dealer", font=("Helvetica", 14), bg="green", fg="white")
        self.dealer_label.pack()
        self.canvas = tk.Canvas(self.master, width=800, height=400, bg="darkgreen")
        self.canvas.pack()
        self.player_label = tk.Label(self.master, text="Spieler", font=("Helvetica", 14), bg="green", fg="white")
        self.player_label.pack()

        self.controls_frame = tk.Frame(self.master, bg="green")
        self.controls_frame.pack(fill=tk.X, pady=10)

        self.bet_entry = tk.Entry(self.controls_frame, font=("Helvetica", 14), width=10)
        self.bet_entry.grid(row=0, column=0, padx=5)
        tk.Button(self.controls_frame, text="Einsatz setzen", font=("Helvetica", 14), command=self.set_bet).grid(row=0, column=1, padx=5)

        self.hit_button = tk.Button(self.controls_frame, text="Hit", font=("Helvetica", 14), command=self.hit, state=tk.DISABLED)
        self.hit_button.grid(row=0, column=2, padx=5)

        self.stand_button = tk.Button(self.controls_frame, text="Stand", font=("Helvetica", 14), command=self.stand, state=tk.DISABLED)
        self.stand_button.grid(row=0, column=3, padx=5)

    def load_card_image(self, card):
        """Lädt das Kartenbild aus dem assets/cards/ Ordner und skaliert es."""
        path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "cards", card['suit'], f"{card['rank']}.png")
        path = os.path.abspath(path)

        if not os.path.exists(path):
            print(f"Fehler: {path} nicht gefunden!")
            return None

        if path not in self.card_images:
            image = Image.open(path).resize((71, 96))  # Skalierung auf kleinere Größe
            self.card_images[path] = ImageTk.PhotoImage(image)
        return self.card_images[path]

    def draw_card(self, hand, x, y):
        """Zieht eine Karte und zeigt sie an."""
        if self.deck.cards:
            card = self.deck.draw_card()
            hand.append(card)
            img = self.load_card_image(card)
            if img:
                self.canvas.create_image(x, y, image=img, anchor=tk.NW)
                self.master.update()

    def calculate_score(self, hand):
        """Berechnet die Punktzahl einer Hand."""
        score = sum(card['value'] for card in hand)
        num_aces = sum(1 for card in hand if card['rank'] == 'Ass')
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score

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

        self.draw_card(self.player_hand, 100, 300)  # Spieler links
        self.draw_card(self.player_hand, 180, 300)
        self.draw_card(self.dealer_hand, 100, 50)  # Dealer oben
        self.draw_card(self.dealer_hand, 180, 50)

        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)

    def hit(self):
        """Spieler zieht eine Karte."""
        x = 100 + (len(self.player_hand) * 80)  # Karten nebeneinander anordnen
        self.draw_card(self.player_hand, x, 300)
        if self.calculate_score(self.player_hand) > 21:
            self.money_label.config(text="Spieler hat über 21! Dealer gewinnt.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)

    def stand(self):
        """Dealer zieht Karten bis mindestens 17 Punkte erreicht sind."""
        while self.calculate_score(self.dealer_hand) < 17:
            x = 100 + (len(self.dealer_hand) * 80)
            self.draw_card(self.dealer_hand, x, 50)
        self.money_label.config(text="Runde beendet!")
