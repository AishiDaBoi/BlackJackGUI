# 🃏 BlackJackGUI 🎰  

A fully interactive **Blackjack** game with a **Kivy-based GUI**, complete with betting, score tracking, and sound effects.  
Try your luck, **beat the dealer**!  

---

## 🚀 Features  
✅ **Graphical User Interface (GUI)** powered by Kivy 🎨  
✅ **User Authentication** (Registration & Login) with secure password hashing 🔐  
✅ **High Score System** stored in a SQLite database 🏆  
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
  - **Double Down** 🔄 → Double the bet and draw one more card
  - **Bet Money** 💸 → Wager an amount before the round starts  
- The **dealer must draw until reaching at least 17 points**.  
- If a player’s hand exceeds **21**, they lose automatically (Bust).  
- If the **player beats the dealer**, they **win their bet** and increase their balance.  
- If the **dealer wins**, the player loses their bet.
- If it's a **tie**, the player keeps their bet.