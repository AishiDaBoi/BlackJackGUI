from kivy.core.audio import SoundLoader

class SoundManager:
    def __init__(self):
        self.background_music = None
        self.click_sound = None
        self.win_sound = None
        self.lose_sound = None
        self.popup_sound = None
        self.load_sounds()

    def load_sounds(self):
        # Passe die Pfade an dein Projektverzeichnis an
        self.background_music = SoundLoader.load("assets/sounds/background.mp3")
        self.click_sound = SoundLoader.load("assets/sounds/click.mp3")
        self.win_sound = SoundLoader.load("assets/sounds/win.mp3")
        self.lose_sound = SoundLoader.load("assets/sounds/lose.mp3")
        self.popup_sound = SoundLoader.load("assets/sounds/popup.mp3")

    def play_background(self):
        if self.background_music:
            self.background_music.loop = True  # Endlosschleife
            self.background_music.play()

    def stop_background(self):
        if self.background_music:
            self.background_music.stop()

    def play_click(self):
        if self.click_sound:
            self.click_sound.play()

    def play_win(self):
        if self.win_sound:
            self.win_sound.play()

    def play_lose(self):
        if self.lose_sound:
            self.lose_sound.play()

    def play_popup(self):
        if self.popup_sound:
            self.popup_sound.play()

# Erstelle eine globale Instanz für einfachen Zugriff
sound_manager = SoundManager()
