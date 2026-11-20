"""
ascii_roulette : roue de roulette en pixel art (tirage animé) + écran de résultat.

Deux fonctions à utiliser :
    animer_tirage(roue, index_gagnant)
        la roue néon tourne, la bille ralentit puis se pose dans la case gagnante,
        qui se retrouve sous le repère ▼ et clignote.
    ecran_resultat(numero, gain_net, mise, argent)
        écran JACKPOT (zéro vert), GAGNÉ (pluie de confettis), PARTAGE ou PERDU.

Nécessite un terminal qui gère les couleurs ANSI 24 bits (terminal Windows, VS Code,
Linux, macOS) d'au moins 61 colonnes sur 26 lignes. Sinon (IDLE, Thonny...), une
version texte simple est affichée.

Technique : comme pour le crâne du GAME OVER, deux pixels sont dessinés dans un seul
caractère "▀" (moitié haute = couleur du texte, moitié basse = couleur du fond).
"""

import colorsys
import math
import random
import time
from typing import Callable

from ASCII.ascii_gameover import bg, couleurs_disponibles, fg, RESET


ROUGES: list = [
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
]

# Palette (R, V, B)
FOND: tuple = (13, 2, 34)
ROSE: tuple = (255, 60, 170)
CYAN: tuple = (40, 205, 225)
OR: tuple = (255, 205, 70)
BLANC: tuple = (255, 255, 255)
CASE_ROUGE: tuple = (215, 25, 60)
CASE_NOIRE: tuple = (52, 48, 72)
CASE_VERTE: tuple = (0, 170, 85)
PISTE: tuple = (35, 12, 55)
BRUIT: tuple = (90, 20, 60)

# Dimensions de l'image de la roue (en pixels : 2 pixels par ligne de terminal)
LARGEUR: int = 61
HAUTEUR: int = 44
CENTRE_X: float = 30.5
CENTRE_Y: float = 22.0
COLONNE_REPERE: int = 30

# Police 5 x 7 pour les chiffres du résultat
POLICE: dict = {
    "0": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": ["..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."],
}

LARGEUR_ECRAN: int = 61
HAUTEUR_ECRAN: int = 15
SIGNES_BRUIT: str = "#@$%&*01"
SIGNES_CONFETTIS: str = "✦*▪·◆"
# les confettis évitent les lignes de texte (bannière, pastille, gain, argent)
LIGNES_CONFETTIS: list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]


# ----------------------------------------------------------------------------
# Petits outils de couleur
# ----------------------------------------------------------------------------

def melanger(a: tuple, b: tuple, t: float) -> tuple:
    """Mélange deux couleurs : t = 0 donne a, t = 1 donne b."""
    res = (int(a[0] + (b[0] - a[0]) * t),
           int(a[1] + (b[1] - a[1]) * t),
           int(a[2] + (b[2] - a[2]) * t))
    return res


def eclaircir(c: tuple, k: float) -> tuple:
    """Multiplie la luminosité d'une couleur (k < 1 assombrit, k > 1 éclaircit)."""
    res = (min(255, int(c[0] * k)), min(255, int(c[1] * k)), min(255, int(c[2] * k)))
    return res


def couleur_case(numero: int) -> tuple:
    """Couleur de la case d'un numéro : vert pour 0, rouge ou noir sinon."""
    res = CASE_NOIRE
    if numero == 0:
        res = CASE_VERTE
    elif numero in ROUGES:
        res = CASE_ROUGE
    return res


def nom_couleur(numero: int) -> str:
    """Nom de la couleur d'un numéro."""
    res = "NOIR"
    if numero == 0:
        res = "VERT"
    elif numero in ROUGES:
        res = "ROUGE"
    return res


def arc_en_ciel(t: float) -> tuple:
    """Couleur de l'arc-en-ciel pour t entre 0 et 1."""
    r, v, b = colorsys.hsv_to_rgb(t * 0.83, 0.8, 1.0)
    return (int(r * 255), int(v * 255), int(b * 255))


# ----------------------------------------------------------------------------
# Lignes de texte colorées (titre, pied de page)
# ----------------------------------------------------------------------------

