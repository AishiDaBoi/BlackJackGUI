import logging

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.progressbar import ProgressBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

# Import authentication functions (for MySQL and JSON-based login/registration)
from src.auth.auth import login_user, register_user
from src.auth.loginViaJson import login_user_json, register_user_json
from src.game.sounds import sound_manager

from src.game.sounds import MusicChangerWindow


class LoginWindow(Screen):
    def __init__(self, on_success, **kwargs):
        super().__init__(**kwargs)
        # Callback for successful login
        self.on_success = on_success
        # Flag to toggle between JSON and MySQL login methods
        self.use_json = False
        # Start playing background music
        sound_manager.play_background()

        # Create a centered main layout with fixed size
        self.layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15,
            size_hint=(None, None),
            width=400,
            height=500,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        # Bind layout size changes to update background
        self.layout.bind(size=self._update_background)

        # Set a background color for the entire screen
        with self.canvas.before:
            self.bg_color = Color(0, 0.5, 0, 1)  # Dark green
            self.background = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_background, pos=self._update_background)

        # Title label
        self.layout.add_widget(Label(
            text="Welcome to Blackjack",
            font_size=26,
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40
        ))

        # Create input fields for username and password
        username_box, self.entry_username = self.create_input_field("Username:")
        password_box, self.entry_password = self.create_input_field("Password:", password=True)
        self.layout.add_widget(username_box)
        self.layout.add_widget(password_box)

        # Bind text changes to check if both fields are filled
        self.entry_username.bind(text=self.check_text_fields)
        self.entry_password.bind(text=self.check_text_fields)

        # Add a checkbox to choose JSON-based login instead of MySQL
        self.layout.add_widget(self.create_checkbox("Use JSON instead of MySQL", self.on_json_checkbox_active))

        # Button to use default user credentials
        self.default_user_button = Button(
            text="Use Default User",
            font_size=16,
            size_hint=(0.8, None),
            height=50
        )
        self.default_user_button.bind(on_press=self.use_default_user)
        self.layout.add_widget(self.default_user_button)

        # Create Login & Register buttons with hover effects.
        # Initially, both buttons are disabled and gray.
        self.login_button = self.create_button("Login", self.login)
        self.register_button = self.create_button("Register", self.register)
        self.openMusicChanger_button = self.create_button("Music Changer", self.openMusicChanger)
        self.login_button.disabled = True
        self.register_button.disabled = True
        self.openMusicChanger_button.disabled = True
        self.login_button.background_color = (0.5, 0.5, 0.5, 1)
        self.register_button.background_color = (0.5, 0.5, 0.5, 1)
        self.openMusicChanger_button.background_color = (0.5, 0.5, 0.5, 1)
        self.layout.add_widget(self.login_button)
        self.layout.add_widget(self.register_button)
        self.layout.add_widget(self.openMusicChanger_button)

        # Add the main layout to the screen
        self.add_widget(self.layout)

        # Create a loading overlay that centers its content (ProgressBar and Label)
        self.loading_overlay = AnchorLayout(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            opacity=0  # Initially hidden
        )
        # Layout for the loading overlay
        loading_box = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=20,
            size_hint=(None, None),
            width=300,
            height=150
        )
        self.loading_label = Label(
            text="Loading...",
            font_size=24,
            color=(1, 1, 1, 1),
            size_hint=(1, None),
            height=50
        )
        self.progress_bar = ProgressBar(max=100, value=0, size_hint=(1, None), height=30)
        loading_box.add_widget(self.loading_label)
        loading_box.add_widget(self.progress_bar)
        self.loading_overlay.add_widget(loading_box)
        self.add_widget(self.loading_overlay)

        # Enable hover handling on the window for button hover effects
        Window.bind(mouse_pos=self.on_hover)

    def _update_background(self, instance, value):
        """Updates the background size and position when the screen changes."""
        self.background.pos = self.pos
        self.background.size = self.size

    def create_input_field(self, label_text, password=False):
        """Creates a centered input field with a label."""
        box = BoxLayout(orientation='vertical', size_hint=(1, None), height=80, spacing=5)
        label = Label(text=label_text, font_size=18, color=(1, 1, 1, 1), size_hint_y=None, height=30)
        input_field = TextInput(
            hint_text=label_text,
            font_size=18,
            password=password,
            size_hint=(1, None),
            height=50
        )
        box.add_widget(label)
        box.add_widget(input_field)
        return box, input_field

    def create_checkbox(self, label_text, callback):
        """Creates a checkbox with an associated label."""
        box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, spacing=10)
        label = Label(text=label_text, font_size=14, color=(1, 1, 1, 1), size_hint_x=0.8)
        checkbox = CheckBox(size_hint_x=0.2)
        checkbox.bind(active=callback)
        box.add_widget(label)
        box.add_widget(checkbox)
        return box

    def create_button(self, text, callback):
        """Creates a button with a hover effect."""
        button = Button(
            text=text,
            font_size=18,
            size_hint=(0.8, None),
            height=50,
            background_color=(0, 0.7, 0, 1)  # Default green (used when active)
        )
        button.bind(on_press=callback)
        button.hovered = False  # For tracking hover state
        return button

    def use_default_user(self, instance):
        """Sets default user credentials."""
        sound_manager.play_click()
        self.entry_username.text = "Test User"
        self.entry_password.text = "1234"

    def on_json_checkbox_active(self, instance, value):
        """Toggles between JSON and MySQL login methods."""
        self.use_json = value

    def on_hover(self, window, pos):
        """Changes the button color on hover."""
        for button in [self.login_button, self.register_button]:
            # Convert window coordinates to widget coordinates
            if button.collide_point(*button.to_widget(*pos)):
                if not button.hovered:
                    button.hovered = True
                    # If both input fields are filled, set button color to bright green
                    button.background_color = (0, 1, 0, 1)
            else:
                if button.hovered:
                    button.hovered = False
                    # Reset button state based on text fields
                    self.check_text_fields(None, None)

    def check_text_fields(self, instance, value):
        """Checks whether both text fields are filled and adjusts button states."""
        username_filled = bool(self.entry_username.text.strip())
        password_filled = bool(self.entry_password.text.strip())
        if username_filled and password_filled:
            self.login_button.disabled = False
            self.register_button.disabled = False
            # Set active color (default green)
            self.login_button.background_color = (0, 0.7, 0, 1)
            self.register_button.background_color = (0, 0.7, 0, 1)
        else:
            self.login_button.disabled = True
            self.register_button.disabled = True
            # Set disabled color (gray)
            self.login_button.background_color = (0.5, 0.5, 0.5, 1)
            self.register_button.background_color = (0.5, 0.5, 0.5, 1)

    def show_loading_overlay(self, text):
        """Displays the loading overlay with a progress bar and hides the login area."""
        self.loading_label.text = text
        self.progress_bar.value = 0
        self.loading_overlay.opacity = 1
        self.layout.opacity = 0
        self.loading_event = Clock.schedule_interval(self.update_progress, 0.1)

    def update_progress(self, dt):
        """Updates the progress bar value."""
        if self.progress_bar.value < 100:
            self.progress_bar.value += 5
        else:
            Clock.unschedule(self.loading_event)
            self.hide_loading_overlay()

    def hide_loading_overlay(self):
        """Hides the loading overlay and shows the login area again."""
        self.loading_overlay.opacity = 0
        self.layout.opacity = 1

    def openMusicChanger(self, instance):
        sound_manager.play_click()
        logger = logging.getLogger(__name__)
        logger.info("Music Changer opened")
        self.add_widget(MusicChangerWindow())

    def login(self, instance):
        """Starts the login process with a loading animation."""
        sound_manager.play_click()
        username = self.entry_username.text.strip()
        password = self.entry_password.text.strip()
        if not username or not password:
            self.show_popup("Error", "Please fill in both fields!")
            return

        # Choose the login function based on the checkbox setting
        login_func = login_user_json if self.use_json else login_user
        self.show_loading_overlay("Loading...")
        # Simulate a login delay (2 seconds) and then process the login result
        Clock.schedule_once(lambda dt: self.process_login(login_func(username, password)), 2)

    def process_login(self, success):
        """Processes the login result."""
        self.hide_loading_overlay()
        if success:
            self.on_success(self.entry_username.text.strip())
        else:
            self.show_popup("Error", "Incorrect login credentials!")

    def register(self, instance):
        """Starts the registration process with a loading animation."""
        sound_manager.play_click()
        username = self.entry_username.text.strip()
        password = self.entry_password.text.strip()
        if not username or not password:
            self.show_popup("Error", "Please fill in both fields!")
            return

        # Choose the registration function based on the checkbox setting
        register_func = register_user_json if self.use_json else register_user
        self.show_loading_overlay("Registering...")
        # Simulate registration delay (2 seconds) and then process the registration result
        Clock.schedule_once(lambda dt: self.process_register(register_func(username, password)), 2)

    def process_register(self, success):
        """Processes the registration result."""
        self.hide_loading_overlay()
        if success:
            self.show_popup("Success", "Registration successful! Please log in.")
        else:
            self.show_popup("Error", "Username already taken!")

    def show_popup(self, title, message):
        """Displays a popup with the given title and message."""
        popup_layout = BoxLayout(orientation='vertical', padding=15, spacing=10)
        popup_label = Label(text=message, font_size=18, color=(1, 1, 1, 1))
        popup_button = Button(text="OK", font_size=18, size_hint=(1, 0.3))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)
        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        sound_manager.play_popup()
        popup.open()

