"""
Animation ASCII d'une roulette française.
ascii_roulette() renvoie le numéro gagnant, entre 0 et 36.
"""
import random
import time

ROULETTE: list = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26
]


def afficher_roulette(position: int, numero_final: int = -1) -> None:
    """Affiche une représentation ASCII de la roulette."""

    taille: int = len(ROULETTE)
    n1: int = ROULETTE[position % taille]
    n2: int = ROULETTE[(position + 5) % taille]
    n3: int = ROULETTE[(position + 10) % taille]
    n4: int = ROULETTE[(position + 15) % taille]
    n5: int = ROULETTE[(position + 20) % taille]
    n6: int = ROULETTE[(position + 25) % taille]
    n7: int = ROULETTE[(position + 30) % taille]
    n8: int = ROULETTE[(position + 35) % taille]

    print("\033[2J\033[H", end="")
    print("          LE GRAND CASINO ROYAL")
    print("               ROULETTE")
    print()
    print("                   ▼")
    print("          .-----------------.")
    print("       .-'                   '-.")
    print("     .'       " + str(n1).rjust(2) + "                '.")
    print("    /   " + str(n8).rjust(2) + "                   " + str(n2).rjust(2) + "   \\")
    print("   |                           |")
    print("   |   " + str(n7).rjust(2) + "        ( O )        " + str(n3).rjust(2) + "   |")
    print("   |                           |")
    print("    \\   " + str(n6).rjust(2) + "                   " + str(n4).rjust(2) + "   /")
    print("     '.       " + str(n5).rjust(2) + "                .'")
    print("       '-.                 .-'")
    print("          '---------------'")
    print()
    if numero_final == -1:
        print("             LA BILLE TOURNE...")
    else:
        print("          NUMERO GAGNANT :", numero_final)


def ascii_roulette() -> int:
    """Fait tourner la roulette et renvoie le numéro gagnant."""

    index_depart: int = random.randint(0, 36)
    index_gagnant: int = random.randint(0, 36)

    distance: int = (index_gagnant - index_depart) % 37
    distance = distance + 37 * 3

    etape: int = 0
    while etape <= distance:
        position: int = (index_depart + etape) % 37
        afficher_roulette(position)
        pause: float = 0.035 + (etape / distance) * 0.18
        time.sleep(pause)
        etape = etape + 1

    numero_gagnant: int = ROULETTE[index_gagnant]
    afficher_roulette(index_gagnant, numero_gagnant)
    print()
    print("       La bille s'est arretee !")
    print()
    return numero_gagnant