def ligne_composee(morceaux: list, largeur: int) -> str:
    """Centre des morceaux (texte, couleur du texte, couleur du fond) sur une ligne."""
    total = 0
    for morceau in morceaux:
        total += len(morceau[0])
    marge = (largeur - total) // 2
    res = bg(FOND) + " " * marge
    for morceau in morceaux:
        res += fg(morceau[1]) + bg(morceau[2]) + morceau[0]
    res += bg(FOND) + " " * (largeur - marge - total) + RESET
    return res


def ligne_degrade(texte: str, largeur: int, couleur: Callable) -> str:
    """Ligne centrée dont chaque lettre prend la couleur donnée par couleur(t)."""
    morceaux = []
    for i in range(len(texte)):
        morceaux.append((texte[i], couleur(i / max(1, len(texte) - 1)), FOND))
    return ligne_composee(morceaux, largeur)


def ligne_repere(largeur: int) -> str:
    """Ligne contenant le repère ▼ au-dessus de la roue."""
    res = bg(FOND) + " " * COLONNE_REPERE + fg(OR) + "▼"
    res += bg(FOND) + " " * (largeur - COLONNE_REPERE - 1) + RESET
    return res


# ----------------------------------------------------------------------------
# La roue vue du dessus
# ----------------------------------------------------------------------------

def calculer_polaire() -> list:
    """Pour chaque pixel de l'image : sa distance au centre et son angle."""
    res = []
    for y in range(HAUTEUR):
        ligne = []
        for x in range(LARGEUR):
            dx = x + 0.5 - CENTRE_X
            dy = y + 0.5 - CENTRE_Y
            ligne.append((math.hypot(dx, dy), math.atan2(dy, dx)))
        res.append(ligne)
    return res


def calculer_etoiles() -> dict:
    """Quelques étoiles fixes dans le fond (même ciel à chaque image)."""
    hasard = random.Random(7)
    res = {}
    for i in range(40):
        x = hasard.randrange(LARGEUR)
        y = hasard.randrange(HAUTEUR)
        couleur = CYAN
        if hasard.random() < 0.5:
            couleur = ROSE
        res[(x, y)] = melanger(FOND, couleur, 0.35 + hasard.random() * 0.4)
    return res


POLAIRE: list = calculer_polaire()
ETOILES: dict = calculer_etoiles()


def couleur_pixel(roue: list, x: int, y: int, rotation: float,
                  case_clignote: int, clignote: float) -> tuple:
    """Couleur d'un pixel de la roue (sans la bille)."""
    res = ETOILES.get((x, y), FOND)
    r = POLAIRE[y][x][0]
    a = POLAIRE[y][x][1]

    if r <= 22:
        tour = ((a - rotation) / (2 * math.pi)) % 1.0   # position dans le tour, de 0 à 1
        position = tour * len(roue)
        numero_case = int(position)
        reste = position - numero_case

        if r > 21:
            res = ROSE                                   # liseré néon
        elif r > 19.5:
            res = eclaircir((240, 190, 60), 0.8 + 0.2 * math.sin(a * 3))   # bord doré
        elif r > 17.5:
            res = PISTE                                  # piste de la bille
        elif r > 12:
            if reste < 0.06 or reste > 0.94:
                res = (205, 155, 45)                     # séparation dorée
            else:
                c = couleur_case(roue[numero_case])
                if numero_case == case_clignote:
                    c = melanger(c, OR, clignote)
                res = eclaircir(c, 0.72 + 0.28 * (r - 12) / 5.5)
        elif r > 10.5:
            res = (240, 190, 60)                         # anneau doré
        elif r > 3.5:
            if r > 9.2:
                res = CYAN                               # anneau néon
            else:
                rayon_colore = (75, 25, 125)
                if int(tour * 8) % 2 == 1:
                    rayon_colore = (30, 70, 130)
                res = eclaircir(rayon_colore, 0.7 + r / 20)
        elif r < 2:
            res = (255, 235, 140)                        # cœur de la roue
        else:
            res = (205, 150, 40)
    return res


