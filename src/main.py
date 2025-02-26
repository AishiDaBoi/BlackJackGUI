import tkinter as tk
from src.auth import LoginWindow
from game.game import BlackjackGame
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window


class LoadingApp(App):
    def __init__(self, username, login_root, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.login_root = login_root

    def build(self):
        # Fenster maximieren und Hintergrundfarbe auf Grün setzen
        Window.maximize()
        Window.clearcolor = (0, 0.5, 0, 1)  # Grün (RGB: 0, 0.5, 0)

        self.layout = BoxLayout(orientation="vertical")
        self.label = Label(text="Loading...", font_size=24, color=(1, 1, 1, 1))  # Weißer Text
        self.progress = ProgressBar(max=100)

        self.layout.add_widget(self.label)
        self.layout.add_widget(self.progress)

        # Starte die Simulation eines Ladevorgangs
        Clock.schedule_interval(self.update_progress, 0.1)

        return self.layout

    def update_progress(self, dt):
        """Aktualisiert den Fortschrittsbalken."""
        if self.progress.value < 100:
            self.progress.value += 1
        else:
            # Stoppe die Simulation, wenn der Ladevorgang abgeschlossen ist
            Clock.unschedule(self.update_progress)
            self.label.text = "Loading complete!"

            # Spiel-Fenster öffnen
            self.open_game()

    def open_game(self):
        """Öffnet das Spiel-Fenster."""
        self.stop()  # Schließe das Kivy-Loading-Fenster
        self.login_root.destroy()  # Schließe das Login-Fenster

        # Spiel-Fenster öffnen
        game_root = tk.Tk()
        game_root.attributes("-fullscreen", True)  # Fenster im Fullscreen-Modus
        game_root.configure(bg="green")  # Hintergrundfarbe auf Grün setzen
        BlackjackGame(game_root, self.username)
        game_root.mainloop()

def open_game(username, login_root):
    # Starte die Kivy-Loading-Sequenz
    LoadingApp(username, login_root).run()


def start_login():
    root = tk.Tk()
    root.attributes("-fullscreen", True)  # Fenster im Fullscreen-Modus
    root.configure(bg="green")  # Hintergrundfarbe auf Grün setzen
    login_window = LoginWindow(root, open_game)
    root.mainloop()


if __name__ == "__main__":
    start_login()