import tkinter as tk
import random
from PIL import Image, ImageTk
import os
import pygame.mixer

# Kartendeck erstellen
SUITS = ['Herz', 'Karo', 'Pik', 'Kreuz']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Bube', 'Dame', 'König', 'Ass']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
          'Bube': 10, 'Dame': 10, 'König': 10, 'Ass': 11}


def create_deck():
    return [{'suit': suit, 'rank': rank} for suit in SUITS for rank in RANKS]


class BlackjackGame:
    def __init__(self):
        self.deck = create_deck()
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []
        self.player_money = 1000
        self.current_bet = 0


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


def play_tie_sound():
    pass

def play_error_sound():
    pygame.mixer.music.load("sounds/Error.mp3")
    pygame.mixer.music.play()


def play_winning_sound():
    pygame.mixer.music.load("sounds/Win.mp3")
    pygame.mixer.music.play()


def play_lose_sound():
    pygame.mixer.music.load("sounds/Death.mp3")
    pygame.mixer.music.play()


class BlackjackGUI:
    def __init__(self, root):
        pygame.mixer.init()
        self.game = BlackjackGame()
        self.root = root
        self.root.title("Blackjack")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="green")

        # Button zum Beenden des Spiels
        self.exit_button = tk.Button(root, text="X", font=("Helvetica", 16, "bold"), bg="red", fg="white",
                                     command=self.root.destroy)
        self.exit_button.place(relx=0.98, rely=0.02, anchor="ne")  # Oben rechts positionieren

        self.status_label = tk.Label(root, text="Willkommen bei Blackjack!", font=("Helvetica", 24), fg="black",
                                     bg="green")
        self.status_label.pack(pady=20)

        self.player_frame = tk.Frame(root, bg="green")
        self.player_frame.pack(side=tk.TOP, pady=10)
        self.dealer_frame = tk.Frame(root, bg="green")
        self.dealer_frame.pack(side=tk.TOP, pady=10)

        self.score_label = tk.Label(root, text="Spieler: 0 | Dealer: 0", font=("Helvetica", 14), fg="black", bg="green")
        self.score_label.pack(pady=10)

        self.money_label = tk.Label(root, text=f"Guthaben: {self.game.player_money}", font=("Helvetica", 14),
                                    fg="black", bg="green")
        self.money_label.pack(pady=10)

        self.bet_entry = tk.Entry(root, font=("Helvetica", 14))
        self.bet_entry.pack(pady=10)

        self.buttons_frame = tk.Frame(root, bg="green")
        self.buttons_frame.pack(side=tk.BOTTOM, pady=20)

        self.set_bet_button = tk.Button(self.buttons_frame, text="Einsatz setzen", command=self.set_bet,
                                        font=("Helvetica", 16), bg="grey")
        self.set_bet_button.pack(side=tk.LEFT, padx=10)

        self.hit_button = tk.Button(self.buttons_frame, text="Karte ziehen", command=self.player_hit,
                                    font=("Helvetica", 16), bg="grey", state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.buttons_frame, text="Halten", command=self.player_stand,
                                      font=("Helvetica", 16), bg="grey", state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        self.new_game_button = tk.Button(self.buttons_frame, text="Neues Spiel", command=self.new_game,
                                         font=("Helvetica", 16), bg="grey", fg="black", state=tk.DISABLED)
        self.new_game_button.pack(side=tk.LEFT, padx=10)




    def update_gui(self):
        self.status_label.config(text="Neue Runde neues Glück!")
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

    def set_bet(self):
        """ Setzt den Einsatz und startet eine neue Runde. """
        self.set_bet_button.config(state=tk.NORMAL)
        try:
            bet = int(self.bet_entry.get())
            if 0 < bet <= self.game.player_money:
                self.game.current_bet = bet
                self.game.player_money -= bet
                self.start_round()
            else:
                play_error_sound()
        except ValueError:
            play_error_sound()

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
        """ Spieler zieht eine Karte. """
        self.game.draw_card(self.game.player_hand)
        self.update_gui()

        if self.game.calculate_score(self.game.player_hand) > 21:
            self.status_label.config(text="Spieler hat verloren! Über 21.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.new_game_button.config(state=tk.NORMAL)
            self.set_bet_button.config(state=tk.DISABLED)
            play_lose_sound()

    def player_stand(self):
        """ Der Spieler bleibt stehen, der Dealer ist am Zug. """
        while self.game.calculate_score(self.game.dealer_hand) < 17:
            self.game.draw_card(self.game.dealer_hand)
        self.update_gui()

        player_score = self.game.calculate_score(self.game.player_hand)
        dealer_score = self.game.calculate_score(self.game.dealer_hand)

        if dealer_score > 21 or player_score > dealer_score:
            self.status_label.config(text="Spieler gewinnt!")
            self.set_bet_button.config(state=tk.DISABLED)
            play_winning_sound()
            self.game.player_money += self.game.current_bet * 2  # Verdoppelter Gewinn
        elif player_score < dealer_score:
            self.status_label.config(text="Dealer gewinnt!")
            self.set_bet_button.config(state=tk.DISABLED)
            play_lose_sound()
        else:
            self.status_label.config(text="Unentschieden!")
            self.game.player_money += self.game.current_bet  # Einsatz zurück
            self.set_bet_button.config(state=tk.DISABLED)
            play_tie_sound()
            
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.NORMAL)


    def new_game(self):

        """ Startet eine neue Runde ohne Guthaben zurückzusetzen. """
        self.game.deck = create_deck()  # Neues Deck erstellen
        random.shuffle(self.game.deck)
        self.game.player_hand.clear()
        self.game.dealer_hand.clear()
        self.game.current_bet = 0  # Einsatz zurücksetzen

        self.update_gui()
        self.set_bet_button.config(state=tk.NORMAL)

        if self.game.player_money <= 0:
            play_lose_sound()
            self.status_label.config(text="Du hast kein Guthaben mehr! Spiel beendet.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.new_game_button.config(state=tk.DISABLED)
            self.set_bet_button.config(state=tk.DISABLED)
        else:
            self.status_label.config(text="Neues Spiel gestartet! Setze deinen Einsatz.")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.new_game_button.config(state=tk.DISABLED)




# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
