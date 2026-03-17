#!/usr/bin/env python3
"""
德州撲克 (Texas Hold'em) 勝率計算器
Texas Hold'em Poker Win Rate Calculator
Uses Monte Carlo simulation with 10,000 iterations
"""

import random
from itertools import combinations
from collections import Counter

# ─── Card Definitions ──────────────────────────────────────────────────────────
RANKS = "23456789TJQKA"
SUITS = "cdhs"  # clubs, diamonds, hearts, spades
SUIT_SYMBOLS = {"c": "♣", "d": "♦", "h": "♥", "s": "♠"}
RANK_DISPLAY = {"T": "10", "J": "J", "Q": "Q", "K": "K", "A": "A"}

def card_display(card):
    r_idx, s_idx = card
    r = RANKS[r_idx]
    s = SUITS[s_idx]
    r_str = RANK_DISPLAY.get(r, r)
    return f"{r_str}{SUIT_SYMBOLS[s]}"

def parse_card(s):
    s = s.strip().upper()
    if len(s) < 2:
        raise ValueError(f"Invalid card: '{s}'")
    rank = s[0]
    suit = s[1].lower()
    if rank not in RANKS:
        raise ValueError(f"Invalid rank '{rank}'. Use: 2-9, T, J, Q, K, A")
    if suit not in SUITS:
        raise ValueError(f"Invalid suit '{suit}'. Use: c(♣) d(♦) h(♥) s(♠)")
    return (RANKS.index(rank), SUITS.index(suit))

def input_cards(prompt, count, used_cards):
    while True:
        try:
            raw = input(prompt).strip().split()
            if len(raw) != count:
                print(f"  ⚠  Please enter exactly {count} card(s). Example: Ah Kd")
                continue
            cards = [parse_card(c) for c in raw]
            dupes = [c for c in cards if tuple(c) in used_cards]
            if dupes:
                print(f"  ⚠  Card(s) already used: {[card_display(c) for c in dupes]}")
                continue
            dupe_self = len(cards) != len(set(map(tuple, cards)))
            if dupe_self:
                print("  ⚠  Duplicate cards in your input.")
                continue
            return cards
        except ValueError as e:
            print(f"  ⚠  {e}")

# ─── Hand Evaluator ─────────────────────────────────────────────────────────────
def eval_5card(hand):
    """Evaluate a 5-card hand → comparable tuple (higher = better)."""
    ranks = sorted([c[0] for c in hand], reverse=True)
    suits = [c[1] for c in hand]

    is_flush = len(set(suits)) == 1

    is_straight = ranks == list(range(ranks[0], ranks[0] - 5, -1))
    if not is_straight and ranks == [12, 3, 2, 1, 0]:  # Wheel A-2-3-4-5
        is_straight = True
        ranks = [3, 2, 1, 0, -1]

    cnt = Counter(ranks)
    freq = sorted(cnt.values(), reverse=True)
    sorted_ranks = sorted(cnt.keys(), key=lambda r: (cnt[r], r), reverse=True)

    if is_straight and is_flush: return (8, ranks)
    if freq == [4, 1]:           return (7, sorted_ranks)
    if freq == [3, 2]:           return (6, sorted_ranks)
    if is_flush:                 return (5, ranks)
    if is_straight:              return (4, ranks)
    if freq[0] == 3:             return (3, sorted_ranks)
    if freq[:2] == [2, 2]:       return (2, sorted_ranks)
    if freq[0] == 2:             return (1, sorted_ranks)
    return (0, ranks)

HAND_NAMES = [
    "High Card", "One Pair", "Two Pair", "Three of a Kind",
    "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush"
]

def best_7card(cards):
    """Best 5-card hand out of 7 cards."""
    return max(eval_5card(combo) for combo in combinations(cards, 5))

# ─── Monte Carlo Simulation ──────────────────────────────────────────────────────
def calc_win_rate(hole, community, num_players, sims=10000):
    all_cards = [(r, s) for r in range(13) for s in range(4)]
    used = {tuple(c) for c in hole + community}
    deck = [c for c in all_cards if tuple(c) not in used]

    need_board = 5 - len(community)
    need_opps  = (num_players - 1) * 2
    total_need = need_board + need_opps

    if len(deck) < total_need:
        return 0.0, 0.0, 0.0

    wins = ties = losses = 0

    for _ in range(sims):
        random.shuffle(deck)
        board    = list(community) + deck[:need_board]
        opp_deck = deck[need_board:]

        my_rank = best_7card(hole + board)

        beat_me = tie_me = False
        for i in range(num_players - 1):
            opp_hole = opp_deck[i * 2:(i + 1) * 2]
            opp_rank = best_7card(opp_hole + board)
            if opp_rank > my_rank:
                beat_me = True
                break
            elif opp_rank == my_rank:
                tie_me = True

        if beat_me:   losses += 1
        elif tie_me:  ties   += 1
        else:         wins   += 1

    return wins/sims*100, ties/sims*100, losses/sims*100

