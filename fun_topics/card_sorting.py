import random

# Constants
SUITS = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Generate standard 52-card deck
def build_deck():
    return [f"{rank} of {suit}" for suit in SUITS for rank in RANKS]

# Helper to get numerical value for sorting
def rank_value(rank):
    return RANKS.index(rank)

def suit_value(suit):
    return SUITS.index(suit)

# Parsing card string
def parse_card(card):
    rank, _, suit = card.partition(' of ')
    return rank, suit

# --- Sorting Functions ---

# Sort by rank (within suit)
def sort_by_rank(deck):
    return sorted(deck, key=lambda card: rank_value(parse_card(card)[0]))

# Sort by suit (within rank)
def sort_by_suit(deck):
    return sorted(deck, key=lambda card: suit_value(parse_card(card)[1]))

# Sort full: suit first, then rank
def sort_suit_then_rank(deck):
    return sorted(deck, key=lambda card: (suit_value(parse_card(card)[1]), rank_value(parse_card(card)[0])))

# Sort full: rank first, then suit
def sort_rank_then_suit(deck):
    return sorted(deck, key=lambda card: (rank_value(parse_card(card)[0]), suit_value(parse_card(card)[1])))

# Using slicing to group and sort per-suit blocks
def sort_by_suit_blocks(deck):
    suit_groups = [[card for card in deck if parse_card(card)[1] == suit] for suit in SUITS]
    return [card for group in suit_groups for card in sorted(group, key=lambda card: rank_value(parse_card(card)[0]))]

# --- Dealing Functions ---

# Deal cards to N players
def deal_cards(deck, num_players=4, cards_each=5):
    return [deck[i::num_players][:cards_each] for i in range(num_players)]

# Shuffle and deal
def shuffle_and_deal(num_players=4, cards_each=5):
    deck = build_deck()
    random.shuffle(deck)
    hands = deal_cards(deck, num_players, cards_each)
    return hands

# --- Example Usage ---
if __name__ == "__main__":
    deck = build_deck()
    random.shuffle(deck)

    print("Original shuffled deck (first 10):")
    print(deck[:10])

    print("\nSorted by rank:")
    print(sort_by_rank(deck)[:10])

    print("\nSorted by suit:")
    print(sort_by_suit(deck)[:10])

    print("\nSorted by suit then rank:")
    print(sort_suit_then_rank(deck)[:10])

    print("\nSorted by rank then suit:")
    print(sort_rank_then_suit(deck)[:10])

    print("\nSorted by per-suit block slicing:")
    print(sort_by_suit_blocks(deck)[:10])

    print("\nDealt hands:")
    hands = shuffle_and_deal(num_players=4, cards_each=5)
    for i, hand in enumerate(hands):
        print(f"Player {i+1}: {hand}")