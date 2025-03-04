import random
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, RoundedRectangle

# Mapping für Kartencodes -> Dateinamen
CARD_NAME_MAP = {
    '2C': '2_of_clubs.png', '2D': '2_of_diamonds.png', '2H': '2_of_hearts.png', '2S': '2_of_spades.png',
    '3C': '3_of_clubs.png', '3D': '3_of_diamonds.png', '3H': '3_of_hearts.png', '3S': '3_of_spades.png',
    '4C': '4_of_clubs.png', '4D': '4_of_diamonds.png', '4H': '4_of_hearts.png', '4S': '4_of_spades.png',
    '5C': '5_of_clubs.png', '5D': '5_of_diamonds.png', '5H': '5_of_hearts.png', '5S': '5_of_spades.png',
    '6C': '6_of_clubs.png', '6D': '6_of_diamonds.png', '6H': '6_of_hearts.png', '6S': '6_of_spades.png',
    '7C': '7_of_clubs.png', '7D': '7_of_diamonds.png', '7H': '7_of_hearts.png', '7S': '7_of_spades.png',
    '8C': '8_of_clubs.png', '8D': '8_of_diamonds.png', '8H': '8_of_hearts.png', '8S': '8_of_spades.png',
    '9C': '9_of_clubs.png', '9D': '9_of_diamonds.png', '9H': '9_of_hearts.png', '9S': '9_of_spades.png',
    '10C': '10_of_clubs.png', '10D': '10_of_diamonds.png', '10H': '10_of_hearts.png', '10S': '10_of_spades.png',
    'JC': 'jack_of_clubs.png', 'JD': 'jack_of_diamonds.png', 'JH': 'jack_of_hearts.png', 'JS': 'jack_of_spades.png',
    'QC': 'queen_of_clubs.png', 'QD': 'queen_of_diamonds.png', 'QH': 'queen_of_hearts.png', 'QS': 'queen_of_spades.png',
    'KC': 'king_of_clubs.png', 'KD': 'king_of_diamonds.png', 'KH': 'king_of_hearts.png', 'KS': 'king_of_spades.png',
    'AC': 'ace_of_clubs.png', 'AD': 'ace_of_diamonds.png', 'AH': 'ace_of_hearts.png', 'AS': 'ace_of_spades.png'
}

# Funktion zum Umwandeln des Kartencodes in den Dateinamen
def get_card_filename(card_code):
    return CARD_NAME_MAP.get(card_code, "back.png")  # Falls unbekannt, Rückseite anzeigen

# Liste aller Karten
DECK = list(CARD_NAME_MAP.keys())

class GreenBackground(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0, 0.5, 0, 1)  # Sattes Grün für den gesamten Hintergrund
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos


from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle


class CardArea(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(1, 1, 1, 1)  # Weißer Hintergrund
            self.border = RoundedRectangle(size=self.size, pos=self.pos, radius=[15])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.border.pos = self.pos
        self.border.size = self.size


class BlackjackApp(App):
    def build(self):
        self.deck = DECK.copy()  # Neues Deck erstellen
        random.shuffle(self.deck)  # Karten mischen
        self.cards = []  # Gespielte Karten

        # Hauptlayout mit grünem Hintergrund
        root = GreenBackground(orientation='vertical')

        # Kartenbereich mit weißem Hintergrund
        card_area_container = BoxLayout(size_hint=(1, 0.6), padding=10)  # 60% der Höhe nutzen
        self.card_area = CardArea(size_hint=(1, 1))
        card_area_container.add_widget(self.card_area)
        root.add_widget(card_area_container)

        # Karten-Layout (Innerhalb der weißen Ablage)
        self.card_layout = BoxLayout(size_hint=(1, 1), padding=20, spacing=10)
        self.card_area.add_widget(self.card_layout)

        # Button zum Ziehen neuer Karten
        self.draw_button = Button(text="Neue Karte ziehen", size_hint=(1, 0.2))
        self.draw_button.bind(on_press=self.draw_card)
        root.add_widget(self.draw_button)

        return root

    def draw_card(self, instance):
        if self.deck:
            new_card = self.deck.pop()  # Karte ziehen
            self.cards.append(new_card)

            # Bildpfad holen
            image_path = os.path.join("cards", get_card_filename(new_card))
            print(f"Lade Bild: {image_path}")  # Debug-Ausgabe

            # Bild hinzufügen
            card_image = Image(source=image_path, size_hint=(None, None), size=(100, 150))
            self.card_layout.add_widget(card_image)
        else:
            self.draw_button.text = "Keine Karten mehr!"

if __name__ == '__main__':
    BlackjackApp().run()
