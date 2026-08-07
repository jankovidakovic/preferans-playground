from pref.types import Igra, Player, Suit


def sljedeci(igrac: Player) -> Player:
    return (igrac + 1) % 3


def prethodni(igrac: Player) -> Player:
    return (igrac + 2) % 3  # isto ko -1%3, al nema negativnih brojeva


def igra_u_boju(igra: Igra) -> Suit | None:
    if igra == "Pik":
        return "Pik"
    elif igra == "Karo":
        return "Karo"
    elif igra == "Herc":
        return "Herc"
    elif igra == "Tref":
        return "Tref"
    return None
