from pref.constants import BOJE
from pref.karte import get_cards_of_suit, human_readable_cards_of_suit
from pref.types import Card, Hand, Suit


def broj_sigurnih_stihova(karte_u_boji: list[Card]) -> int:
    broj_stihova = 0
    najjaca_karta = 7
    for i in sorted(karte_u_boji, reverse=True):
        if i == najjaca_karta:
            broj_stihova += 1
            najjaca_karta -= 1
        else:
            break
    return broj_stihova


def stihovi_u_bojama(hand: Hand) -> dict[Suit, int]:
    stihovi_u_boji: dict[Suit, int] = {}
    for boja in BOJE:
        karte_u_boji = get_cards_of_suit(hand, boja)
        stihovi_u_boji[boja] = broj_sigurnih_stihova(karte_u_boji)

    return stihovi_u_boji


def drugi_kralj(karte_u_boji: list[Card]) -> bool:
    kralj = 6
    return kralj in karte_u_boji and len(karte_u_boji) > 1


def treca_baba(karte_u_boji: list[Card]) -> bool:
    baba = 5
    return baba in karte_u_boji and len(karte_u_boji) > 2


def gabula(karte_u_boji: list[Card]) -> bool:
    return 5 in karte_u_boji and 6 in karte_u_boji


def analiziraj_boju(karte_u_boji: list[Card]) -> dict[str, int | bool]:
    return {
        "karte_u_boji": human_readable_cards_of_suit(karte_u_boji),
        "sigurni_stihovi": broj_sigurnih_stihova(karte_u_boji),
        "drugi_kralj": drugi_kralj(karte_u_boji),
        "treca_baba": treca_baba(karte_u_boji),
        "gabula": gabula(karte_u_boji),
    }


def analiziraj_ruku(hand: Hand):
    analiza_po_bojama = {}
    for boja in BOJE:
        analiza = analiziraj_boju(boja)
        analiza_po_bojama[boja] = analiza
    return analiza_po_bojama
