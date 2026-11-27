"""
ascii_discretion : le dessin de la scène « sortie discrète » (le jeu est dans la page 11).

    scene(pas, total, curseur, zone, erreurs, erreurs_max, message, reussi)
        retourne l'écran complet : les empreintes de pas qui avancent en zigzag,
        la barre de précision avec son curseur, un message et la jauge de bruit.
"""

from ASCII.ascii_gameover import fg

CYAN: tuple = (40, 205, 225)
OR: tuple = (255, 205, 70)
BLANC: tuple = (255, 255, 255)
VERT: tuple = (120, 255, 160)
ROUGE: tuple = (255, 90, 90)
GRIS: tuple = (80, 60, 120)
SOL: tuple = (70, 40, 110)

LARGEUR_BARRE: int = 41      # nombre de cases de la barre
CENTRE: int = 20             # case du milieu de la zone verte
COLONNE_BARRE: int = 11      # colonne de l'écran où commence la barre

# Une empreinte (talon puis semelle), tournée vers la droite
EMPREINTE: list = [
    "▗▄▖ ▗▄▄▄▖",
    "▐█▌ ▐███▌",
    "▝▀▘ ▝▀▀▀▘",
]


def colonne(n: int) -> str:
    """Code ANSI qui place le curseur du terminal à la colonne n."""
    return f"\033[{n}G"


def scene(pas: int, total: int, curseur: int, zone: int, erreurs: int,
          erreurs_max: int, message: str, reussi: bool) -> str:
    """Retourne l'écran de la scène (chaque ligne est effacée avant d'être redessinée)."""
    lignes = ["", fg(SOL) + "═" * 61]

    # les pas avancent de gauche à droite, un pied en haut puis un pied en bas
    pieds = ["", "", "", "", "", ""]
    for i in range(total):
        couleur = GRIS
        if i < pas:
            couleur = CYAN
        elif i == pas:
            couleur = BLANC
        for r in range(len(EMPREINTE)):
            pieds[r + 3 * (i % 2)] += colonne(5 + 6 * i) + fg(couleur) + EMPREINTE[r]
    lignes += pieds

    lignes.append(fg(SOL) + "═" * 61)
    lignes.append("")

    lignes.append(colonne(COLONNE_BARRE + curseur) + fg(BLANC) + "▼")
    barre = colonne(COLONNE_BARRE)
    for i in range(LARGEUR_BARRE):
        ecart = abs(i - CENTRE)
        if ecart <= zone:
            barre += fg(VERT) + "█"
        else:
            barre += fg((40 + ecart * 2, 25 + ecart, 80 + ecart * 2)) + "█"
    lignes.append(barre)

    couleur_message = OR
    if message == "":
        message = "ESPACE quand le curseur est dans le vert"
    elif reussi:
        couleur_message = VERT
    else:
        couleur_message = ROUGE
    lignes.append(colonne(max(1, 1 + (61 - len(message)) // 2)) + fg(couleur_message) + message)

    lignes.append("")
    jauge = fg(ROUGE) + "█" * erreurs + fg(GRIS) + "░" * (erreurs_max + 1 - erreurs)
    lignes.append(colonne(11) + fg(CYAN) + "BRUIT " + jauge
                  + colonne(40) + fg(BLANC) + "pas " + str(pas) + " / " + str(total))

    return "\033[2K" + "\n\033[2K".join(lignes) + "\033[J"
