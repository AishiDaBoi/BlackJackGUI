import tkinter as tk
from tkinter import messagebox

from .auth import login_user, register_user
from .loginViaJson import login_user_json, register_user_json

class LoginWindow:
    def __init__(self, master, on_success):
        self.master = master
        self.on_success = on_success
        self.use_json = tk.BooleanVar(value=False)

        master.title("Login / Registrierung")
        master.geometry("600x400")
        master.configure(bg="green")

        tk.Label(master, text="Willkommen bei Blackjack", font=("Helvetica", 20), bg="green").pack(pady=20)

        tk.Label(master, text="Username:", font=("Helvetica", 14), bg="green").pack(pady=5)
        self.entry_username = tk.Entry(master, font=("Helvetica", 14))
        self.entry_username.pack(pady=5)

        tk.Label(master, text="Password:", font=("Helvetica", 14), bg="green").pack(pady=5)
        self.entry_password = tk.Entry(master, font=("Helvetica", 14), show="*")
        self.entry_password.pack(pady=5)

        self.json_checkbox = tk.Checkbutton(master, text="JSON statt MySQL nutzen", variable=self.use_json, bg="green", font=("Helvetica", 12))
        self.json_checkbox.pack(pady=5)

        tk.Button(master, text="Login", font=("Helvetica", 14), command=self.login).pack(pady=10)
        tk.Button(master, text="Registrieren", font=("Helvetica", 14), command=self.register).pack(pady=10)

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        use_json = self.use_json.get()

        if not username or not password:
            messagebox.showerror("Fehler", "Bitte beide Felder ausfüllen!")
            return

        if (login_user_json(username, password) if use_json else login_user(username, password)):
            messagebox.showinfo("Erfolg", "Login erfolgreich!")
            self.master.destroy()
            self.on_success(username)
        else:
            messagebox.showerror("Fehler", "Falsche Anmeldeinformationen!")

    def register(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        use_json = self.use_json.get()

        if not username or not password:
            messagebox.showerror("Fehler", "Bitte beide Felder ausfüllen!")
            return

        success = register_user_json(username, password) if use_json else register_user(username, password)

        if success:
            messagebox.showinfo("Erfolg", "Registrierung erfolgreich! Bitte einloggen.")
        else:
            messagebox.showerror("Fehler", "Benutzername bereits vergeben!")
