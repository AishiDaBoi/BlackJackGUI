from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.slider import Slider
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
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
        self.background_music = SoundLoader.load("assets/sounds/background.mp3")
        self.click_sound = SoundLoader.load("assets/sounds/click.mp3")
        self.win_sound = SoundLoader.load("assets/sounds/win.mp3")
        self.lose_sound = SoundLoader.load("assets/sounds/lose.mp3")
        self.popup_sound = SoundLoader.load("assets/sounds/popup.mp3")

    def play_background(self):
        if self.background_music:
            self.background_music.loop = True
            self.background_music.volume = 0.2
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


sound_manager = SoundManager()


class RecycleViewButton(RecycleDataViewBehavior, ButtonBehavior, Label):
    """Button für die Musikliste, klickbar für Auswahl"""

    index = None

    def on_press(self):
        self.parent.parent.parent.select_music(self.text)


class MusicListView(RecycleView):
    def __init__(self, music_window, **kwargs):
        super().__init__(**kwargs)
        self.music_window = music_window
        self.data = [{"text": song} for song in self.music_window.preinstalled_files]

    def add_music(self, file_path):
        self.data.append({"text": file_path})

    def select_music(self, selected_file):
        sound_manager.stop_background()
        sound_manager.background_music = SoundLoader.load(selected_file)
        if sound_manager.background_music:
            sound_manager.play_background()


class MusicChangerWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.preinstalled_files = [
            "assets/sounds/background.mp3",
            "assets/sounds/alternative.mp3",
        ]
        self.custom_files = []
        self.current_file = None

        self.file_chooser = FileChooserListView(filters=["*.mp3", "*.wav"])
        self.file_chooser.bind(on_selection=self.on_file_selected)
        self.add_widget(self.file_chooser)

        self.upload_button = Button(text="Upload", size_hint=(1, 0.1))
        self.upload_button.bind(on_press=self.upload_file)
        self.add_widget(self.upload_button)

        self.volume_slider = Slider(min=0, max=1, value=0.2, size_hint=(1, 0.1))
        self.volume_slider.bind(value=self.on_volume_change)
        self.add_widget(self.volume_slider)

        self.music_list = MusicListView(self)
        self.add_widget(self.music_list)

    def on_file_selected(self, filechooser, selection):
        if selection:
            self.current_file = selection[0]

    def upload_file(self, instance):
        if self.current_file:
            self.custom_files.append(self.current_file)
            self.music_list.add_music(self.current_file)

    def on_volume_change(self, instance, value):
        if sound_manager.background_music:
            sound_manager.background_music.volume = value


sound_manager = SoundManager()
