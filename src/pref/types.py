from dataclasses import dataclass
from typing import Literal

Card = int
Suit = Literal["Pik", "Karo", "Herc", "Tref"]

# we really need this to be ord tho
Igra = Literal["Pik", "Karo", "Herc", "Tref", "Betl", "Sanac", "Preferans"]
Player = int
Licitacija = list[tuple[Player, Igra | None]]

Hand = list[Card]
Game = tuple[Hand, Hand, Hand]
Move = tuple[Hand, Card]

Stih = tuple[Card, Card, Card]
Stihovi = list[Stih]
PobjedniciStihova = list[int]
OsvojeniStihovi = list[int]

Bodovi = list[int]
Juhe = list[int]


@dataclass
class Round:
    lic: Licitacija
    izvodjac: Player
    igra: Igra
    tko_igra: tuple[bool, bool, bool]
    stihovi: list[tuple[Card, Card, Card]]
    pobjednici_stihova: list[int]
    osvojeni_stihovi: list[int]
    bodovi: list[int]
    juhe: list[int]
