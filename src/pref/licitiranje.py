from pref.types import Card, Hand, Igra, Literal

Suit = Literal["Pik", "Karo", "Herc", "Tref"]


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


def stihovi_u_bojama(hand: Hand) -> dict[Suit, int]:
    stihovi_u_boji: dict[Suit, int] = {}
    boje: list[Suit] = ["Pik", "Karo", "Herc", "Tref"]
    for boja in boje:
        karte_u_boji = get_cards_of_suit(hand, boja)
        stihovi_u_boji[boja] = broj_sigurnih_stihova(karte_u_boji)

    return stihovi_u_boji


def zovi_na_6(hand: Hand) -> Igra | None:
    # TODO: ovo nikad ne zove betl, uvijek zove dalje
    sigurni_stihovi = stihovi_u_bojama(hand)

    stih_u_svakoj_boji = all(stihovi > 0 for stihovi in sigurni_stihovi.values())
    ukupno_stihova = sum(sigurni_stihovi.values())

    # ne zovi ak nemas 6 stihova
    if ukupno_stihova < 6:
        return None

    # ak imas 6 sigurnih i po jedan u svakoj, zovi sanac
    if stih_u_svakoj_boji:
        return "Sanac"

    barem_3 = any(stihovi >= 3 for stihovi in sigurni_stihovi.values())
    najbolja_boja = max(sigurni_stihovi.items(), key=lambda x: x[1])[0]

    # ak imas barem 3 stiha u jednoj boji i barem 6 sveukupno,
    #  onda zovi najbolju boju
    if barem_3:
        return najbolja_boja

    # dosli smo do tu: imamo 6 ili vise stihova, al ne u svakoj boji, i ni u jednoj boji 3
    # znaci: imamo 2 stiha u 3 boje
    # za sad cemo rec dalje
    return None
