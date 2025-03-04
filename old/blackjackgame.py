import tkinter as tk
import random
import pygame.mixer
from highscore import update_highscore, get_highscore
from src import load_users, save_users

# Kartenwerte & Symbole
SUITS = ['Herz', 'Karo', 'Pik', 'Kreuz']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Bube', 'Dame', 'König', 'Ass']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'Bube': 10, 'Dame': 10, 'König': 10, 'Ass': 11}

# Sound-Effekte
pygame.mixer.init()

def play_sound(file):
    pygame.mixer.Sound(file).play()

class BlackjackGame:
    def __init__(self, master, username):
        self.deck = self.create_deck()
        self.player_hand = []
        self.dealer_hand = []
        self.player_money = 1000
        self.current_bet = 0
        self.master = master
        self.username = username
        self.rounds_won = 0
        self.highscore_value = max(get_highscore(username), self.load_json_highscore(username))

    def create_deck(self):
        """Erstellt ein gemischtes Kartendeck."""
        deck = [{'suit': suit, 'rank': rank} for suit in SUITS for rank in RANKS]
        random.shuffle(deck)
        return deck

    def load_json_highscore(self, username):
        """Lädt den Highscore aus der JSON-Datei."""
        users = load_users()
        return users.get(username, {}).get("highscore", 0)

    def save_json_highscore(self):
        """Speichert den Highscore in JSON."""
        users = load_users()
        users[self.username]["highscore"] = self.highscore_value
        save_users(users)

    def update_highscore(self):
        """Speichert den höchsten Score in DB und JSON."""
        update_highscore(self.username, self.rounds_won)
        self.highscore_value = max(self.highscore_value, self.rounds_won)
        self.save_json_highscore()

    def place_bet(self, bet):
        """Setzt einen Einsatz."""
        if 0 < bet <= self.player_money:
            self.current_bet = bet
            self.player_money -= bet
            return True
        return False

    def draw_card(self, hand):
        """Zieht eine Karte für den Spieler oder den Dealer."""
        if self.deck:
            hand.append(self.deck.pop())

    def calculate_score(self, hand):
        """Berechnet den Punktestand einer Hand."""
        score = sum(VALUES[card['rank']] for card in hand)
        num_aces = sum(1 for card in hand if card['rank'] == 'Ass')
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score

    def player_wins(self):
        """Spieler gewinnt die Runde."""
        self.player_money += self.current_bet * 2
        self.rounds_won += 1
        self.update_highscore()
        play_sound("../assets/sounds/win.mp3")

    def dealer_wins(self):
        """Dealer gewinnt die Runde."""
        play_sound("sounds/lose.mp3")

    def check_blackjack(self):
        """Überprüft, ob ein Blackjack vorliegt."""
        player_blackjack = self.calculate_score(self.player_hand) == 21 and len(self.player_hand) == 2
        dealer_blackjack = self.calculate_score(self.dealer_hand) == 21 and len(self.dealer_hand) == 2

        if player_blackjack and dealer_blackjack:
            return "Tie"
        elif player_blackjack:
            self.player_money += int(self.current_bet * 2.5)
            self.rounds_won += 1
            self.update_highscore()
            play_sound("../assets/sounds/win.mp3")
            return "Player Blackjack"
        elif dealer_blackjack:
            play_sound("sounds/lose.mp3")
            return "Dealer Blackjack"
        return None

    def dealer_play(self):
        """Der Dealer zieht Karten, bis er mindestens 17 Punkte hat."""
        while self.calculate_score(self.dealer_hand) < 17:
            self.draw_card(self.dealer_hand)

    def resolve_game(self):
        """Ermittelt den Gewinner der Runde."""
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)

        if player_score > 21:
            return "Player Bust"
        elif dealer_score > 21:
            self.player_wins()
            return "Dealer Bust"
        elif player_score > dealer_score:
            self.player_wins()
            return "Player Wins"
        elif player_score < dealer_score:
            self.dealer_wins()
            return "Dealer Wins"
        else:
            self.player_money += self.current_bet  # Einsatz zurück
            play_sound("../assets/sounds/Tie.mp3")
            return "Tie"

class BlackjackGUI:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.game = BlackjackGame(self.root, self.username)

        self.root.title("Blackjack")
        self.root.geometry("800x600")
        self.root.configure(bg="green")

        tk.Label(root, text=f"Spieler: {self.username}", font=("Helvetica", 18), bg="green", fg="white").pack()

        self.status_label = tk.Label(root, text="Setze deinen Einsatz!", font=("Helvetica", 14), bg="green", fg="white")
        self.status_label.pack()

        self.money_label = tk.Label(root, text=f"Guthaben: {self.game.player_money}", font=("Helvetica", 14), bg="green", fg="white")
        self.money_label.pack()

        self.bet_entry = tk.Entry(root, font=("Helvetica", 14))
        self.bet_entry.pack()

        tk.Button(root, text="Einsatz setzen", font=("Helvetica", 14), command=self.set_bet).pack()

        self.hit_button = tk.Button(root, text="Hit", font=("Helvetica", 14), command=self.hit, state=tk.DISABLED)
        self.hit_button.pack()

        self.stand_button = tk.Button(root, text="Stand", font=("Helvetica", 14), command=self.stand, state=tk.DISABLED)
        self.stand_button.pack()

    def set_bet(self):
        """Spieler setzt einen Einsatz und das Spiel beginnt."""
        try:
            bet = int(self.bet_entry.get())
            if self.game.place_bet(bet):
                self.game.draw_card(self.game.player_hand)
                self.game.draw_card(self.game.player_hand)
                self.game.draw_card(self.game.dealer_hand)
                self.hit_button.config(state=tk.NORMAL)
                self.stand_button.config(state=tk.NORMAL)
            else:
                self.status_label.config(text="Ungültiger Einsatz!")
        except ValueError:
            self.status_label.config(text="Bitte eine Zahl eingeben!")

    def hit(self):
        """Spieler zieht eine Karte."""
        self.game.draw_card(self.game.player_hand)
        if self.game.calculate_score(self.game.player_hand) > 21:
            self.status_label.config(text="Bust! Du hast verloren.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)

    def stand(self):
        """Spieler bleibt stehen, der Dealer spielt."""
        self.game.dealer_play()
        result = self.game.resolve_game()
        self.status_label.config(text=result)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