# ─── Current Best Hand ──────────────────────────────────────────────────────────
def show_current_hand(hole, community):
    if len(community) >= 3:
        rank_tuple = best_7card(hole + community)
        hand_name  = HAND_NAMES[rank_tuple[0]]
        print(f"  🃏  Your current best hand: {hand_name}")

# ─── Display Helpers ────────────────────────────────────────────────────────────
PROGRESS_BAR_WIDTH = 30

def progress_bar(pct):
    filled = int(pct / 100 * PROGRESS_BAR_WIDTH)
    bar = "█" * filled + "░" * (PROGRESS_BAR_WIDTH - filled)
    return f"[{bar}] {pct:5.1f}%"

def print_result(win, tie, loss, stage):
    print(f"\n  ╔══════════════════════════════════════════╗")
    print(f"  ║  📊  {stage:<38}║")
    print(f"  ╠══════════════════════════════════════════╣")
    print(f"  ║  🏆 Win   {progress_bar(win)} ║")
    print(f"  ║  🤝 Tie   {progress_bar(tie)} ║")
    print(f"  ║  ❌ Lose  {progress_bar(loss)} ║")
    print(f"  ╚══════════════════════════════════════════╝")

def cards_str(cards):
    return "  ".join(card_display(c) for c in cards)

# ─── Main Program ────────────────────────────────────────────────────────────────
def main():
    print("\n" + "="*50)
    print("   🃏  德州撲克勝率計算器  🃏")
    print("   Texas Hold'em Win Rate Calculator")
    print("="*50)
    print("   Card format: [Rank][Suit]")
    print("   Ranks: 2 3 4 5 6 7 8 9 T J Q K A")
    print("   Suits: c(♣)  d(♦)  h(♥)  s(♠)")
    print("   Example: Ah = Ace♥   Td = 10♦   Ks = King♠")
    print("="*50 + "\n")

    # Number of players
    while True:
        try:
            n = int(input("  👥  Number of players (2–10): "))
            if 2 <= n <= 10:
                break
            print("  ⚠  Please enter a number between 2 and 10.")
        except ValueError:
            print("  ⚠  Invalid input.")

    used = set()

    # Hole cards
    print("\n  🂠  Enter YOUR 2 hole cards (e.g.  Ah Kd):")
    hole = input_cards("  → ", 2, used)
    used.update(tuple(c) for c in hole)
    print(f"  Your hand: {cards_str(hole)}")

    # Pre-flop
    print("\n  ⏳  Calculating pre-flop odds...")
    w, t, l = calc_win_rate(hole, [], n)
    print_result(w, t, l, "Pre-Flop")

    # ── Flop (3 cards) ──
    print("\n  🂡  Enter the FLOP (3 community cards):")
    flop = input_cards("  → ", 3, used)
    used.update(tuple(c) for c in flop)
    community = flop
    print(f"  Board: {cards_str(community)}")
    show_current_hand(hole, community)

    print("\n  ⏳  Calculating flop odds...")
    w, t, l = calc_win_rate(hole, community, n)
    print_result(w, t, l, "Post-Flop")

    # ── Turn (1 card) ──
    print("\n  🂢  Enter the TURN (1 community card):")
    turn = input_cards("  → ", 1, used)
    used.update(tuple(c) for c in turn)
    community = flop + turn
    print(f"  Board: {cards_str(community)}")
    show_current_hand(hole, community)

    print("\n  ⏳  Calculating turn odds...")
    w, t, l = calc_win_rate(hole, community, n)
    print_result(w, t, l, "Post-Turn")

    # ── River (1 card) ──
    print("\n  🂣  Enter the RIVER (1 community card):")
    river = input_cards("  → ", 1, used)
    used.update(tuple(c) for c in river)
    community = flop + turn + river
    print(f"  Board: {cards_str(community)}")

    print("\n  ⏳  Calculating final odds...")
    w, t, l = calc_win_rate(hole, community, n, sims=50000)

    hand_rank_val = best_7card(hole + community)
    final_hand    = HAND_NAMES[hand_rank_val[0]]
    print(f"\n  🃏  Your final best hand: \033[1m{final_hand}\033[0m")
    print_result(w, t, l, "Post-River (Final)")
    print()

if __name__ == "__main__":
    while True:
        main()
        again = input("  🔄  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("\n  GG! Thanks for using Texas Hold'em Calculator! 🃏\n")
            break
