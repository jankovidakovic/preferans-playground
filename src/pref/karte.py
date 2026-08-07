from pref.constants import HUMAN_READABLE_CARD_MAPPING
from pref.types import Card, Suit


def get_card_suit(card: Card) -> Suit:
    if 0 <= card < 8:
        return "Pik"
    elif 8 <= card < 16:
        return "Karo"
    elif 16 <= card < 24:
        return "Herc"
    elif 24 <= card < 32:
        return "Tref"
    else:
        raise RuntimeError(f"cannot convert card {card} to suit")


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


def najveca_u_boji(karte: list[Card], boja: Suit) -> Card | None:
    karte_u_boji = get_cards_of_suit(karte, boja)
    if len(karte_u_boji) == 0:
        return None
    return max(karte_u_boji)
