import tkinter as tk
import random
from PIL import Image, ImageTk
import os

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
        self.player_score = 0
        self.dealer_score = 0
        self.player_money = 1000  # Startguthaben
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

# GUI erstellen
class BlackjackGUI:
    def __init__(self, root):
        self.game = BlackjackGame()

        # Fenster konfigurieren (Vollbildmodus)
        self.root = root
        self.root.title("Blackjack")
        self.root.attributes('-fullscreen', True)

        # Hintergrundfarbe (schwarz zu Beginn)
        self.root.configure(bg="green")

        # GUI-Komponenten
        self.status_label = tk.Label(root, text="Willkommen bei Blackjack!", font=("Helvetica", 24), fg="black", bg="green")
        self.status_label.pack(pady=20)

        # Spieler-Frame und Anzeige der Karten
        self.player_frame = tk.Frame(root)
        self.player_frame.pack(side=tk.TOP, pady=10)
        self.player_label = tk.Label(self.player_frame, text="Deine Karten: ", font=("Helvetica", 14), fg="black", bg="green")
        self.player_label.pack(side=tk.LEFT)

        # Dealer-Frame und Anzeige der Karten
        self.dealer_frame = tk.Frame(root, bg="green")
        self.dealer_frame.pack(side=tk.TOP, pady=10)
        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer-Karten: ", font=("Helvetica", 14), fg="black", bg="green")
        self.dealer_label.pack(side=tk.LEFT)

        # Anzeige des aktuellen Punktestands
        self.score_label = tk.Label(root, text="Spieler: 0 | Dealer: 0", font=("Helvetica", 14), fg="black", bg="green")
        self.score_label.pack(pady=10)

        # Anzeige des Guthabens
        self.money_label = tk.Label(root, text=f"Guthaben: {self.game.player_money}€", font=("Helvetica", 14), fg="black", bg="green")
        self.money_label.pack(pady=10)

        # Eingabefeld für den Einsatz
        self.bet_label = tk.Label(root, text="Setze deinen Einsatz:", font=("Helvetica", 14), fg="black", bg="green")
        self.bet_label.pack(pady=10)

        self.bet_entry = tk.Entry(root, font=("Helvetica", 14))
        self.bet_entry.pack(pady=10)

        # Button-Frame für Aktionen
        self.buttons_frame = tk.Frame(root, bg="green")
        self.buttons_frame.pack(side=tk.BOTTOM, pady=20)

        self.set_bet_button = tk.Button(self.buttons_frame, text="Einsatz setzen", command=self.set_bet, font=("Helvetica", 16), bg="grey")
        self.set_bet_button.pack(side=tk.LEFT, padx=10)

        self.hit_button = tk.Button(self.buttons_frame, text="Karte ziehen", command=self.player_hit, font=("Helvetica", 16), bg="grey", state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.buttons_frame, text="Halten", command=self.player_stand, font=("Helvetica", 16), bg="grey", state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        # Neues Spiel Button (wird erst am Ende der Runde angezeigt)
        self.new_game_button = tk.Button(self.buttons_frame, text="Neues Spiel", command=self.new_game, font=("Helvetica", 16), bg="grey", fg="black", state=tk.DISABLED)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

    def update_gui(self):
        # Bilder für Spieler und Dealer aktualisieren
        self.display_cards(self.game.player_hand, self.player_frame)
        self.display_cards(self.game.dealer_hand, self.dealer_frame)
        self.update_score()

    def display_cards(self, hand, frame):
        for widget in frame.winfo_children():
            widget.destroy()  # Vorherige Karten löschen
        for card in hand:
            img_path = os.path.join('cards', card['suit'], f"{card['rank']}.png")
            img = Image.open(img_path)
            img = img.resize((71, 96))  # Größe der Karten anpassen
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=img_tk, bg="green")
            label.image = img_tk  # Referenz speichern, damit das Bild nicht gelöscht wird
            label.pack(side=tk.LEFT, padx=5)

    def update_score(self):
        self.game.player_score = self.game.calculate_score(self.game.player_hand)
        self.game.dealer_score = self.game.calculate_score(self.game.dealer_hand)
        self.score_label.config(text=f"Spieler: {self.game.player_score} | Dealer: {self.game.dealer_score}")
        self.money_label.config(text=f"Guthaben: {self.game.player_money}€")

    def set_bet(self):
        bet = self.bet_entry.get()
        try:
            bet = int(bet)
        except ValueError:
            self.status_label.config(text="Ungültiger Einsatz! Bitte eine Zahl eingeben.")
            return

        if bet <= 0 or bet > self.game.player_money:
            self.status_label.config(text="Ungültiger Einsatz! Dein Guthaben reicht nicht aus.")
            return

        # Einsatz setzen
        self.game.current_bet = bet
        self.game.player_money -= bet  # Einsatz vom Guthaben abziehen

        # Verstecke Einsatz Widgets
        self.bet_label.pack_forget()
        self.bet_entry.pack_forget()
        self.set_bet_button.pack_forget()

        # Deck mischen und Karten austeilen
        self.game = BlackjackGame()
        self.game.draw_card(self.game.player_hand)
        self.game.draw_card(self.game.player_hand)
        self.game.draw_card(self.game.dealer_hand)
        self.game.draw_card(self.game.dealer_hand)

        # Reset Buttons und Status
        self.status_label.config(text="Deine Karten")
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.new_game_button.config(state=tk.DISABLED)  # Deaktiviert, bis die Runde endet
        self.root.configure(bg="green")
        self.update_gui()

    def player_hit(self):
        self.game.draw_card(self.game.player_hand)
        self.update_gui()
        if self.game.player_score > 21:
            self.status_label.config(text="Du hast überzogen! Der Dealer gewinnt.")
            self.root.configure(bg="green")
            self.hit_button.config(state=tk.DISABLED)
            self.stand_button.config(state=tk.DISABLED)
            self.end_round()

    def player_stand(self):
        self.status_label.config(text="Du hältst. Der Dealer spielt...")
        # Dealer zieht Karten bis mindestens 17 Punkte erreicht sind
        while self.game.dealer_score < 17:
            self.game.draw_card(self.game.dealer_hand)
            self.update_gui()

        # Gewinner ermitteln
        if self.game.dealer_score > 21 or self.game.player_score > self.game.dealer_score:
            self.status_label.config(text="Du gewinnst!")
            self.root.configure(bg="green")
            self.game.player_money += self.game.current_bet  # Gewinn: Einsatz zurückbekommen + gewinn
        elif self.game.player_score < self.game.dealer_score:
            self.status_label.config(text="Der Dealer gewinnt!")
            self.root.configure(bg="green")
            self.game.player_money -= self.game.current_bet  # Verlust: Einsatz verloren
        else:
            self.status_label.config(text="Unentschieden!")
            self.root.configure(bg="green")  # Unentschieden als gelb darstellen

        self.end_round()

    def end_round(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.new_game_button.config(state=tk.NORMAL)  # Neues Spiel Button aktivieren

    def new_game(self):
        bet = self.bet_entry.get()
        try:
            bet = int(bet)
        except ValueError:
            bet = 0

        # Überprüfen, ob der Einsatz gültig ist
        if bet <= 0 or bet > self.game.player_money:
            self.status_label.config(text="Ungültiger Einsatz!")
            return

        # Einsatz setzen
        self.game.current_bet = bet
        self.game.player_money -= bet  # Einsatz vom Guthaben abziehen

        # Deck mischen und Karten austeilen
        self.game = BlackjackGame()
        self.game.draw_card(self.game.player_hand)
        self.game.draw_card(self.game.player_hand)
        self.game.draw_card(self.game.dealer_hand)
        self.game.draw_card(self.game.dealer_hand)

        # Reset Buttons und Status
        self.status_label.config(text="Deine Karten")
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.new_game_button.config(state=tk.DISABLED)  # Deaktiviert, bis die Runde endet
        self.root.configure(bg="green")
        self.update_gui()

# Hauptprogramm
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackGUI(root)
    root.mainloop()
