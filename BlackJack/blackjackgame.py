# blackjackgame.py

import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os
import pygame.mixer
from auth import register_user, login_user
import highscore

# --- Kartendeck und Utility-Funktionen ---

SUITS = ['Herz', 'Karo', 'Pik', 'Kreuz']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Bube', 'Dame', 'König', 'Ass']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'Bube': 10, 'Dame': 10, 'König': 10, 'Ass': 11}


def create_deck():
    return [{'suit': suit, 'rank': rank} for suit in SUITS for rank in RANKS]


def changeOnHover(button, colorOnHover, colorOnLeave):
    button.bind("<Enter>", lambda e: button.config(background=colorOnHover))
    button.bind("<Leave>", lambda e: button.config(background=colorOnLeave))


# --- Spiel-Logik ---

class BlackjackGame:
    def __init__(self, master, username):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.player_money = 1000
        self.current_bet = 0
        self.master = master
        self.username = username
        self.rounds_won = 0  # Gewonnene Runden
        self.highscore_value = highscore.get_highscore(username) or 0  # Falls None, setze 0

    def player_wins_round(self):
        """Wird aufgerufen, wenn der Spieler eine Runde gewinnt."""
        self.rounds_won += 1

        # Falls der neue Wert höher ist als der gespeicherte Highscore → Update
        if self.rounds_won > self.highscore_value:
            self.highscore_value = self.rounds_won
            highscore.update_highscore(self.username, self.rounds_won)

    def draw_card(self, hand):
        if self.deck:
            hand.append(self.deck.pop())

    def calculate_score(self, hand):
        score = sum(VALUES[card['rank']] for card in hand)
        num_aces = sum(1 for card in hand if card['rank'] == 'Ass')
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score


# --- Sound-Funktionen ---

def play_background_music():
    pygame.mixer.music.load("sounds/backgroundMusic.mp3")
    pygame.mixer.music.play(10000, 0.0, 0)
    pygame.mixer.music.set_volume(0.05)


def play_tie_sound():
    pygame.mixer.music.load("sounds/Tie.mp3")
    pygame.mixer.music.play()


def play_error_sound():
    pygame.mixer.music.load("sounds/errorEcho.mp3")
    pygame.mixer.music.play()


def play_winning_sound():
    pygame.mixer.music.load("sounds/Win.mp3")
    pygame.mixer.music.play()


def play_lose_sound():
    pygame.mixer.music.load("sounds/Death.mp3")
    pygame.mixer.music.play()


# --- Blackjack GUI ---

