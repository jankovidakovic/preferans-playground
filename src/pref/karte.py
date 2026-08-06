from pref.constants import HUMAN_READABLE_CARD_MAPPING
from pref.types import Card, Suit


def is_suit(card: Card, suit: Suit) -> bool:
    match suit:
        case "Pik":
            return card < 8
        case "Karo":
            return 8 <= card < 16
        case "Herc":
            return 16 <= card < 24
        case "Tref":
            return 24 <= card < 32


def get_cards_of_suit(cards: list[Card], suit: Suit) -> list[Card]:
    match suit:
        case "Pik":
            suit_normalization = 0
        case "Karo":
            suit_normalization = 8
        case "Herc":
            suit_normalization = 16
        case "Tref":
            suit_normalization = 24

    return [card - suit_normalization for card in cards if is_suit(card, suit)]


def human_readable_cards_of_suit(cards_of_suit: list[Card]) -> list[str]:
    return [HUMAN_READABLE_CARD_MAPPING[card] for card in cards_of_suit]
