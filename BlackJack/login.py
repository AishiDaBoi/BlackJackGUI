import tkinter as tk
from tkinter import messagebox
from loginViaJson import login, register  # Neue Login/Registrierung aus JSON & DB

class LoginWindow:
    def __init__(self, master, on_success):
        """
        Erstellt das Login- und Registrierungsfenster.

        Args:
            master (tk.Tk): Das Hauptfenster der Anwendung.
            on_success (function): Callback-Funktion nach erfolgreichem Login.
        """
        self.master = master
        self.on_success = on_success  # Callback nach erfolgreichem Login
        self.use_json = tk.BooleanVar(value=False)  # Standard: Datenbank-Login

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

        # Auswahl, ob JSON oder Datenbank genutzt wird
        self.json_checkbox = tk.Checkbutton(master, text="JSON statt Datenbank nutzen",
                                            variable=self.use_json, bg="green", font=("Helvetica", 12))
        self.json_checkbox.pack(pady=5)

        tk.Button(master, text="Login", font=("Helvetica", 14), command=self.login).pack(pady=10)
        tk.Button(master, text="Registrieren", font=("Helvetica", 14), command=self.register).pack(pady=10)

    def login(self):
        """Verarbeitet das Login-Event."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Fehler", "Bitte beide Felder ausfüllen!")
            return

        if login(username, password, self.use_json.get()):
            messagebox.showinfo("Erfolg", "Login erfolgreich!")
            self.master.destroy()  # Fenster schließen
            self.on_success(username)  # Callback aufrufen
        else:
            messagebox.showerror("Fehler", "Falsche Anmeldeinformationen!")

    def register(self):
        """Verarbeitet das Registrierungs-Event."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Fehler", "Bitte beide Felder ausfüllen!")
            return

        if register(username, password, self.use_json.get()):
            messagebox.showinfo("Erfolg", "Registrierung erfolgreich! Bitte einloggen.")
        else:
            messagebox.showerror("Fehler", "Benutzername bereits vergeben!")