def image_roue(roue: list, rotation: float, billes: list,
               case_clignote: int, clignote: float) -> list:
    """Construit l'image (liste de lignes de pixels) de la roue et des billes."""
    image = []
    for y in range(HAUTEUR):
        ligne = []
        for x in range(LARGEUR):
            ligne.append(couleur_pixel(roue, x, y, rotation, case_clignote, clignote))
        image.append(ligne)

    # billes : (angle, distance au centre, rayon, couleur)
    for bille in billes:
        bx = CENTRE_X + bille[1] * math.cos(bille[0])
        by = CENTRE_Y + bille[1] * math.sin(bille[0])
        for y in range(max(0, int(by - bille[2]) - 1), min(HAUTEUR, int(by + bille[2]) + 2)):
            for x in range(max(0, int(bx - bille[2]) - 1), min(LARGEUR, int(bx + bille[2]) + 2)):
                if math.hypot(x + 0.5 - bx, y + 0.5 - by) < bille[2]:
                    image[y][x] = bille[3]
    return image


def lignes_image(image: list) -> list:
    """Transforme l'image en lignes de terminal (2 pixels par caractère ▀)."""
    res = []
    for y in range(0, HAUTEUR, 2):
        ligne = ""
        for x in range(LARGEUR):
            ligne += fg(image[y][x]) + bg(image[y + 1][x]) + "▀"
        res.append(ligne + RESET)
    return res


def afficher_image_roue(image: list, titre: str, pied: str) -> None:
    """Redessine tout l'écran : titre, repère, roue, pied de page."""
    lignes = [titre, ligne_repere(LARGEUR)] + lignes_image(image) + [pied]
    print("\033[H" + "\n".join(lignes))


# ----------------------------------------------------------------------------
# Mouvement de la bille et de la roue
# ----------------------------------------------------------------------------

def angle_roue(t: float, rotation_finale: float) -> float:
    """Rotation de la roue à l'instant t (0 à 1) : elle ralentit jusqu'à l'arrêt."""
    freinage = 1 - (1 - t) ** 2
    return rotation_finale - 2 * math.pi * 1.2 * (1 - freinage)


def angle_bille(t: float, rotation_finale: float, centre_case: float,
                tours_bille: float) -> float:
    """Angle de la bille : elle tourne dans l'autre sens que la roue, puis se pose."""
    freinage = 1 - (1 - t) ** 3
    relatif = 2 * math.pi * tours_bille * (1 - freinage)
    return angle_roue(t, rotation_finale) + centre_case + relatif


def distance_bille(t: float) -> float:
    """Distance de la bille au centre : sur la piste, puis elle tombe dans la case."""
    d = min(1.0, max(0.0, (t - 0.7) / 0.3))
    lisse = d * d * (3 - 2 * d)
    res = 18.5 - 3.5 * lisse + 0.9 * abs(math.sin(d * 3 * math.pi)) * (1 - d)
    return res


def animation_couleur(roue: list, index_gagnant: int) -> None:
    """Tirage animé en pixel art."""
    pas = 2 * math.pi / len(roue)
    centre_case = (index_gagnant + 0.5) * pas
    # à la fin, la case gagnante est tout en haut, sous le repère ▼
    rotation_finale = -math.pi / 2 - centre_case
    tours_bille = 5 + random.random() * 1.5
    numero = roue[index_gagnant]
    nb_images = 60

    titre = ligne_degrade("★  R O U L E T T E  ★", LARGEUR,
                          lambda t: melanger(ROSE, CYAN, t))

    print("\033[2J", end="")
    for i in range(nb_images + 1):
        t = i / nb_images
        rotation = angle_roue(t, rotation_finale)
        billes = []
        if t < 0.7:
            # traînée lumineuse derrière la bille
            for k in range(5, 0, -1):
                tk = max(0.0, t - 0.012 * k)
                billes.append((angle_bille(tk, rotation_finale, centre_case, tours_bille),
                               distance_bille(tk), 1.3,
                               melanger(PISTE, CYAN, 1 - k / 6)))
        billes.append((angle_bille(t, rotation_finale, centre_case, tours_bille),
                       distance_bille(t), 1.9, BLANC))

        image = image_roue(roue, rotation, billes, -1, 0.0)
        pulsation = melanger(CYAN, BLANC, abs(math.sin(i / 4)))
        pied = ligne_composee([("LA BILLE TOURNE...", pulsation, FOND)], LARGEUR)
        afficher_image_roue(image, titre, pied)
        time.sleep(0.04)

    # la case gagnante clignote
    pied = ligne_composee([("NUMÉRO GAGNANT : ", OR, FOND),
                           (" " + str(numero) + " ", BLANC, couleur_case(numero))], LARGEUR)
    for j in range(8):
        clignote = 0.9
        if j % 2 == 1:
            clignote = 0.25
        billes = [(-math.pi / 2, 15.0, 1.9, BLANC)]
        image = image_roue(roue, rotation_finale, billes, index_gagnant, clignote)
        afficher_image_roue(image, titre, pied)
        time.sleep(0.12)


