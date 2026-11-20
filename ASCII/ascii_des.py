"""Représentation ASCII de deux dés à six faces."""


def _lignes_de(valeur: int) -> list:
    """Construit les cinq lignes qui dessinent une face de dé."""

    if valeur == 1:
        face: list = ["┌─────┐", "│     │", "│  ●  │", "│     │", "└─────┘"]
    elif valeur == 2:
        face = ["┌─────┐", "│●    │", "│     │", "│    ●│", "└─────┘"]
    elif valeur == 3:
        face = ["┌─────┐", "│●    │", "│  ●  │", "│    ●│", "└─────┘"]
    elif valeur == 4:
        face = ["┌─────┐", "│●   ●│", "│     │", "│●   ●│", "└─────┘"]
    elif valeur == 5:
        face = ["┌─────┐", "│●   ●│", "│  ●  │", "│●   ●│", "└─────┘"]
    else:
        face = ["┌─────┐", "│●   ●│", "│●   ●│", "│●   ●│", "└─────┘"]

    return face


def afficher_des(de1: int, de2: int) -> None:
    """Affiche les deux dés côte à côte en couleur."""

    lignes_de1: list = _lignes_de(de1)
    lignes_de2: list = _lignes_de(de2)

    print("\033[2J\033[H", end="")
    print("             DUEL DE DÉS")
    print("       \033[96mDÉ 1\033[0m             \033[96mDÉ 2\033[0m")
    print()

    for ligne in range(len(lignes_de1)):
        print("       \033[97;44m" + lignes_de1[ligne] + "\033[0m     "
              + "\033[97;44m" + lignes_de2[ligne] + "\033[0m")

    print()
