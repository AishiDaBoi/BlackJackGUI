from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup


def show_popup(self, title, message):
    """Creates and displays a popup with the given title and message."""
    popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
    popup_label = Label(text=message, font_size=18, color=(1, 1, 1, 1))
    popup_button = Button(text="OK", font_size=18, size_hint=(1, 0.3))
    popup_layout.add_widget(popup_label)
    popup_layout.add_widget(popup_button)
    popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
    popup_button.bind(on_press=popup.dismiss)
    # sound_manager.play_popup()
    popup.open()


class BettingSystem:
    def __init__(self, balance):
        """Initialisiert das Wettsystem mit einem Startguthaben."""
        self.balance = balance
        self.current_bet = 0

    def place_bet(self, amount):

        if amount > self.balance:
            show_popup(self, "Error", "Not enough credits! Max bet is " + str(self.balance) + " credits.")


        """Setzt einen Einsatz."""
        if amount > 0 and amount <= self.balance:
            self.current_bet = amount
            self.balance -= amount
            return True
        return False

    def win_bet(self):
        """Spieler gewinnt die Runde (2:1 Auszahlung)."""
        self.balance += self.current_bet * 2

    def push_bet(self):
        """Unentschieden: Einsatz wird zurückgegeben."""
        self.balance += self.current_bet

