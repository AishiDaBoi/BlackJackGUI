import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock

from src.game.deck import Deck
from src.game.betting import BettingSystem
from src.auth.database import get_db_connection  # MySQL connection
from src.game.sounds import sound_manager
import logging

logging.basicConfig(
    filename='Logging.log',
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    level=logging.INFO
)

class BlackjackGame(BoxLayout):
    def __init__(self, username, **kwargs):
        super().__init__(**kwargs)
        # Store the username and load the player's credits from the database
        self.username = username
        self.credits = self.load_credits_from_db(username)
        # Initialize the deck and betting system with the loaded credits
        self.deck = Deck()
        self.betting = BettingSystem(self.credits)
        self.player_hand = []  # List to store player's cards
        self.dealer_hand = []  # List to store dealer's cards
        self.split_mode = False  # For future split logic

        # Bind the window close event to the on_close method
        Window.bind(on_request_close=self.on_close)

        # Set layout properties
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        # Set background (dark green) using a canvas rectangle
        with self.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0, 0.2, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Build the UI
        self.setup_gui()

    def update_rect(self, *args):
        """Updates the background rectangle when the window resizes."""
        self.rect.pos = self.pos
        self.rect.size = self.size

    def load_credits_from_db(self, username):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT credits FROM users WHERE username = ?",
                (username,)
            )
            result = cursor.fetchone()
            return result['credits'] if result else 1000
        finally:
            conn.close()

    def save_credits_to_db(self):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET credits = ? WHERE username = ?",
                (self.betting.balance, self.username)
            )
            conn.commit()
        finally:
            conn.close()


    def setup_gui(self):
        """Initializes the graphical user interface."""
        # Header: Display player's name and balance (always visible)
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)
        header.add_widget(Label(text=f"Player: {self.username}", font_size=24, color=(1, 1, 1, 1)))
        self.money_label = Label(text=f"Balance: {self.betting.balance} Chips", font_size=18, color=(1, 1, 1, 1))
        header.add_widget(self.money_label)
        self.add_widget(header)

        # Dealer area: Section to display dealer's cards
        dealer_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), padding=10, spacing=5)
        dealer_layout.add_widget(Label(text="Dealer", font_size=18, color=(1, 1, 1, 1)))
        self.dealer_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=150)
        dealer_layout.add_widget(self.dealer_grid)
        self.add_widget(dealer_layout)

        # Player area: Section to display player's cards
        player_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.3), padding=10, spacing=5)
        player_layout.add_widget(Label(text="Player", font_size=18, color=(1, 1, 1, 1)))
        self.player_grid = GridLayout(cols=5, spacing=5, size_hint_y=None, height=150)
        player_layout.add_widget(self.player_grid)
        self.add_widget(player_layout)

        # Betting input: Allows player to enter a bet and choose "All-In"
        bet_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10, spacing=10)
        self.bet_entry = TextInput(hint_text="Bet Amount", font_size=18, multiline=False, size_hint=(0.3, 1))
        bet_layout.add_widget(self.bet_entry)
        self.bet_button = Button(text="Place Bet", font_size=18, size_hint=(0.3, 1))
        self.bet_button.bind(on_press=self.set_bet)
        bet_layout.add_widget(self.bet_button)
        self.all_in_button = Button(text="All-In", font_size=18, size_hint=(0.3, 1))
        self.all_in_button.bind(on_press=self.all_in)
        bet_layout.add_widget(self.all_in_button)
        self.add_widget(bet_layout)

        # Action buttons: Hit, Stand, Double Down, Split, New Round
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

        self.new_round_button = Button(text="New Round", font_size=18, size_hint=(0.2, 1), disabled=True)
        self.new_round_button.bind(on_press=self.new_round)
        action_layout.add_widget(self.new_round_button)

        logger = logging.getLogger(__name__)
        logger.info("BlackjackGame created")

        self.add_widget(action_layout)

    def load_card_image(self, card):
        """Loads the corresponding card image based on card suit and rank."""
        suit_translation = {"Hearts": "Hearts", "Diamonds": "Diamonds", "Spades": "Spades", "Clubs": "Clubs"}
        suit = suit_translation.get(card['suit'], card['suit'])
        rank = card['rank']
        filename = f"{rank}.png"
        path = os.path.join("assets", "cards", suit, filename)
        if os.path.exists(path):
            logger = logging.getLogger(__name__)
            logger.info(f"Card image loaded: {path}")
            return Image(source=path, size_hint=(None, None), size=(71, 96))
        return None

    def draw_card(self, hand, grid):
        """Draws a card from the deck, adds it to the specified hand, and displays it in the grid."""
        if self.deck.cards:
            card = self.deck.draw_card()
            hand.append(card)
            img = self.load_card_image(card)
            if img:
                grid.add_widget(img)

    def calculate_score(self, hand):
        """Calculates the score of a hand of cards."""
        # Sum up the value of all cards in the hand
        score = sum(card['value'] for card in hand)
        # Count the number of aces in the hand (represented as 'Ass' in the original data)
        num_aces = sum(1 for card in hand if card['rank'] == 'Ass')
        # Adjust score if score exceeds 21 and there are aces to adjust
        while score > 21 and num_aces:
            score -= 10
            num_aces -= 1
        return score

    def set_bet(self, instance):
        """Handles bet placement by the player."""
        sound_manager.play_click()
        try:
            bet = int(self.bet_entry.text)
            # If the bet is successfully placed, start the round
            if self.betting.place_bet(bet):
                self.start_round()
                self.money_label.text = f"Balance: {self.betting.balance} Chips"
                # Disable bet input area as bet has been set
                self.bet_entry.disabled = True
                self.bet_button.disabled = True
                self.all_in_button.disabled = True
        except ValueError:
            # If input is not a valid integer, ignore the bet
            pass

    def all_in(self, instance):
        """Places an all-in bet with the player's current balance."""
        sound_manager.play_click()
        all_in_amount = self.betting.balance
        if all_in_amount > 0 and self.betting.place_bet(all_in_amount):
            self.start_round()
            self.money_label.text = f"Balance: {self.betting.balance} Chips"
            self.bet_entry.disabled = True
            self.bet_button.disabled = True
            self.all_in_button.disabled = True

    def start_round(self):
        """Starts a new round by dealing cards to both player and dealer."""
        sound_manager.play_click()
        # Reset both hands
        self.player_hand = []
        self.dealer_hand = []
        # Clear card display areas
        self.dealer_grid.clear_widgets()
        self.player_grid.clear_widgets()
        # Reset the deck if possible, otherwise instantiate a new deck
        if hasattr(self.deck, 'reset'):
            self.deck.reset()
        else:
            self.deck = Deck()
        # Deal two cards to player and dealer; dealer's second card remains hidden initially
        self.draw_card(self.player_hand, self.player_grid)
        self.draw_card(self.player_hand, self.player_grid)
        self.draw_card(self.dealer_hand, self.dealer_grid)
        self.draw_hidden_card(self.dealer_hand, self.dealer_grid)
        # Enable action buttons for the round (except New Round, which remains disabled until round end)
        self.hit_button.disabled = False
        self.stand_button.disabled = False
        self.double_button.disabled = False
        logger = logging.getLogger(__name__)
        logger.info("New round started")


    def draw_hidden_card(self, hand, grid):
        """Draws a hidden card for the dealer."""
        card = self.deck.draw_card()
        hand.append(card)
        img = Image(source="assets/cards/cardback/back.png", size_hint=(None, None), size=(71, 96))
        self.dealer_hidden_img = img
        grid.add_widget(img)


    def hit(self, instance):
        logger = logging.getLogger(__name__)
        logger.info("Player hits")
        """Processes the player's action to draw a card."""
        sound_manager.play_click()
        self.draw_card(self.player_hand, self.player_grid)
        # If the player's score exceeds 21, end the round immediately
        if self.calculate_score(self.player_hand) > 21:
            self.end_round("Lost: Over 21")
        elif self.calculate_score(self.player_hand) == 21:
            self.stand(None)


    def stand(self, instance):
        logger = logging.getLogger(__name__)
        logger.info("Player stands")
        """Processes the stand action: reveals the dealer's hidden card and plays out the dealer's hand."""
        sound_manager.play_click()
        # Reveal the dealer's hidden card if applicable
        if hasattr(self, 'dealer_hidden_img'):
            self.dealer_grid.remove_widget(self.dealer_hidden_img)
            actual_img = self.load_card_image(self.dealer_hand[1])
            self.dealer_grid.add_widget(actual_img, index=1)
            del self.dealer_hidden_img
        # Dealer draws cards until reaching a minimum score of 17
        while self.calculate_score(self.dealer_hand) < 17:
            self.draw_card(self.dealer_hand, self.dealer_grid)
        player_score = self.calculate_score(self.player_hand)
        dealer_score = self.calculate_score(self.dealer_hand)
        # Determine outcome based on scores
        if player_score > 21:
            result = "Lost: Over 21"
        elif dealer_score > 21 or player_score > dealer_score:
            result = f"Won: {player_score} vs. {dealer_score}"
            self.betting.win_bet()
        elif player_score == dealer_score:
            result = f"Push: Tied at {player_score}"
            self.betting.push_bet()
        else:
            result = f"Lost: {player_score} vs. {dealer_score}"
        self.end_round(result)

    def double_down(self, instance):
        """Double Down: doubles the bet, draws one card, and then automatically ends the round."""
        sound_manager.play_click()

        if len(self.player_hand) > 2:
            self.show_popup("Double Down", "Double Down is only allowed with 2 cards.")
            self.double_button.disabled = True
        else:

            if len(self.player_hand) == 2 and self.betting.balance >= self.betting.current_bet:
                additional_bet = self.betting.current_bet
                if self.betting.place_bet(additional_bet):
                    self.money_label.text = f"Balance: {self.betting.balance} Chips"
                    self.draw_card(self.player_hand, self.player_grid)
                    # After doubling down, disable further actions and force stand
                    self.hit_button.disabled = True
                    self.stand_button.disabled = True
                    self.double_button.disabled = True
                    self.split_button.disabled = True
                    self.stand(None)  # Automatically execute stand

    def split(self, instance):
        """Split: (Simplified) Shows a popup indicating that the split function is activated."""
        sound_manager.play_click()
        if len(self.player_hand) == 2 and self.player_hand[0]['rank'] == self.player_hand[1]['rank']:
            self.show_popup("Split", "Split function activated (implementation pending)")
            self.split_button.disabled = True

    def new_round(self, instance):
        """Prepares the UI for a new round and disables the 'New Round' button until the round ends.
        Clears card display areas so that cards are only visible after a new bet is placed."""
        # Disable the New Round button to prevent multiple rounds from starting concurrently
        self.new_round_button.disabled = True
        # Clear card display areas
        self.dealer_grid.clear_widgets()
        self.player_grid.clear_widgets()
        # Re-enable the bet input area for a new bet
        self.bet_entry.disabled = False
        self.bet_button.disabled = False
        self.all_in_button.disabled = False
        self.bet_entry.text = ""
        # Reset the current bet value
        self.betting.current_bet = 0

    def end_round(self, result):
        """Ends the round by displaying the result popup and enabling the 'New Round' button."""
        self.hit_button.disabled = True
        self.stand_button.disabled = True
        self.double_button.disabled = True
        self.split_button.disabled = True
        self.new_round_button.disabled = False
        self.money_label.text = f"Balance: {self.betting.balance} Chips"
        # Reset the current bet value
        self.betting.current_bet = 0
        self.show_popup("Result", result)

    def show_popup(self, title, message):
        """Creates and displays a popup with the given title and message."""
        popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        popup_label = Label(text=message, font_size=18, color=(1, 1, 1, 1))
        popup_button = Button(text="OK", font_size=18, size_hint=(1, 0.3))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        sound_manager.play_popup()
        popup.open()

    def on_close(self, *args):
        """Called when the user closes the window via the title bar.
        Displays a loading popup, saves credits in the background, then shows a confirmation popup."""
        # Create a loading popup indicating that saving is in progress
        loading_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        loading_label = Label(text="Saving in progress...", font_size=18, color=(1, 1, 1, 1))
        loading_layout.add_widget(loading_label)
        self.loading_popup = Popup(title="Please Wait", content=loading_layout, size_hint=(0.6, 0.3),
                                   auto_dismiss=False)
        self.loading_popup.open()
        # Schedule the save_and_exit function to run after a short delay (to prevent UI freezing)
        Clock.schedule_once(self.save_and_exit, 1.5)
        return True  # Prevent the window from closing immediately

    def save_and_exit(self, dt):
        """Saves credits to the database and then displays a confirmation popup before closing the app."""
        try:
            self.save_credits_to_db()
            print("Credits successfully saved!")  # Debug output
        except Exception as e:
            print(f"Error saving credits: {e}")
            self.loading_popup.dismiss()
            self.show_popup("Error", "Saving failed. Please try again.")
            return
        # Dismiss the loading popup
        self.loading_popup.dismiss()
        # Create a confirmation popup informing the user that credits are saved and the app will close
        popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        popup_label = Label(text="Credits saved! The game will now close.", font_size=18, color=(1, 1, 1, 1))
        popup_button = Button(text="OK", font_size=18, size_hint=(1, 0.3))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)
        confirm_popup = Popup(title="Saving Complete", content=popup_layout, size_hint=(0.8, 0.4), auto_dismiss=False)

        def close_app(instance):
            confirm_popup.dismiss()
            App.get_running_app().stop()

        popup_button.bind(on_press=close_app)
        confirm_popup.open()


class BlackjackApp(App):
    def build(self):
        # Replace "Player" with the actual login name if needed
        return BlackjackGame(username="Player")


if __name__ == "__main__":
    BlackjackApp().run()