def animation_simple(roue: list, index_gagnant: int) -> None:
    """Version texte pour les terminaux sans couleurs."""
    print()
    print("La bille tourne", end="", flush=True)
    for i in range(8):
        time.sleep(0.25)
        print(".", end="", flush=True)
    print()
    print("Numéro gagnant :", roue[index_gagnant])


def animer_tirage(roue: list, index_gagnant: int) -> None:
    """Anime le tirage et s'arrête sur la case index_gagnant de la roue."""
    if couleurs_disponibles():
        animation_couleur(roue, index_gagnant)
    else:
        animation_simple(roue, index_gagnant)


# ----------------------------------------------------------------------------
# Écran de résultat
# ----------------------------------------------------------------------------

# un style par issue : bannière, dégradé des chiffres, ombre, confettis ou bruit
STYLES: dict = {
    "jackpot": {"banniere": "★ ★ ★  J A C K P O T  ★ ★ ★", "debut": None, "fin": None,
                "haut": OR, "bas": ROSE, "ombre": (20, 70, 110), "confettis": True},
    "gagne": {"banniere": "★ ★ ★   G A G N É   ★ ★ ★", "debut": OR, "fin": ROSE,
              "haut": OR, "bas": ROSE, "ombre": (20, 70, 110), "confettis": True},
    "partage": {"banniere": "P A R T A G E", "debut": (255, 170, 60), "fin": (200, 60, 40),
                "haut": (255, 180, 70), "bas": (200, 80, 50), "ombre": (70, 25, 12),
                "confettis": False},
    "perdu": {"banniere": "P E R D U", "debut": (255, 90, 90), "fin": (110, 20, 45),
              "haut": (255, 110, 110), "bas": (170, 40, 70), "ombre": (60, 12, 40),
              "confettis": False},
}


def issue(numero: int, gain_net: float) -> str:
    """Retourne jackpot, gagne, partage ou perdu."""
    res = "perdu"
    if gain_net > 0 and numero == 0:
        res = "jackpot"
    elif gain_net > 0:
        res = "gagne"
    elif numero == 0:
        res = "partage"
    return res


def grille_vide() -> list:
    """Grille de cases [caractère, couleur du texte, couleur du fond]."""
    res = []
    for y in range(HAUTEUR_ECRAN):
        ligne = []
        for x in range(LARGEUR_ECRAN):
            ligne.append([" ", BLANC, FOND])
        res.append(ligne)
    return res


def ecrire(grille: list, y: int, x: int, texte: str, couleur: tuple, fond: tuple) -> None:
    """Écrit un texte dans la grille."""
    for i in range(len(texte)):
        grille[y][x + i] = [texte[i], couleur, fond]


def ecrire_degrade(grille: list, y: int, texte: str, couleur: Callable) -> None:
    """Écrit un texte centré, lettre par lettre, avec la couleur couleur(t)."""
    x = (LARGEUR_ECRAN - len(texte)) // 2
    for i in range(len(texte)):
        grille[y][x + i] = [texte[i], couleur(i / max(1, len(texte) - 1)), FOND]


def dessiner_nombre(grille: list, y0: int, numero: int, style: dict) -> None:
    """Dessine le numéro en chiffres géants (dégradé + ombre)."""
    chiffres = str(numero)
    largeur = len(chiffres) * 10 + (len(chiffres) - 1) * 2
    x0 = (LARGEUR_ECRAN - largeur) // 2

    for passage in range(2):
        for numero_chiffre in range(len(chiffres)):
            motif = POLICE[chiffres[numero_chiffre]]
            for dy in range(7):
                for dx in range(5):
                    if motif[dy][dx] == "#":
                        for moitie in range(2):
                            x = x0 + numero_chiffre * 12 + dx * 2 + moitie
                            if passage == 0:
                                grille[y0 + dy + 1][x + 2] = ["█", style["ombre"], FOND]
                            else:
                                couleur = melanger(style["haut"], style["bas"], dy / 6)
                                grille[y0 + dy][x] = ["█", couleur, FOND]