class BlackjackGUI:
    def __init__(self, root, username):
        self.root = root
        pygame.mixer.init()
        self.username = username
        self.game = BlackjackGame(self.root, self.username)

        # Zähler für gewonnene Runden in dieser Sitzung
        self.rounds_won = 0
        # Highscore aus der DB (maximal gewonnene Runden in früheren Sitzungen)
        self.highscore_value = highscore.get_highscore(self.username)

        self.root = root
        self.root.title("Blackjack")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="green")
        play_background_music()

        # Button zum Beenden des Spiels
        self.exit_button = tk.Button(root, text="X", font=("Helvetica", 16, "bold"),
                                     bg="red", fg="white", command=self.root.destroy)
        self.exit_button.place(relx=0.98, rely=0.02, anchor="ne")

        self.status_label = tk.Label(root, text="Willkommen bei Blackjack!",
                                     font=("Helvetica", 24), fg="black", bg="green")
        self.status_label.pack(pady=20)

        self.player_frame = tk.Frame(root, bg="green")
        self.player_frame.pack(side=tk.TOP, pady=10)
        self.dealer_frame = tk.Frame(root, bg="green")
        self.dealer_frame.pack(side=tk.TOP, pady=10)

        self.score_label = tk.Label(root, text="Spieler: 0 | Dealer: 0",
                                    font=("Helvetica", 14), fg="black", bg="green")
        self.score_label.pack(pady=10)

        # Bestehende Guthabenanzeige (optional)
        self.money_label = tk.Label(root, text=f"Guthaben: {self.game.player_money}",
                                    font=("Helvetica", 14), fg="black", bg="green")
        self.money_label.pack(pady=10)

        # Anzeige für gewonnene Runden
        self.rounds_label = tk.Label(root, text=f"Gewonnene Runden: {self.rounds_won}",
                                     font=("Helvetica", 14), fg="black", bg="green")
        self.rounds_label.pack(pady=10)

        # Anzeige für den Highscore (maximal gewonnene Runden)
        self.highscore_label = tk.Label(root, text=f"Highscore (max. gewonnene Runden): {self.highscore_value}",
                                        font=("Helvetica", 14), fg="black", bg="green")
        self.highscore_label.pack(pady=10)

        self.bet_entry = tk.Entry(root, font=("Helvetica", 14))
        self.bet_entry.pack(pady=10)

        self.buttons_frame = tk.Frame(root, bg="green")
        self.buttons_frame.pack(side=tk.BOTTOM, pady=20)

        self.set_bet_button = tk.Button(self.buttons_frame, text="Einsatz setzen",
                                        command=self.set_bet, font=("Helvetica", 16), bg="grey")
        self.set_bet_button.pack(side=tk.LEFT, padx=10)

        self.hit_button = tk.Button(self.buttons_frame, text="Karte ziehen",
                                    command=self.player_hit, font=("Helvetica", 16),
                                    bg="grey", state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.buttons_frame, text="Halten",
                                      command=self.player_stand, font=("Helvetica", 16),
                                      bg="grey", state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        self.new_game_button = tk.Button(self.buttons_frame, text="Nächste Runde",
                                         command=self.new_game, font=("Helvetica", 16),
                                         bg="grey", fg="black", state=tk.DISABLED)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        changeOnHover(self.set_bet_button, "white", "grey")
        changeOnHover(self.hit_button, "white", "grey")
        changeOnHover(self.stand_button, "white", "grey")
        changeOnHover(self.new_game_button, "white", "grey")

    def update_gui(self):
        self.status_label.config(text="Neue Runde – gutes Gelingen!")
        self.display_cards(self.game.player_hand, self.player_frame)
        self.display_cards(self.game.dealer_hand, self.dealer_frame)
        self.update_score()
        self.set_bet_button.config(state=tk.DISABLED)

    def display_cards(self, hand, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        for card in hand:
            img_path = f'cards/{card["suit"]}/{card["rank"]}.png'
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((71, 96))
                img_tk = ImageTk.PhotoImage(img)
                label = tk.Label(frame, image=img_tk, bg="green")
                label.image = img_tk
                label.pack(side=tk.LEFT, padx=5)

    def update_score(self):
        self.score_label.config(
            text=f"Spieler: {self.game.calculate_score(self.game.player_hand)} | Dealer: {self.game.calculate_score(self.game.dealer_hand)}")
        self.money_label.config(text=f"Guthaben: {self.game.player_money}")
        self.rounds_label.config(text=f"Gewonnene Runden: {self.rounds_won}")
        self.highscore_label.config(text=f"Highscore (max. gewonnene Runden): {self.highscore_value}")

    def set_bet(self):
        try:
            bet = int(self.bet_entry.get())
            if 0 < bet <= self.game.player_money:
                self.game.current_bet = bet
                self.game.player_money -= bet
                self.start_round()
            else:
                play_error_sound()
                self.status_label.config(text="Ungültiger Einsatz!")
        except ValueError:
            play_error_sound()
            self.status_label.config(text="Bitte eine gültige Zahl eingeben!")

    def start_round(self):
        self.game.player_hand.clear()
        self.game.dealer_hand.clear()
        self.game.draw_card(self.game.player_hand)
        self.game.draw_card(self.game.player_hand)
        self.game.draw_card(self.game.dealer_hand)
        self.game.draw_card(self.game.dealer_hand)
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.new_game_button.config(state=tk.DISABLED)
        self.update_gui()

    def player_hit(self):
        self.game.draw_card(self.game.player_hand)
        self.update_gui()
        if self.game.calculate_score(self.game.player_hand) > 21:
            self.status_label.config(text="Du hast überkauft! Runde verloren.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.new_game_button.config(state=tk.NORMAL)
            play_lose_sound()

    def player_stand(self):
        while self.game.calculate_score(self.game.dealer_hand) < 17:
            self.game.draw_card(self.game.dealer_hand)
        self.update_gui()

        player_score = self.game.calculate_score(self.game.player_hand)
        dealer_score = self.game.calculate_score(self.game.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            self.status_label.config(text="Du gewinnst die Runde!")
            play_winning_sound()
            # Runde gewonnen – Zähler erhöhen
            self.rounds_won += 1
            # Falls neuer Rekord erzielt wurde, in der DB speichern
            if self.rounds_won > self.highscore_value:
                self.highscore_value = self.rounds_won
                highscore.update_highscore(self.username, self.highscore_value)
        elif player_score < dealer_score:
            self.status_label.config(text="Dealer gewinnt die Runde!")
            play_lose_sound()
        else:
            self.status_label.config(text="Unentschieden!")
            play_tie_sound()

        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.NORMAL)
        self.update_score()

    def new_game(self):
        # Erstelle ein neues Deck und setze die Hände sowie den aktuellen Einsatz zurück.
        self.game.deck = create_deck()
        random.shuffle(self.game.deck)
        self.game.player_hand.clear()
        self.game.dealer_hand.clear()
        self.game.current_bet = 0

        if self.game.player_money <= 0:
            play_lose_sound()
            self.status_label.config(text="Kein Guthaben mehr – Spiel beendet.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.new_game_button.config(state=tk.DISABLED)
            self.set_bet_button.config(state=tk.DISABLED)
        else:
            self.status_label.config(text="Neue Runde! Setze deinen Einsatz.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.new_game_button.config(state=tk.DISABLED)
            self.set_bet_button.config(state=tk.NORMAL)
        self.update_score()


