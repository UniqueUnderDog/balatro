def apply_joker(joker,card):
    if not isinstance(card, list):
        return card
    if joker == JokerType.TAROT:
        return card[0]
    elif joker == JokerType.JOKER:
        return card[1]
