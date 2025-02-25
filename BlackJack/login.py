# login.py

import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk
import os
import pygame.mixer
from auth import register_user, login_user
import highscore
import blackjackgame


# --- Login-/Registrierungs-GUI ---

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login / Registrierung")
        master.geometry("600x400")
        master.configure(bg="green")

        self.label_title = tk.Label(master, text="Willkommen bei Blackjack",
                                    font=("Helvetica", 20), bg="green")
        self.label_title.pack(pady=20)

        self.label_username = tk.Label(master, text="Benutzername:",
                                       font=("Helvetica", 14), bg="green")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(master, font=("Helvetica", 14))
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(master, text="Passwort:",
                                       font=("Helvetica", 14), bg="green")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(master, font=("Helvetica", 14), show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(master, text="Login",
                                      font=("Helvetica", 14), command=self.login)
        self.button_login.pack(pady=10)
        self.button_register = tk.Button(master, text="Registrieren",
                                         font=("Helvetica", 14), command=self.register)
        self.button_register.pack(pady=10)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showerror("Fehler", "Bitte beide Felder ausfüllen!")
            return
        if login_user(username, password):
            messagebox.showinfo("Erfolg", "Login erfolgreich!")
            self.master.destroy()
            game_root = tk.Tk()
            blackjackgame.BlackjackGUI(game_root, username)
            game_root.mainloop()
        else:
            messagebox.showerror("Fehler", "Falsche Anmeldedaten!")

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        if not username or not password:
            messagebox.showerror("Fehler", "Bitte beide Felder ausfüllen!")
            return
        register_user(username, password)
        messagebox.showinfo("Registrierung", "Benutzer erfolgreich registriert! Bitte einloggen.")


# --- Programmstart ---

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
