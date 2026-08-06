from pref.types import Player


def sljedeci(igrac: Player) -> Player:
    return (igrac + 1) % 3


def prethodni(igrac: Player) -> Player:
    return (igrac + 2) % 3  # isto ko -1%3, al nema negativnih brojeva
