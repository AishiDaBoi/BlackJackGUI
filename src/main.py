from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from auth import LoginWindow, login_user
from game import BlackjackGame


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.login_window = LoginWindow(self.open_game)
        self.add_widget(self.login_window)  # <---- Hier wird das Login-Fenster sichtbar


    def open_game(self, username):
        self.manager.current = 'game'
        self.manager.get_screen('game').start_game(username)


class GameScreen(Screen):
    def start_game(self, username):
        self.clear_widgets()
        self.game = BlackjackGame(username)
        self.add_widget(self.game)


class BlackjackApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(GameScreen(name='game'))
        return sm


if __name__ == "__main__":
    BlackjackApp().run()
