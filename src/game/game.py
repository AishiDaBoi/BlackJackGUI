import tkinter as tk
from tkinter import messagebox, simpledialog
import os
from PIL import Image, ImageTk
from src.game.deck import Deck
from src.game.betting import BettingSystem
from src.game.stats import get_highscore, update_highscore, get_balance, update_balance


def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card['rank'] in ['Bube', 'Dame', 'König']:
            value += 10
        elif card['rank'] == 'Ass':
            value += 11
            aces += 1
        else:
            value += int(card['rank'])

    # Reduziere Asser von 11 auf 1, wenn der Wert über 21 liegt
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1
    return value


class BlackjackGame:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.deck = Deck()
        self.betting = BettingSystem(get_balance(username))  # Guthaben aus der DB laden
        self.player_hand = []
        self.dealer_hand = []
        self.rounds_won = 0
        self.highscore_value = get_highscore(username) or 0
        self.card_images = {}
        self.current_bet = 0

        # Fenster borderless fullscreen windowed machen
        self.master.title("Blackjack")
        self.master.attributes("-fullscreen", True)  # Fenster im Fullscreen-Modus
        self.master.configure(bg="green")
        self.master.resizable(False, False)

        # Speichere Daten, wenn das Fenster geschlossen wird
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        self.setup_gui()
        self.start_round()

    def player_wins_round(self):
        self.rounds_won += 1
        if self.rounds_won > self.highscore_value:
            self.highscore_value = self.rounds_won
            update_highscore(self.username, self.rounds_won)

    def load_card_image(self, card):
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, "..", "..", "assets", "cards", card['suit'], f"{card['rank']}.png")
        path = os.path.abspath(path)

        print(f"Versuche, Bild zu laden: {path}")  # Debugging-Ausgabe

        if not os.path.exists(path):
            print(f"Fehler: {path} nicht gefunden!")
            return None

        if path not in self.card_images:
            try:
                image = Image.open(path).resize((100, 140))  # Größere Karten
                self.card_images[path] = ImageTk.PhotoImage(image)
                print(f"Bild erfolgreich geladen: {path}")  # Debugging-Ausgabe
            except Exception as e:
                print(f"Fehler beim Laden des Bildes: {e}")
                return None
        return self.card_images[path]

    def draw_card(self, hand, x, y, face_up=True):
        if self.deck.cards:
            card = self.deck.draw_card()
            hand.append(card)
            if face_up:
                img = self.load_card_image(card)
            else:
                img = self.load_card_image({'suit': 'cardback', 'rank': 'back'})  # Verdeckte Karte
            if img:
                print(f"Zeichne Karte {card} an Position ({x}, {y})")  # Debugging-Ausgabe
                self.canvas.create_image(x, y, image=img, anchor=tk.NW)
                self.master.update()
            else:
                print(f"Fehler: Bild für Karte {card} konnte nicht geladen werden!")
        else:
            print("Fehler: Keine Karten mehr im Deck!")

    def start_round(self):
        """Startet eine neue Runde."""
        self.player_hand = []
        self.dealer_hand = []
        self.canvas.delete("all")
        self.deck = Deck()  # Neues Deck mischen

        # Manuellen Einsatz setzen
        self.current_bet = self.place_bet()
        if self.current_bet == 0:  # Wenn der Spieler keinen Einsatz setzt, beende die Runde
            return

        # Karten austeilen
        self.draw_card(self.player_hand, 100, 400)  # Erste Karte für den Spieler
        self.draw_card(self.player_hand, 220, 400)  # Zweite Karte für den Spieler
        self.draw_card(self.dealer_hand, 100, 100, face_up=True)  # Erste Karte für den Dealer (aufgedeckt)
        self.draw_card(self.dealer_hand, 220, 100, face_up=False)  # Zweite Karte für den Dealer (verdeckt)

        # Überprüfe, ob der Dealer einen Blackjack hat
        dealer_value = calculate_hand_value(self.dealer_hand)
        if dealer_value == 21:
            # Decke die verdeckte Karte des Dealers auf
            self.canvas.delete("all")
            for i, card in enumerate(self.dealer_hand):
                self.draw_card(self.dealer_hand, 100 + i * 120, 100, face_up=True)

            # Überprüfe, ob der Spieler auch einen Blackjack hat
            player_value = calculate_hand_value(self.player_hand)
            if player_value == 21:
                self.end_round("It's a tie!")  # Unentschieden
            else:
                self.end_round("Dealer wins with Blackjack!")  # Dealer gewinnt mit Blackjack
            return

        # Aktiviere Buttons
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_button.config(state=tk.NORMAL)
        self.surrender_button.config(state=tk.NORMAL)
        self.new_round_button.config(state=tk.DISABLED)
    def place_bet(self):
        """Fragt den Spieler nach dem Einsatz."""
        while True:
            bet = simpledialog.askinteger("Einsatz", "Setzen Sie Ihren Einsatz (1 - {}):".format(self.betting.balance), minvalue=1, maxvalue=self.betting.balance)
            if bet is None:  # Wenn der Benutzer das Fenster schließt
                messagebox.showerror("Fehler", "Bitte setzen Sie einen Einsatz!")
            elif self.betting.place_bet(bet):
                self.balance_label.config(text=f"Guthaben: {self.betting.balance}")
                return bet
            else:
                messagebox.showerror("Fehler", "Ungültiger Einsatz!")

    def setup_gui(self):
        """Erstellt das GUI für das Spiel."""
        self.canvas = tk.Canvas(self.master, width=1200, height=800, bg="green", highlightthickness=0)
        self.canvas.pack()

        # Buttons mit größerer Schrift und Abmessungen
        button_width = 15
        button_font = ("Helvetica", 18)
        self.hit_button = tk.Button(self.master, text="Hit", font=button_font, width=button_width, command=self.hit)
        self.hit_button.place(x=50, y=650)

        self.stand_button = tk.Button(self.master, text="Stand", font=button_font, width=button_width,
                                      command=self.stand)
        self.stand_button.place(x=300, y=650)

        self.double_button = tk.Button(self.master, text="Double", font=button_font, width=button_width,
                                       command=self.double)
        self.double_button.place(x=550, y=650)

        self.surrender_button = tk.Button(self.master, text="Surrender", font=button_font, width=button_width,
                                          command=self.surrender)
        self.surrender_button.place(x=800, y=650)

        self.new_round_button = tk.Button(self.master, text="Neue Runde", font=button_font, width=button_width,
                                          command=self.start_round)
        self.new_round_button.place(x=1050, y=650)

        # Labels mit größerer Schrift
        label_font = ("Helvetica", 20)
        self.player_label = tk.Label(self.master, text=f"Spieler: {self.username}", font=label_font, bg="green",
                                     fg="white")
        self.player_label.place(x=50, y=20)

        self.balance_label = tk.Label(self.master, text=f"Guthaben: {self.betting.balance}", font=label_font,
                                      bg="green", fg="white")
        self.balance_label.place(x=50, y=60)

        self.highscore_label = tk.Label(self.master, text=f"Highscore: {self.highscore_value}", font=label_font,
                                        bg="green", fg="white")
        self.highscore_label.place(x=50, y=100)

    def hit(self):
        """Zieht eine zusätzliche Karte für den Spieler."""
        if len(self.player_hand) < 5:  # Begrenze die Anzahl der Karten auf 5
            self.draw_card(self.player_hand, 100 + len(self.player_hand) * 120, 400)
            player_value = calculate_hand_value(self.player_hand)
            if player_value > 21:
                self.end_round("Dealer wins!")

    def stand(self):
        """Beendet den Zug des Spielers und lässt den Dealer ziehen."""
        # Decke die verdeckte Karte des Dealers auf
        self.canvas.delete("all")
        for i, card in enumerate(self.dealer_hand):
            self.draw_card(self.dealer_hand, 100 + i * 120, 100, face_up=True)

        # Dealer-Wert berechnen
        dealer_value = calculate_hand_value(self.dealer_hand)
        print(f"[DEBUG] Dealer-Wert vor dem Ziehen: {dealer_value}")

        # Dealer zieht Karten, bis er mindestens 17 Punkte hat
        while dealer_value < 17:
            if not self.deck.cards:
                print("[ERROR] Keine Karten mehr im Deck!")
                break

            # Neue Karte ziehen und dem Dealer hinzufügen
            new_card = self.deck.draw_card()
            if new_card is None:
                break

            self.dealer_hand.append(new_card)
            self.draw_card(self.dealer_hand, 100 + (len(self.dealer_hand) - 1) * 120, 100, face_up=True)

            # Dealer-Wert NEU berechnen
            dealer_value = calculate_hand_value(self.dealer_hand)
            print(f"[DEBUG] Dealer zieht {new_card['rank']} {new_card['suit']}. Neuer Wert: {dealer_value}")

        # Runde beenden
        self.end_round()

    def double(self):
        """Verdoppelt den Einsatz und zieht eine zusätzliche Karte."""
        if self.betting.place_bet(self.current_bet):  # Verdopple den Einsatz
            self.draw_card(self.player_hand, 100 + len(self.player_hand) * 120, 400)
            self.balance_label.config(text=f"Guthaben: {self.betting.balance}")  # Aktualisiere das Guthaben-Label
            self.stand()  # Beende den Zug des Spielers nach dem Double

    def surrender(self):
        """Beendet die Runde und gibt dem Spieler die Hälfte des Einsatzes zurück."""
        self.betting.push_bet()  # Gib die Hälfte des Einsatzes zurück
        self.balance_label.config(text=f"Guthaben: {self.betting.balance}")  # Aktualisiere das Guthaben-Label
        self.end_round("Spieler gibt auf!")

    def end_round(self, result=None):
        """Beendet die Runde und zeigt das Ergebnis an."""
        if not result:
            player_value = calculate_hand_value(self.player_hand)
            dealer_value = calculate_hand_value(self.dealer_hand)
            if player_value > 21:
                result = "Dealer wins!"
            elif dealer_value > 21:
                result = "Player wins!"
                self.betting.win_bet()  # Spieler gewinnt den Einsatz
            elif player_value > dealer_value:
                result = "Player wins!"
                self.betting.win_bet()  # Spieler gewinnt den Einsatz
            elif dealer_value > player_value:
                result = "Dealer wins!"
            else:
                result = "It's a tie!"
                self.betting.push_bet()  # Unentschieden: Einsatz wird zurückgegeben

        # Aktualisiere das Guthaben-Label
        self.balance_label.config(text=f"Guthaben: {self.betting.balance}")

        # Speichere Guthaben und Highscore in der Datenbank
        update_balance(self.username, self.betting.balance)
        update_highscore(self.username, self.highscore_value)

        # Zeige das Ergebnis an
        messagebox.showinfo("Round Over", result)

        # Deaktiviere Buttons und aktiviere den "Neue Runde"-Button
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_button.config(state=tk.DISABLED)
        self.surrender_button.config(state=tk.DISABLED)
        self.new_round_button.config(state=tk.NORMAL)

    def on_close(self):
        """Speichert Daten und schließt das Fenster."""
        update_balance(self.username, self.betting.balance)
        update_highscore(self.username, self.highscore_value)
        self.master.destroy()