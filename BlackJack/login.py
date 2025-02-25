import tkinter as tk
from tkinter import messagebox
from auth import register_user, login_user


class LoginWindow:
    def __init__(self, master, on_success):
        """
        Initializes the login and registration window.

        Args:
            master (tk.Tk): The root window for the application.
            on_success (function): Callback function executed after successful login.
        """
        self.master = master
        self.on_success = on_success  # Callback for successful login
        master.title("Login / Registration")
        master.geometry("600x400")
        master.configure(bg="green")

        self.label_title = tk.Label(master, text="Welcome to Blackjack",
                                    font=("Helvetica", 20), bg="green")
        self.label_title.pack(pady=20)

        self.label_username = tk.Label(master, text="Username:",
                                       font=("Helvetica", 14), bg="green")
        self.label_username.pack(pady=5)
        self.entry_username = tk.Entry(master, font=("Helvetica", 14))
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(master, text="Password:",
                                       font=("Helvetica", 14), bg="green")
        self.label_password.pack(pady=5)
        self.entry_password = tk.Entry(master, font=("Helvetica", 14), show="*")
        self.entry_password.pack(pady=5)

        self.button_login = tk.Button(master, text="Login",
                                      font=("Helvetica", 14), command=self.login)
        self.button_login.pack(pady=10)
        self.button_register = tk.Button(master, text="Register",
                                         font=("Helvetica", 14), command=self.register)
        self.button_register.pack(pady=10)

    def login(self):
        """Handles user login. Validates input fields and checks credentials."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields!")
            return

        if login_user(username, password):
            messagebox.showinfo("Success", "Login successful!")
            self.master.destroy()  # Close login window
            self.on_success(username)  # Call the callback with username
        else:
            messagebox.showerror("Error", "Incorrect login credentials!")

    def register(self):
        """Handles user registration. Validates input fields and creates a new account."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in both fields!")
            return

        register_user(username, password)
        messagebox.showinfo("Registration", "User registered successfully! Please log in.")
