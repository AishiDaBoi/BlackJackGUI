from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle
from src.auth.auth import login_user, register_user
from src.auth.loginViaJson import login_user_json, register_user_json

class LoginWindow(Screen):
    def __init__(self, on_success, **kwargs):
        super().__init__(**kwargs)
        self.on_success = on_success
        self.use_json = False

        # Hauptlayout
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.layout.bind(size=self._update_background)

        # Hintergrundfarbe
        with self.layout.canvas.before:
            Color(0, 0.5, 0, 1)  # Dunkelgrün
            self.background = Rectangle(pos=self.layout.pos, size=self.layout.size)

        # Titel
        self.layout.add_widget(Label(text="Willkommen bei Blackjack", font_size=26, bold=True, color=(1, 1, 1, 1)))

        # Eingabefelder
        self.entry_username = self.create_input_field("Benutzername:")
        self.entry_password = self.create_input_field("Passwort:", password=True)

        # JSON-Checkbox
        self.json_checkbox = self.create_checkbox("JSON statt MySQL nutzen", self.on_json_checkbox_active)

        # Standard-Benutzer-Button
        self.default_user_button = Button(text="Standard-Benutzer verwenden", font_size=16, size_hint=(1, 0.2))
        self.default_user_button.bind(on_press=self.use_default_user)
        self.layout.add_widget(self.default_user_button)

        # Buttons (Login & Registrierung)
        self.layout.add_widget(self.create_button("Login", self.login))
        self.layout.add_widget(self.create_button("Registrieren", self.register))

        self.add_widget(self.layout)

    def create_input_field(self, label_text, password=False):
        """Erstellt ein Label und ein Eingabefeld."""
        box = BoxLayout(orientation='vertical', size_hint=(1, 0.2), spacing=5)
        box.add_widget(Label(text=label_text, font_size=18, color=(1, 1, 1, 1)))
        input_field = TextInput(hint_text=label_text, font_size=18, password=password)
        box.add_widget(input_field)
        self.layout.add_widget(box)
        return input_field

    def create_checkbox(self, label_text, callback):
        """Erstellt eine Checkbox mit Label."""
        box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        label = Label(text=label_text, font_size=14, color=(1, 1, 1, 1))
        checkbox = CheckBox(size_hint=(0.2, 1))
        checkbox.bind(active=callback)
        box.add_widget(label)
        box.add_widget(checkbox)
        self.layout.add_widget(box)
        return checkbox

    def create_button(self, text, callback):
        """Erstellt einen Button mit einer Aktion."""
        button = Button(text=text, font_size=18, size_hint=(1, 0.2))
        button.bind(on_press=callback)
        return button

    def _update_background(self, instance, value):
        """Aktualisiert die Hintergrundgröße."""
        self.background.pos = instance.pos
        self.background.size = instance.size

    def on_json_checkbox_active(self, instance, value):
        """Schaltet zwischen JSON- und MySQL-Login um."""
        self.use_json = value

    def use_default_user(self, instance):
        """Setzt Standard-Benutzerdaten ein."""
        self.entry_username.text = "TestUser"
        self.entry_password.text = "1234"

    def login(self, instance):
        """Überprüft die Anmeldedaten und öffnet das Spiel."""
        username, password = self.entry_username.text.strip(), self.entry_password.text.strip()
        if not username or not password:
            self.show_popup("Fehler", "Bitte beide Felder ausfüllen!")
            return

        login_func = login_user_json if self.use_json else login_user
        if login_func(username, password):
            self.show_popup("Erfolg", "Login erfolgreich!")
            self.on_success(username)
        else:
            self.show_popup("Fehler", "Falsche Anmeldeinformationen!")

    def register(self, instance):
        """Registriert einen neuen Benutzer."""
        username, password = self.entry_username.text.strip(), self.entry_password.text.strip()
        if not username or not password:
            self.show_popup("Fehler", "Bitte beide Felder ausfüllen!")
            return

        register_func = register_user_json if self.use_json else register_user
        if register_func(username, password):
            self.show_popup("Erfolg", "Registrierung erfolgreich! Bitte einloggen.")
        else:
            self.show_popup("Fehler", "Benutzername bereits vergeben!")

    def show_popup(self, title, message):
        """Zeigt eine Popup-Nachricht an."""
        popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        popup_label = Label(text=message, font_size=18, color=(1, 1, 1, 1))
        popup_button = Button(text="OK", font_size=18, size_hint=(1, 0.3))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()
