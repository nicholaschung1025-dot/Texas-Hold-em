
# 🃏 Texas Hold'em Win Rate Calculator

A **visual, browser-based Texas Hold'em poker odds calculator** that runs entirely in your web browser using **PyScript**. Click cards from an interactive 52-card deck and see your win/tie/loss percentages update after every betting round.

[![Poker Calculator Demo](https://via.placeholder.com/800x400/f1c40f/000000?text=🃏+Texas+Hold%27em+Calculator)](https://yourusername.github.io/poker-calculator/)

## ✨ Features

| 🎯 **Round-by-Round Tracking** | 📊 **Visual Deck Selection** | 🎨 **Casino UI** |
|---|---|---|
| Pre-Flop → Flop → Turn → River | Click real poker cards (no typing!) | Green felt table + gold buttons |
| History grid shows odds evolution | Smart state machine enforces correct card counts | Responsive design (mobile/desktop) |
| Current best hand displayed | Instant visual feedback | Non-blocking async calculations |

## 🎮 How to Play

```
1️⃣ Set # of players (2-10)
2️⃣ Click your 2 HOLE CARDS from the deck (turns blue)
3️⃣ Click "Calculate Pre-Flop" → See odds in history grid
4️⃣ Click exactly 3 FLOP cards → "Calculate Flop"
5️⃣ Click 1 TURN card → "Calculate Turn"  
6️⃣ Click 1 RIVER card → "Calculate River" (Final)
7️⃣ Compare odds evolution across all 4 rounds!
```

## 🖥️ Live Demo

**[Try it live →](https://yourusername.github.io/poker-calculator/)**

## 🚀 Quick Deploy (5 minutes)

1. **Create GitHub Repo**
   ```bash
   gh repo create poker-calculator --public --source=.
   ```

2. **Upload `index.html`**
   - Drag & drop the HTML file from previous messages to your repo's `main` branch

3. **Enable GitHub Pages**
   ```
   Repo Settings → Pages → Source: "Deploy from branch" → Branch: main → Save
   ```

4. **Your site is live!** → `https://yourusername.github.io/poker-calculator`

## 🛠️ Technical Stack

```
Frontend: Vanilla JavaScript + CSS3
Backend: PyScript (Python in browser via WebAssembly)
Math: Monte Carlo simulation (3,500 iterations per calculation)
Standards: Pure HTML5 - No backend server needed
```

## 📊 How It Works (The Math)

**Monte Carlo Simulation** removes all known cards from the deck and simulates thousands of possible outcomes:

```
1. Remove your hole cards + community cards from 52-card deck
2. Remaining deck = N cards
3. For 3,500 iterations:
   ├─ Shuffle remaining deck
   ├─ Deal missing board cards to complete 5-card community
   ├─ Deal 2 cards to each opponent
   ├─ Evaluate best 5-card hand for you vs all opponents
   └─ Count win/tie/loss
4. Win% = (wins ÷ 3500) × 100
```

**✅ Blocker Effect:** If you hold A♠, opponents have 3/51 chance of A♠ (not 4/52).

## 🎨 Design Inspiration

- **Green felt gradient** (`#1b6336 → #0a2e16`)
- **Wooden table rim** (`border: 12px solid #3e2723`)
- **Gold casino buttons** (`linear-gradient(#f1c40f, #d4ac0d)`)
- **Progress bars** animate smoothly with `transition: width 0.5s`

## 📱 Mobile-First

```
✅ Touch-friendly card selection
✅ Responsive poker table layout  
✅ Landscape/portrait support
✅ No zoom issues (viewport meta)
```

## 🔮 Example Usage

```
Your Hand: A♠ K♥ (2 players)
├─ Pre-Flop:  67.2% |  4.1% | 28.7%
├─ Flop:     A♣ 7♦ 2♠ → 82.4% |  3.2% | 14.4%
├─ Turn:     Q♥ → 78.9% |  2.8% | 18.3%
└─ River:    5♣ → 91.7% |  1.9% |  6.4%
```

## 🤝 Contributing

1. **Fork** this repository
2. **Edit** `index.html`
3. **Test locally** (double-click file or use `npx serve`)
4. **PR** your improvements!

## 📄 License

MIT License - Free for personal/commercial use. Credit appreciated!

## 🙏 Acknowledgments

- **PyScript** - Python in the browser magic
- **Poker math** - Adapted from pro Texas Hold'em equity calculators
- **UI Design** - Professional casino aesthetic standards

---

⭐ **Star this repo if it helps your game!** 🃏

---

```
Deployed with ❤️ using GitHub Pages - Zero hosting costs forever
```
