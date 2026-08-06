from pref.stihovi import stihovi_u_bojama
from pref.types import Hand, Igra, Licitacija, Player
from pref.utils import prethodni, sljedeci


def zovi_na_6(hand: Hand) -> Igra | None:
    # TODO: ovo nikad ne zove betl
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


def vrijednost_igre(igra: Igra):
    return {"Pik": 2, "Karo": 3, "Herc": 4, "Tref": 5, "Betl": 6, "Sanac": 7}[igra]


def zeli_licitirat(
    igrac: Player,
    ciljana_igra: Igra | None,
    prvi_na_stihu: Player,
    zadnja_licitacija: int,
    zadnji_licitirao: Player,
) -> bool:
    # ak zeli rec dalje, onda ne moze licitirat
    if ciljana_igra is None:
        return False
    if moze_rec_ja_bi(igrac, prvi_na_stihu, zadnji_licitirao):
        return vrijednost_igre(ciljana_igra) >= zadnja_licitacija
    else:
        return vrijednost_igre(ciljana_igra) > zadnja_licitacija


def moze_rec_ja_bi(
    igrac: Player, prvi_na_stihu: Player, zadnji_licitirao: Player
) -> bool:
    # ak smo prvi na stihu, uvijek mozemo
    if igrac == prvi_na_stihu:
        return True
    # ak smo drugi al prethodni igrac je reko dalje, isto mozemo
    return prethodni(igrac) == prvi_na_stihu and prethodni(igrac) != zadnji_licitirao


def licitiranje(igraci: list[Hand], prvi_na_stihu: Player) -> Licitacija | None:
    # za sad: sve je automatski
    # za svakog igraca, odredit koja mu je ciljana boja
    ciljane_igre: list[Igra | None] = [zovi_na_6(igrac) for igrac in igraci]

    redoslijed = [
        prvi_na_stihu,
        sljedeci(prvi_na_stihu),
        sljedeci(sljedeci(prvi_na_stihu)),
    ]

    licitacije = []
    rekli_dalje = []

    zadnja_licitacija = 1
    zadnji_licitirao = -1  # nitko
    # prvi krug
    for igrac in redoslijed:
        if zeli_licitirat(
            igrac,
            ciljane_igre[igrac],
            prvi_na_stihu,
            zadnja_licitacija,
            zadnji_licitirao,
        ):
            zadnja_licitacija += 1  # prvi krug, nema "ja bi"
            what_say_you = (igrac, zadnja_licitacija)
            zadnji_licitirao = igrac
        else:
            what_say_you = (igrac, None)  # reko dalje
            rekli_dalje.append(igrac)
        licitacije.append(what_say_you)

    if len(rekli_dalje) == 3:
        return None  # refa

    while len(rekli_dalje) < 2:
        for igrac in redoslijed:
            if rekli_dalje[igrac]:
                continue  # skip
            if zeli_licitirat(
                igrac,
                ciljane_igre[igrac],
                prvi_na_stihu,
                zadnja_licitacija,
                zadnji_licitirao,
            ):
                if moze_rec_ja_bi(igrac, prvi_na_stihu, zadnji_licitirao):
                    what_say_you = (igrac, zadnja_licitacija)  # ja bi
                else:
                    # nema ja bi
                    zadnja_licitacija += 1
                    what_say_you = (igrac, zadnja_licitacija)
                zadnji_licitirao = igrac
            else:
                what_say_you = (igrac, None)  # dalje
                if igrac not in rekli_dalje:
                    rekli_dalje.append(igrac)
            licitacije.append(what_say_you)

        # zas je ovo tak jebeno komplicirano

    return licitacije


def pobjednik_lic(lic: Licitacija) -> Player:
    for what_say_you in lic[::-1]:
        if what_say_you[1] is not None:
            return what_say_you[0]
    raise RuntimeError("Bila je refa")
