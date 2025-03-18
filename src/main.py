from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from auth import LoginWindow, login_user
from game import BlackjackGame
from game.sounds import MusicChangerWindow
import logging


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_window = LoginWindow(self.open_game)
        self.add_widget(self.login_window)  # <---- Hier wird das Login-Fenster sichtbar
        logger = logging.getLogger(__name__)
        logger.info("LoginScreen created")

    def open_game(self, username):
        self.manager.current = 'game'
        self.manager.get_screen('game').start_game(username)
        logger = logging.getLogger(__name__)
        logger.info(f"User {username} logged in")

class GameScreen(Screen):
    def start_game(self, username):
        self.clear_widgets()
        self.game = BlackjackGame(username)
        self.add_widget(self.game)
        logger = logging.getLogger(__name__)
        logger.info("GameScreen created")

class MusicChangerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MusicChangerWindow())
        logger = logging.getLogger(__name__)
        logger.info("MusicChangerScreen created")


class BlackjackApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(GameScreen(name='game'))
        logger = logging.getLogger(__name__)
        logger.info("Screens added")
        return sm


if __name__ == "__main__":
    BlackjackApp().run()
