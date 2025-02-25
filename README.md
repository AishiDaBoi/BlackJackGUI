# 🃏 BlackJackGUI 🎰  

A fully interactive **Blackjack** game with a **Tkinter-based GUI**, complete with betting, score tracking, and sound effects.  
Try your luck, **beat the dealer**, and set your **high score**!  

---

## 🚀 Features  
✅ **Graphical User Interface (GUI)** powered by Tkinter 🎨  
✅ **User Authentication** (Registration & Login) with secure password hashing 🔐  
✅ **High Score System** stored in a MySQL database 🏆  
✅ **Betting Mechanism**: Place bets, win, or lose it all! 💰  
✅ **Deck Shuffling & Randomization** for a fair experience 🎴  
✅ **Background Music & Sound Effects** for immersive gameplay 🎵  
✅ **Card Visualization** with dynamically rendered images 🃏

---

## 🎯 Game Rules  
- The goal is to get as close as possible to **21 points** without exceeding it.  
- **Card Values**:  
  - **Number cards (2-10)** → Face value  
  - **Face cards (Jack, Queen, King)** → 10 points  
  - **Ace (A)** → 1 or 11 points, depending on the hand  
- Players can:  
  - **Hit** 🂡 → Draw another card  
  - **Stand** ✋ → Keep their current total  
  - **Bet Money** 💸 → Wager an amount before the round starts  
- The **dealer must draw until reaching at least 17 points**.  
- If a player’s hand exceeds **21**, they lose automatically (Bust).  
- If the **player beats the dealer**, they **win their bet** and increase their balance.  

---

## 🛠️ Installation & Setup  

### 1️⃣ Prerequisites  
Ensure you have the following installed:  
- Python **3.x**  
- `pip` (Python package manager)  
- MySQL Database (or any compatible cloud database)  

### 2️⃣ Clone the Repository  
```bash
git clone https://github.com/yourusername/BlackJackGUI.git
cd BlackJackGUI
