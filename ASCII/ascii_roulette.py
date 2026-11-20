"""Affichage en couleur de la roue de roulette française."""


def _case_coloree(numero: int, rouges: list) -> str:
    """Retourne le numéro encadré par les couleurs de sa case."""

    if numero == 0:
        couleur: str = "\033[97;42m"  # blanc sur vert
    elif numero in rouges:
        couleur = "\033[97;41m"      # blanc sur rouge
    else:
        couleur = "\033[97;40m"      # blanc sur noir

    res: str = couleur + " " + str(numero).rjust(2) + " \033[0m"
    return res


def afficher_roulette(roue: list, rouges: list, position: int,
                      numero_final: int = -1) -> None:
    """Dessine la roue à la position donnée, sans effectuer de tirage."""

    taille: int = len(roue)
    n1: str = _case_coloree(roue[position % taille], rouges)
    n2: str = _case_coloree(roue[(position + 5) % taille], rouges)
    n3: str = _case_coloree(roue[(position + 10) % taille], rouges)
    n4: str = _case_coloree(roue[(position + 15) % taille], rouges)
    n5: str = _case_coloree(roue[(position + 20) % taille], rouges)
    n6: str = _case_coloree(roue[(position + 25) % taille], rouges)
    n7: str = _case_coloree(roue[(position + 30) % taille], rouges)
    n8: str = _case_coloree(roue[(position + 35) % taille], rouges)

    print("\033[2J\033[H", end="")
    print("              LE GRAND CASINO ROYAL")
    print("                       ROULETTE")
    print()
    print("                          ▼")
    print("                 .-----------------.")
    print("              .-'                   '-.")
    print("            .'          " + n1 + "          '.")
    print("           /   " + n8 + "                 " + n2 + "   \\")
    print("          |                               |")
    print("          |   " + n7 + "       (  O  )       " + n3 + "   |")
    print("          |                               |")
    print("           \\   " + n6 + "                 " + n4 + "   /")
    print("            '.          " + n5 + "          .'")
    print("              '-.                 .-'")
    print("                 '---------------'")
    print()

    if numero_final == -1:
        print("                  LA BILLE TOURNE...")
    else:
        print("                NUMÉRO GAGNANT : " + _case_coloree(numero_final, rouges))
