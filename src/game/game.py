import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup

from src.game.deck import Deck
from src.game.betting import BettingSystem
from src.auth.database import get_db_connection  # MySQL-Verbindung


class BlackjackGame(BoxLayout):
    def __init__(self, username, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.credits = self.load_credits_from_db(username)
        self.deck = Deck()
        self.betting = BettingSystem(self.credits)
        self.player_hand = []
        self.dealer_hand = []
        self.split_mode = False  # Für spätere Split-Logik

        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Hintergrund (dunkelgrün)
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0.2, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.setup_gui()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def load_credits_from_db(self, username):
        """Lädt das Guthaben eines Spielers aus der MySQL-Datenbank."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT credits FROM savefiles WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 1000

    def save_credits_to_db(self):
        """Speichert das Guthaben des Spielers in die Datenbank."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE savefiles SET credits = %s WHERE username = %s", (self.betting.balance, self.username))
        conn.commit()
        conn.close()

    def setup_gui(self):
        # Header: Spielername & Guthaben (dauerhaft sichtbar)
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)
        header.add_widget(Label(text=f"Spieler: {self.username}", font_size=24, color=(1, 1, 1, 1)))
        self.money_label = Label(text=f"Guthaben: {self.betting.balance} Chips", font_size=18, color=(1, 1, 1, 1))
        header.add_widget(self.money_label)
        self.add_widget(header)

        # Dealer-Bereich
        dealer_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), padding=10, spacing=5)
        dealer_layout.add_widget(Label(text="Dealer", font_size=18, color=(1, 1, 1, 1)))
        self.dealer_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=150)
        dealer_layout.add_widget(self.dealer_grid)
        self.add_widget(dealer_layout)

        # Spieler-Bereich
        player_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), padding=10, spacing=5)
        player_layout.add_widget(Label(text="Spieler", font_size=18, color=(1, 1, 1, 1)))
        self.player_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=150)
        player_layout.add_widget(self.player_grid)
        self.add_widget(player_layout)

        # Einsatz-Eingabe: Einsatz setzen und All-In
        bet_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)
        self.bet_entry = TextInput(hint_text="Einsatz", font_size=18, multiline=False, size_hint=(0.3, 1))
        bet_layout.add_widget(self.bet_entry)
        self.bet_button = Button(text="Einsatz setzen", font_size=18, size_hint=(0.3, 1))
        self.bet_button.bind(on_press=self.set_bet)
        bet_layout.add_widget(self.bet_button)
        self.all_in_button = Button(text="All-In", font_size=18, size_hint=(0.3, 1))
        self.all_in_button.bind(on_press=self.all_in)
        bet_layout.add_widget(self.all_in_button)
        self.add_widget(bet_layout)

        # Aktionsbuttons: Hit, Stand, Double Down, Split, Neue Runde
        action_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.2), padding=10, spacing=10)
        self.hit_button = Button(text="Hit", font_size=18, size_hint=(0.2, 1), disabled=True)
        self.hit_button.bind(on_press=self.hit)
        action_layout.add_widget(self.hit_button)

        self.stand_button = Button(text="Stand", font_size=18, size_hint=(0.2, 1), disabled=True)
        self.stand_button.bind(on_press=self.stand)
        action_layout.add_widget(self.stand_button)

        self.double_button = Button(text="Double Down", font_size=18, size_hint=(0.2, 1), disabled=True)
        self.double_button.bind(on_press=self.double_down)
        action_layout.add_widget(self.double_button)

        self.split_button = Button(text="Split", font_size=18, size_hint=(0.2, 1), disabled=True)
        self.split_button.bind(on_press=self.split)
        action_layout.add_widget(self.split_button)

        self.new_round_button = Button(text="Neue Runde", font_size=18, size_hint=(0.2, 1), disabled=True)
        self.new_round_button.bind(on_press=self.new_round)
        action_layout.add_widget(self.new_round_button)

        self.add_widget(action_layout)

    def load_card_image(self, card):
        """Lädt das Kartenbild."""
        suit_translation = {"Herz": "Herz", "Karo": "Karo", "Pik": "Pik", "Kreuz": "Kreuz"}
        suit = suit_translation.get(card['suit'], card['suit'])
        rank = card['rank']
        filename = f"{rank}.png"
        path = os.path.join("assets", "cards", suit, filename)
        if os.path.exists(path):
            return Image(source=path, size_hint=(None, None), size=(71, 96))
        return None

    def draw_card(self, hand, grid):
        """Zieht eine Karte und zeigt sie an."""
        if self.deck.cards:
            # Für den Dealer: Falls noch keine Karte vorhanden, wird die erste normal gezeigt;
            # Falls es die 2. Karte ist und der Spieler noch nicht standet, wird sie verdeckt angezeigt.
            card = self.deck.draw_card()
            hand.append(card)
            if grid == self.dealer_grid and len(hand) == 2:
                # Zweite Karte des Dealers: verdeckt anzeigen
                back_path = os.path.join("assets", "cards", "cardback", "back.png")
                hidden_img = Image(source=back_path, size_hint=(None, None), size=(71, 96))
                grid.add_widget(hidden_img)
                # Speichere Referenz, um später aufzudecken
                self.dealer_hidden_img = hidden_img
            else:
                img = self.load_card_image(card)
                if img:
                    grid.add_widget(img)
            # Prüfe, ob Split möglich ist: Bei 2 Karten gleichen Rangs
            if len(self.player_hand) == 2 and self.player_hand[0]['rank'] == self.player_hand[1]['rank']:
                self.split_button.disabled = False
            else:
                self.split_button.disabled = True
            # Double Down nur, wenn genau 2 Karten und genügend Guthaben
            if len(self.player_hand) == 2 and self.betting.balance >= self.betting.current_bet:
                self.double_button.disabled = False
            else:
                self.double_button.disabled = True

    def calculate_score(self, hand):
        """Berechnet die Punktzahl einer Hand."""
        score = sum(card['value'] for card in hand)
        num_aces = sum(1 for card in hand if card['rank'] == 'Ass')
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score

    def set_bet(self, instance):
        try:
            bet = int(self.bet_entry.text)
            if self.betting.place_bet(bet):
                self.start_round()
                self.money_label.text = f"Guthaben: {self.betting.balance} Chips"
                self.save_credits_to_db()
                # Deaktiviere den Einsatzbereich
                self.bet_entry.disabled = True
                self.bet_button.disabled = True
                self.all_in_button.disabled = True
        except ValueError:
            pass

    def all_in(self, instance):
        """Setzt den gesamten aktuellen Kontostand als Einsatz."""
        all_in_amount = self.betting.balance
        if all_in_amount > 0 and self.betting.place_bet(all_in_amount):
            self.start_round()
            self.money_label.text = f"Guthaben: {self.betting.balance} Chips"
            self.save_credits_to_db()
            self.bet_entry.disabled = True
            self.bet_button.disabled = True
            self.all_in_button.disabled = True

    def start_round(self):
        """Startet eine neue Runde."""
        self.player_hand = []
        self.dealer_hand = []
        self.dealer_grid.clear_widgets()
        self.player_grid.clear_widgets()
        # Setze das Deck zurück (falls reset existiert, sonst neu instanziieren)
        if hasattr(self.deck, 'reset'):
            self.deck.reset()
        else:
            self.deck = Deck()

        # Karten austeilen: 2 für Spieler, 2 für Dealer (zweite Dealerkarte verdeckt)
        self.draw_card(self.player_hand, self.player_grid)
        self.draw_card(self.player_hand, self.player_grid)
        self.draw_card(self.dealer_hand, self.dealer_grid)
        self.draw_card(self.dealer_hand, self.dealer_grid)

        # Aktiviere Aktionen (außer Neue Runde)
        self.hit_button.disabled = False
        self.stand_button.disabled = False
        self.new_round_button.disabled = True
        # Double Down und Split werden in draw_card überprüft

    def hit(self, instance):
        """Spieler zieht eine Karte."""
        self.draw_card(self.player_hand, self.player_grid)
        if self.calculate_score(self.player_hand) > 21:
            self.end_round("Verloren: Über 21")

    def stand(self, instance):
        """Dealer zieht Karten; vorher wird die verdeckte Karte aufgedeckt."""
        # Aufdecken der verdeckten Dealerkarte
        if hasattr(self, 'dealer_hidden_img'):
            self.dealer_grid.remove_widget(self.dealer_hidden_img)
            actual_img = self.load_card_image(self.dealer_hand[1])
            self.dealer_grid.add_widget(actual_img, index=1)
            del self.dealer_hidden_img

        while self.calculate_score(self.dealer_hand) < 17:
            self.draw_card(self.dealer_hand, self.dealer_grid)
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        if player_score > 21:
            result = "Verloren: Über 21"
        elif dealer_score > 21 or player_score > dealer_score:
            result = f"Gewonnen: {player_score} vs. {dealer_score}"
            self.betting.win_bet()
        elif player_score == dealer_score:
            result = f"Push: Unentschieden bei {player_score}"
            self.betting.push_bet()
        else:
            result = f"Verloren: {player_score} vs. {dealer_score}"
        self.end_round(result)

    def double_down(self, instance):
        """Double Down: Verdoppelt den Einsatz, zieht eine Karte und endet die Runde."""
        if len(self.player_hand) == 2 and self.betting.balance >= self.betting.current_bet:
            additional_bet = self.betting.current_bet
            if self.betting.place_bet(additional_bet):
                self.money_label.text = f"Guthaben: {self.betting.balance} Chips"
                self.save_credits_to_db()
                self.draw_card(self.player_hand, self.player_grid)
                # Nach Double Down werden keine weiteren Aktionen zugelassen
                self.hit_button.disabled = True
                self.stand_button.disabled = True
                self.double_button.disabled = True
                self.split_button.disabled = True
                self.stand(None)  # Automatisches Stehen

    def split(self, instance):
        """Split: (Vereinfachte Version) Zeigt ein Popup, dass Split aktiviert wurde."""
        if len(self.player_hand) == 2 and self.player_hand[0]['rank'] == self.player_hand[1]['rank']:
            self.show_popup("Split", "Split-Funktion aktiviert (Implementierung folgt)")
            self.split_button.disabled = True

    def new_round(self, instance):
        """Startet manuell eine neue Runde und aktiviert den Einsatzbereich."""
        # Reaktiviere den Einsatzbereich
        self.bet_entry.disabled = False
        self.bet_button.disabled = False
        self.all_in_button.disabled = False
        self.bet_entry.text = ""
        self.start_round()

    def end_round(self, result):
        """Beendet die Runde, zeigt Ergebnis-Popup und aktiviert 'Neue Runde'."""
        self.hit_button.disabled = True
        self.stand_button.disabled = True
        self.double_button.disabled = True
        self.split_button.disabled = True
        self.new_round_button.disabled = False
        self.money_label.text = f"Guthaben: {self.betting.balance} Chips"
        self.save_credits_to_db()
        self.show_popup("Ergebnis", result)

    def save_credits_to_db(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE savefiles SET credits = %s WHERE username = %s", (self.betting.balance, self.username))
        conn.commit()
        conn.close()

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        popup_label = Label(text=message, font_size=18, color=(1, 1, 1, 1))
        popup_button = Button(text="OK", font_size=18, size_hint=(1, 0.3))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()


class BlackjackApp(App):
    def build(self):
        return BlackjackGame(username="Spieler")  # Ersetze "Spieler" durch den tatsächlichen Login-Namen


if __name__ == "__main__":
    BlackjackApp().run()
