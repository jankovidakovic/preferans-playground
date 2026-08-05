import random
from dataclasses import dataclass

Card = int
Igra = "Pik" | "Karo" | "Herc" | "Tref" | "Betl" | "Sanac" | "Preferans"
Player = 1 | 2 | 3
Licitacija = list[tuple[Player, Igra | None]]

Hand = list[Card]
Game = (Hand, Hand, Hand)
Move = (Hand, Card)

Stih = (Card, Card, Card)

Bodovi = tuple[int, int, int]
Juhe = tuple[int, int, int]


def sljedeci(igrac: Player) -> Player:
    return (igrac + 1) % 3


def get_stih(stih: Stih, igra: Igra) -> Player:
    return 1


def make_move(hand: Hand, current_move_cards: list[Card]) -> Card:
    return hand[0]  # uvijek igra prvu kartu


# potencijalno ilegalno (mora postivat boju, mora sijec adutom)


def licitiranje(a: Hand, b: Hand, c: Hand, prvi_na_stihu: Player) -> Licitacija:
    return None


def pobjednik_lic(lic: Licitacija) -> Player:
    return 1


def odbaci_talon(igrac: Hand) -> tuple[Hand, list[Card]]:
    # odbaci zadnje dvije karte
    return igrac[:10], [igrac[10], igrac[11]]


def zvanje(igrac: Hand, lic: Licitacija, odbaceni_talon: list[Card]) -> Igra:
    return "Herc"  # whatever


def odredi_jel_igraju(
    igraci: list[Hand],
    lic: Licitacija,
    izvodjac: Player,
    igra: Igra,
    talon: list[Card],
    prvi_na_stihu: Player,
) -> tuple[bool, bool, bool]:
    return True, False, False


def tko_igra_prvi(prvi_na_stihu: Player, jel_igraju: tuple[bool, bool, bool]) -> Player:
    return 1  # uvijek prvi igra


def tko_nosi_stih(stih: tuple[Card, Card, Card], igra: Igra) -> Player:
    return 1  # uvijek prvi nosi stih


def jel_izvodjac_proso(stihovi: int, igra: Igra) -> bool:
    if igra == "Betl" and stihovi == 0:
        return True
    return stihovi >= 6


def jesu_pratioci_pali(stihovi: tuple[int, int]) -> tuple[bool, bool]:
    if stihovi[0] + stihovi[1] >= 4:
        return (True, True)
    return (stihovi[0] >= 2, stihovi[1] >= 2)


def kolko_igra_vrijedi(igra: Igra) -> int:
    return 8  # mos mislit


@dataclass
class Round:
    lic: Licitacija
    izvodjac: Player
    igra: Igra
    jel_igraju: list[bool]
    stihovi: list[tuple[Card, Card, Card]]
    pobjednici_stihova: list[int]
    osvojeni_stihovi: tuple[int, int, int]
    bodovi: tuple[int, int, int]
    juhe: tuple[int, int, int]


def play_round(
    igraci: list[Hand], prvi_na_stihu: Player, talon: list[Card]
) -> tuple[Bodovi, Juhe]:
    lic: Licitacija | None = licitiranje(igraci, prvi_na_stihu)
    if lic is None:
        return "Dalje"

    izvodjac = pobjednik_lic(lic)
    igraci[izvodjac].extend(talon)

    igraci[izvodjac], odbaceni_talon = odbaci_talon(igraci[izvodjac])

    igra = zvanje(igraci[izvodjac], lic, odbaceni_talon)

    jel_igraju = odredi_jel_igraju(igraci, lic, igra, talon, prvi_na_stihu)

    if sum(jel_igraju) == 1:
        # dalje dalje
        return (10, 0, 0)

    trenutni_na_stihu = tko_igra_prvi(prvi_na_stihu, jel_igraju)

    stihovi = []
    osvojeni_stihovi = [0, 0, 0]

    for move in range(10):
        prvi_igrac = igraci[trenutni_na_stihu]
        prva_karta = make_move(prvi_igrac, [])

        drugi_igrac = igraci[sljedeci(prvi_igrac)]
        druga_karta = make_move(drugi_igrac, [prva_karta])

        treci_igrac = igraci[sljedeci(drugi_igrac)]
        treca_karta = make_move(treci_igrac, [prva_karta, druga_karta])

        stih = (prva_karta, druga_karta, treca_karta)
        stihovi.append(stih)
        pobjednik_stiha = tko_nosi_stih(stih, igra)
        osvojeni_stihovi[pobjednik_stiha] += 1

    igra_vrijedi = kolko_igra_vrijedi(igra)
    izvodjac_proso = jel_izvodjac_proso(osvojeni_stihovi[izvodjac], igra)
    drugi_pao, treci_pao = jesu_pratioci_pali(
        osvojeni_stihovi[sljedeci(izvodjac)],
        osvojeni_stihovi[sljedeci(sljedeci(izvodjac))],
    )

    bodovi = [0, 0, 0]
    bodovi[izvodjac] = -igra_vrijedi if izvodjac_proso else igra_vrijedi
    if drugi_pao:
        bodovi[sljedeci(izvodjac)] = igra_vrijedi
    if treci_pao:
        bodovi[sljedeci(sljedeci(izvodjac))] = igra_vrijedi

    juhe = [0, 0, 0]
    juhe[sljedeci(izvodjac)] = (
        osvojeni_stihovi[sljedeci(izvodjac)]
        if igra != "Betl"
        else (0 if izvodjac_proso else 5 * igra_vrijedi)
    )

    juhe[sljedeci(sljedeci(izvodjac))] = (
        osvojeni_stihovi[sljedeci(sljedeci(izvodjac))]
        if igra != "Betl"
        else (0 if izvodjac_proso else 5 * igra_vrijedi)
    )

    return tuple(bodovi), tuple(juhe)


def random_32_cards() -> list[Card]:
    return []


def play_game(pocetni_bodovi: int) -> tuple[Bodovi, Juhe]:
    bodovi = [pocetni_bodovi, pocetni_bodovi, pocetni_bodovi]
    juhe = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    prvi_na_stihu = random.randint(3)

    while sum(bodovi) > 0:
        cards = random_32_cards()
        players = [cards[:10], cards[11:20], cards[21:30]]
        runda = play_round(players, prvi_na_stihu, cards[30:32])

        bodovi[0] += runda.bodovi[0]
        bodovi[1] += runda.bodovi[1]
        bodovi[2] += runda.bodovi[2]

        juhe[sljedeci(runda.izvodjac)][runda.izvodjac] = juhe[sljedeci(runda.izvodjac)]
        juhe[sljedeci(sljedeci(runda.izvodjac))][runda.izvodjac] = juhe[
            sljedeci(sljedeci(runda.izvodjac))
        ]

    final = [
        bodovi[0] * 10 - juhe[0][1] - juhe[0][2] + juhe[1][0] + juhe[2][0],
        bodovi[1] * 10 - juhe[1][2] - juhe[1][0] + juhe[2][1] + juhe[0][1],
        bodovi[2] * 10 - juhe[2][0] - juhe[2][1] + juhe[0][2] + juhe[1][2],
    ]

    return final
