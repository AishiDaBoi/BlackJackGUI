import tkinter as tk
from auth import LoginWindow, login_user
from game import BlackjackGame, Deck


def open_game(username):
    root = tk.Tk()
    BlackjackGame(root, username)
    root.mainloop()

def start_login():
    root = tk.Tk()
    login_window = LoginWindow(root, open_game)
    root.mainloop()

if __name__ == "__main__":
    start_login()
