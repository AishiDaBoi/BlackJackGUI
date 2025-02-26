import tkinter as tk

def animate_card(hand, master):
    """Animiert das Bewegen einer Karte auf den Tisch."""
    for card in hand:
        label = tk.Label(master, text=f"{card['rank']} {card['suit']}", bg="white", font=("Helvetica", 14))
        label.place(x=100, y=100)  # Karten erscheinen hier
