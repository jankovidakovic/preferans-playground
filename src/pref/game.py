import random

from pref.types import *


def sljedeci(igrac: Player) -> Player:
    return (igrac + 1) % 3


def get_stih(stih: Stih, igra: Igra) -> Player:
    return 1


def make_move(hand: Hand, current_move_cards: list[Card]) -> Card:
    # potencijalno ilegalno (mora postivat boju, mora sijec adutom)
    return hand[0]  # uvijek igra prvu kartu


def licitiranje(igraci: list[Hand], prvi_na_stihu: Player) -> Licitacija:
    return [(0, None), (1, None), (2, None)]  # refa


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


def jel_izvodjac_proso(osvojeni_stihovi: int, igra: Igra) -> bool:
    if igra == "Betl" and osvojeni_stihovi == 0:
        return True
    return osvojeni_stihovi >= 6


def jesu_pratioci_pali(osvojeni_stihovi: tuple[int, int]) -> tuple[bool, bool]:
    if osvojeni_stihovi[0] + osvojeni_stihovi[1] >= 4:
        print("Oba pratioca prosli")
        return (True, True)
    return (osvojeni_stihovi[0] >= 2, osvojeni_stihovi[1] >= 2)


def kolko_igra_vrijedi(igra: Igra) -> int:
    return 8  # mos mislit


def igranje_stihova(
    igraci: list[Hand],
    izvodjac: Player,
    igra: Igra,
    tko_igra: tuple[bool, bool, bool],
    prvi_na_stihu: Player,
) -> tuple[Stihovi, PobjedniciStihova, OsvojeniStihovi]:

    stihovi = []
    pobjednici_stihova = []
    osvojeni_stihovi = [0, 0, 0]

    if sum(tko_igra) == 1:
        # dalje dalje
        osvojeni_stihovi[izvodjac] = 10
        return stihovi, pobjednici_stihova, osvojeni_stihovi

    trenutni_na_stihu = tko_igra_prvi(prvi_na_stihu, tko_igra)

    for move in range(1, 10 + 1):
        print(f"Potez {move}")
        # TODO: sta ak sam jedan igra

        # prvi
        prva_karta = make_move(igraci[trenutni_na_stihu], [])

        # drugi
        trenutni_na_stihu = sljedeci(trenutni_na_stihu)
        druga_karta = make_move(igraci[trenutni_na_stihu], [prva_karta])

        # treci
        trenutni_na_stihu = sljedeci(trenutni_na_stihu)
        treca_karta = make_move(igraci[trenutni_na_stihu], [prva_karta, druga_karta])

        stih = (prva_karta, druga_karta, treca_karta)
        stihovi.append(stih)
        pobjednik_stiha = tko_nosi_stih(stih, igra)
        pobjednici_stihova.append(pobjednik_stiha)
        osvojeni_stihovi[pobjednik_stiha] += 1

    return stihovi, pobjednici_stihova, osvojeni_stihovi


def bodovanje(
    igra: Igra,
    izvodjac: Player,
    tko_igra: tuple[bool, bool, bool],
    osvojeni_stihovi: OsvojeniStihovi,
) -> tuple[Bodovi, Juhe]:
    igra_vrijedi = kolko_igra_vrijedi(igra)
    izvodjac_proso = jel_izvodjac_proso(osvojeni_stihovi[izvodjac], igra)
    drugi_pao, treci_pao = jesu_pratioci_pali(
        (
            osvojeni_stihovi[sljedeci(izvodjac)],
            osvojeni_stihovi[sljedeci(sljedeci(izvodjac))],
        )
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

    return bodovi, juhe


def play_round(
    igraci: list[Hand], prvi_na_stihu: Player, talon: list[Card]
) -> Round | None:
    lic = licitiranje(igraci, prvi_na_stihu)
    if lic == [(0, None), (1, None), (2, None)]:
        return None  # refa

    izvodjac = pobjednik_lic(lic)
    igraci[izvodjac].extend(talon)  # uzme talon

    igraci[izvodjac], odbaceni_talon = odbaci_talon(igraci[izvodjac])

    igra = zvanje(igraci[izvodjac], lic, odbaceni_talon)

    tko_igra = odredi_jel_igraju(igraci, lic, izvodjac, igra, talon, prvi_na_stihu)

    stihovi, pobjednici_stihova, osvojeni_stihovi = igranje_stihova(
        igraci, izvodjac, igra, tko_igra, prvi_na_stihu
    )

    bodovi, juhe = bodovanje(igra, izvodjac, tko_igra, osvojeni_stihovi)

    # lic: Licitacija
    # izvodjac: Player
    # igra: Igra
    # jel_igraju: list[bool]
    # stihovi: list[tuple[Card, Card, Card]]
    # pobjednici_stihova: list[int]
    # osvojeni_stihovi: tuple[int, int, int]
    # bodovi: tuple[int, int, int]
    # juhe: tuple[int, int, int]

    return Round(
        lic,
        izvodjac,
        igra,
        tko_igra,
        stihovi,
        pobjednici_stihova,
        osvojeni_stihovi,
        bodovi,
        juhe,
    )


def random_32_cards() -> list[Card]:
    cards = list(range(32))
    random.shuffle(cards)
    return cards


def play_game(starting_points: int, max_rounds: int) -> list[int]:
    bodovi = [starting_points, starting_points, starting_points]
    juhe = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    prvi_na_stihu = random.randint(0, 3)

    round_num = 0

    while sum(bodovi) > 0 and round_num < max_rounds:
        round_num += 1
        print(f"Round {round_num}")
        cards = random_32_cards()
        players = [cards[:10], cards[11:20], cards[21:30]]
        round = play_round(players, prvi_na_stihu, cards[30:32])

        if round is None:
            print("Refa")
            continue  # TODO: refa

        bodovi[0] += round.bodovi[0]
        bodovi[1] += round.bodovi[1]
        bodovi[2] += round.bodovi[2]

        juhe[sljedeci(round.izvodjac)][round.izvodjac] = round.juhe[
            sljedeci(round.izvodjac)
        ]
        juhe[sljedeci(sljedeci(round.izvodjac))][round.izvodjac] = round.juhe[
            sljedeci(sljedeci(round.izvodjac))
        ]

    scores = [
        bodovi[0] * 10 - juhe[0][1] - juhe[0][2] + juhe[1][0] + juhe[2][0],
        bodovi[1] * 10 - juhe[1][2] - juhe[1][0] + juhe[2][1] + juhe[0][1],
        bodovi[2] * 10 - juhe[2][0] - juhe[2][1] + juhe[0][2] + juhe[1][2],
    ]

    return scores
