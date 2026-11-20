
import random
import time


ROULETTE = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34,
    6, 27, 13, 36, 11, 30, 8, 23, 10, 5,
    24, 16, 33, 1, 20, 14, 31, 9, 22, 18,
    29, 7, 28, 12, 35, 3, 26
]


def afficher_roulette(position: int) -> None:
    """Affiche la roulette avec les numéros autour de la roue."""

    largeur: int = len(ROULETTE)

    n1: int = ROULETTE[position % largeur]
    n2: int = ROULETTE[(position + 5) % largeur]
    n3: int = ROULETTE[(position + 10) % largeur]
    n4: int = ROULETTE[(position + 15) % largeur]
    n5: int = ROULETTE[(position + 20) % largeur]
    n6: int = ROULETTE[(position + 25) % largeur]
    n7: int = ROULETTE[(position + 30) % largeur]
    n8: int = ROULETTE[(position + 35) % largeur]

    print("\033[H\033[J", end="")
    print("       ╔══════════════════════╗")
    print("       ║     ROULETTE         ║")
    print("       ╚══════════════════════╝")
    print()
    print("             ▼")
    print()
    print("       ┌─────────────────┐")
    print("       │       " + str(n1).rjust(2) + "        │")
    print("       │                 │")
    print("   " + str(n8).rjust(2) + "  │       ◉         │  " + str(n2))
    print("       │                 │")
    print("   " + str(n7).rjust(2) + "  │                 │  " + str(n3))
    print("       │                 │")
    print("       │       " + str(n4).rjust(2) + "        │")
    print("       └─────────────────┘")
    print()
    print("          La bille tourne...")


def ascii_roulette() -> int:
    """Anime la roulette et renvoie le numéro gagnant."""

    numero_gagnant: int = random.randint(0, 36)

    position: int = random.randint(0, 36)
    nb_tours: int = 45

    index_gagnant: int = ROULETTE.index(numero_gagnant)

    distance: int = (index_gagnant - position) % 37
    distance = distance + 37 * 3

    for etape in range(nb_tours):
        afficher_roulette(position)

        position = position + distance // nb_tours

        distance = distance - distance // nb_tours

        time.sleep(0.04 + etape * 0.008)

    afficher_roulette(index_gagnant)

    print()
    print("     ★ NUMERO GAGNANT :", numero_gagnant, "★")
    print()

    return numero_gagnant
