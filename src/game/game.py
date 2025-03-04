from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
import os

from src.game.deck import Deck
from src.game.betting import BettingSystem


class BlackjackGame(BoxLayout):
    def __init__(self, username, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.deck = Deck()
        self.betting = BettingSystem(1000)
        self.player_hand = []
        self.dealer_hand = []

        self.orientation = 'vertical'
        self.setup_gui()

    def setup_gui(self):
        # Spielername und Guthaben
        self.add_widget(Label(text=f"Spieler: {self.username}", font_size=24))
        self.money_label = Label(text=f"Guthaben: {self.betting.balance} Chips", font_size=18)
        self.add_widget(self.money_label)

        # Dealer-Bereich
        self.add_widget(Label(text="Dealer", font_size=18))
        self.dealer_grid = GridLayout(cols=5, size_hint_y=None, height=100)
        self.add_widget(self.dealer_grid)

        # Spieler-Bereich
        self.add_widget(Label(text="Spieler", font_size=18))
        self.player_grid = GridLayout(cols=5, size_hint_y=None, height=100)
        self.add_widget(self.player_grid)

        # Steuerelemente
        self.controls = BoxLayout(size_hint=(1, 0.1))
        self.bet_entry = TextInput(hint_text="Einsatz", font_size=18, size_hint=(0.3, 1))
        self.controls.add_widget(self.bet_entry)
        self.controls.add_widget(Button(text="Einsatz setzen", font_size=18, on_press=self.set_bet))
        self.hit_button = Button(text="Hit", font_size=18, on_press=self.hit, disabled=True)
        self.controls.add_widget(self.hit_button)
        self.stand_button = Button(text="Stand", font_size=18, on_press=self.stand, disabled=True)
        self.controls.add_widget(self.stand_button)
        self.add_widget(self.controls)

    def load_card_image(self, card):
        """Lädt das Kartenbild."""
        path = os.path.join("assets", "cards", card['suit'], f"{card['rank']}.png")
        if os.path.exists(path):
            return Image(source=path, size_hint=(None, None), size=(71, 96))
        return None

    def draw_card(self, hand, grid):
        """Zeichnet eine Karte im Grid."""
        if self.deck.cards:
            card = self.deck.draw_card()
            hand.append(card)
            img = self.load_card_image(card)
            if img:
                grid.add_widget(img)

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
        except ValueError:
            pass

    def start_round(self):
        """Startet eine neue Runde."""
        self.player_hand = []
        self.dealer_hand = []
        self.dealer_grid.clear_widgets()
        self.player_grid.clear_widgets()

        self.draw_card(self.player_hand, self.player_grid)
        self.draw_card(self.player_hand, self.player_grid)
        self.draw_card(self.dealer_hand, self.dealer_grid)
        self.draw_card(self.dealer_hand, self.dealer_grid)

        self.hit_button.disabled = False
        self.stand_button.disabled = False

    def hit(self, instance):
        """Spieler zieht eine Karte."""
        self.draw_card(self.player_hand, self.player_grid)
        if self.calculate_score(self.player_hand) > 21:
            self.money_label.text = "Spieler hat über 21! Dealer gewinnt."
            self.hit_button.disabled = True
            self.stand_button.disabled = True

    def stand(self, instance):
        """Dealer zieht Karten."""
        while self.calculate_score(self.dealer_hand) < 17:
            self.draw_card(self.dealer_hand, self.dealer_grid)
        self.money_label.text = "Runde beendet!"

class BlackjackApp(App):
    def build(self):
        return BlackjackGame(username="Spieler")

if __name__ == "__main__":
    BlackjackApp().run()
