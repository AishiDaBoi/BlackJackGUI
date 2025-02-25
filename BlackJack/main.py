import tkinter as tk
from login import LoginWindow
import blackjackgame
from db import get_db_connection


class MainMenu:
    def __init__(self, master, username):
        """Main menu after successful login."""
        self.master = master
        self.master.title("Blackjack Main Menu")
        self.master.geometry("600x400")
        self.master.configure(bg="green")

        self.username = username

        tk.Label(master, text=f"Welcome, {username}!", font=("Helvetica", 18), bg="green").pack(pady=10)

        self.start_button = tk.Button(master, text="🎲 Play Blackjack", font=("Helvetica", 14), command=self.start_blackjack)
        self.start_button.pack(pady=10)

        self.highscore_frame = tk.Frame(master, bg="white", bd=2, relief="sunken")
        self.highscore_frame.pack(pady=10, fill="both", expand=True)
        self.show_highscores()

    def start_blackjack(self):
        """Starts the Blackjack game."""
        self.master.withdraw()  # Versteckt das Hauptmenü-Fenster
        game_root = tk.Toplevel(self.master)  # Erstellt ein neues Fenster für Blackjack
        blackjackgame.BlackjackGUI(game_root, self.username)

    def show_highscores(self):
        """Displays the highscore list."""
        tk.Label(self.highscore_frame, text="🏆 Highscores", font=("Helvetica", 14, "bold"), bg="white").pack(pady=5)
        scores = self.get_highscores()

        for user, score in scores:
            tk.Label(self.highscore_frame, text=f"{user}: {score} Wins", font=("Helvetica", 12), bg="white").pack()

    def get_highscores(self):
        """Fetches the highscore list from the database."""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, highscore FROM users ORDER BY highscore DESC LIMIT 10")
        scores = cursor.fetchall()
        cursor.close()
        conn.close()
        return scores


def open_main_menu(username):
    """Opens the main menu after successful login."""
    root = tk.Tk()
    MainMenu(root, username)
    root.mainloop()


def start_login():
    """Opens the login window and waits for successful login."""
    root = tk.Tk()
    login_window = LoginWindow(root, open_main_menu)  # Pass the callback function
    root.mainloop()


if __name__ == "__main__":
    start_login()