def construire_ecran(numero: int, gain_net: float, mise: int, argent: float) -> list:
    """Construit la grille de l'écran de résultat."""
    genre = issue(numero, gain_net)
    style = STYLES[genre]
    grille = grille_vide()

    if style["debut"] is None:
        ecrire_degrade(grille, 0, style["banniere"], arc_en_ciel)
    else:
        ecrire_degrade(grille, 0, style["banniere"],
                       lambda t: melanger(style["debut"], style["fin"], t))

    dessiner_nombre(grille, 2, numero, style)

    pastille = "  " + str(numero) + "  " + nom_couleur(numero) + "  "
    ecrire(grille, 11, (LARGEUR_ECRAN - len(pastille)) // 2, pastille, BLANC,
           couleur_case(numero))

    if genre == "perdu":
        message = "PERDU : -" + f"{mise:g}" + " €"
    elif genre == "partage":
        message = "PARTAGE : tu perds la moitié de ta mise (-" + f"{mise / 2:g}" + " €)"
    else:
        message = "BÉNÉFICE : +" + f"{gain_net:g}" + " €"
    ecrire_degrade(grille, 13, message, lambda t: melanger(BLANC, OR, 0.4 + 0.6 * t))

    ecrire_degrade(grille, 14, "Ton argent : " + f"{argent:g}" + " €",
                   lambda t: melanger(CYAN, ROSE, t))
    return grille


def afficher_grille(grille: list) -> None:
    """Redessine l'écran de résultat."""
    lignes = []
    for ligne in grille:
        texte = ""
        for case in ligne:
            texte += fg(case[1]) + bg(case[2]) + case[0]
        lignes.append(texte + RESET)
    print("\033[H" + "\n".join(lignes))


def resultat_couleur(numero: int, gain_net: float, mise: int, argent: float) -> None:
    """Écran de résultat animé : confettis si gagné, parasites si perdu."""
    genre = issue(numero, gain_net)
    style = STYLES[genre]
    base = construire_ecran(numero, gain_net, mise, argent)

    palette = [CYAN, ROSE, OR, (120, 255, 160), BLANC]
    confettis = []
    for i in range(70):
        confettis.append([random.randrange(LARGEUR_ECRAN), random.choice(LIGNES_CONFETTIS),
                          random.choice(SIGNES_CONFETTIS), random.choice(palette)])

    nb_images = 6
    if style["confettis"]:
        nb_images = 14

    time.sleep(0.8)
    print("\033[2J", end="")
    for j in range(nb_images):
        grille = []
        for ligne in base:
            grille.append([list(case) for case in ligne])

        if style["confettis"]:
            # les confettis tombent et finissent par se poser à leur place finale
            for c in confettis:
                y = int(c[1] - (nb_images - 1 - j) * 1.5)
                if y in LIGNES_CONFETTIS and grille[y][c[0]][0] == " ":
                    grille[y][c[0]] = [c[2], c[3], FOND]
        else:
            # parasites qui s'éteignent peu à peu
            for i in range(int(60 * (1 - j / (nb_images - 1)))):
                y = random.randrange(HAUTEUR_ECRAN)
                x = random.randrange(LARGEUR_ECRAN)
                if grille[y][x][0] == " ":
                    grille[y][x] = [random.choice(SIGNES_BRUIT), BRUIT, FOND]

        afficher_grille(grille)
        time.sleep(0.08)


def resultat_simple(numero: int, gain_net: float, mise: int, argent: float) -> None:
    """Version texte pour les terminaux sans couleurs."""
    genre = issue(numero, gain_net)
    print()
    print("Résultat :", numero, "(" + nom_couleur(numero).lower() + ")")
    if genre == "perdu":
        print("Perdu ! Tu perds", mise, "euros.")
    elif genre == "partage":
        print("Le zéro sort : la règle du partage te fait perdre", mise / 2, "euros.")
    else:
        print("Bravo ! Tu gagnes", gain_net, "euros de bénéfice.")


def ecran_resultat(numero: int, gain_net: float, mise: int, argent: float) -> None:
    """Affiche l'écran de résultat (jackpot, gagné, partage ou perdu)."""
    if couleurs_disponibles():
        resultat_couleur(numero, gain_net, mise, argent)
    else:
        resultat_simple(numero, gain_net, mise, argent)
