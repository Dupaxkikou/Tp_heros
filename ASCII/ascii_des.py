"""
ascii_des : deux dés en pixel art qui roulent sur un tapis néon + écran de résultat.

Deux fonctions à utiliser :
    animer_lancer(de1, de2)
        les dés rebondissent et tournent sur le tapis, ralentissent puis
        s'arrêtent sur les faces de1 et de2 (de 1 à 6) et s'illuminent.
    ecran_resultat_des(de1, de2, gain_net, mise, argent)
        écran JACKPOT (gros gain), GAGNÉ (confettis) ou PERDU, avec le total en
        chiffres géants.

Nécessite un terminal qui gère les couleurs ANSI 24 bits d'au moins 61 colonnes
sur 21 lignes. Sinon (IDLE, Thonny...), une version texte simple est affichée.

Même technique que la roulette : deux pixels par caractère "▀".
"""

import math
import random
import time

from ASCII.ascii_gameover import couleurs_disponibles
from ASCII.ascii_roulette import (BLANC, CYAN, FOND, OR, ROSE, animer_ecran, dessiner_nombre,
                                  ecrire, ecrire_degrade, eclaircir, grille_vide,
                                  ligne_composee, ligne_degrade, lignes_image, melanger,
                                  LARGEUR_ECRAN, STYLES)


LARGEUR: int = 61
HAUTEUR: int = 36            # en pixels : 2 pixels par ligne de terminal
DEMI_DE: float = 8.5         # un dé fait 17 pixels de côté
CORPS_DE: tuple = (205, 25, 55)
VIOLET: tuple = (90, 30, 140)

# Position des points sur chaque face (coordonnées de -1 à 1)
POINTS: dict = {
    1: [(0, 0)],
    2: [(-0.5, -0.5), (0.5, 0.5)],
    3: [(-0.5, -0.5), (0, 0), (0.5, 0.5)],
    4: [(-0.5, -0.5), (0.5, -0.5), (-0.5, 0.5), (0.5, 0.5)],
    5: [(-0.5, -0.5), (0.5, -0.5), (0, 0), (-0.5, 0.5), (0.5, 0.5)],
    6: [(-0.5, -0.55), (0.5, -0.55), (-0.5, 0), (0.5, 0), (-0.5, 0.55), (0.5, 0.55)],
}


# ----------------------------------------------------------------------------
# Le tapis (dessiné une seule fois)
# ----------------------------------------------------------------------------

def distance_tapis(x: float, y: float) -> float:
    """Distance (négative à l'intérieur) au bord du tapis, un rectangle arrondi."""
    demi_l = 28.5
    demi_h = 13.5
    rayon = 6.0
    qx = abs(x - 30.5) - (demi_l - rayon)
    qy = abs(y - 20.5) - (demi_h - rayon)
    res = math.hypot(max(qx, 0), max(qy, 0)) + min(max(qx, qy), 0) - rayon
    return res


def construire_tapis() -> list:
    """Image du fond : étoiles, liseré néon, bord doré et tapis vert."""
    hasard = random.Random(11)
    image = []
    for y in range(HAUTEUR):
        ligne = []
        for x in range(LARGEUR):
            ligne.append(FOND)
        image.append(ligne)
    for i in range(40):
        couleur = CYAN
        if hasard.random() < 0.5:
            couleur = ROSE
        image[hasard.randrange(HAUTEUR)][hasard.randrange(LARGEUR)] = melanger(
            FOND, couleur, 0.35 + hasard.random() * 0.4)

    for y in range(HAUTEUR):
        for x in range(LARGEUR):
            d = distance_tapis(x + 0.5, y + 0.5)
            if d <= -2:
                eloignement = math.hypot((x + 0.5 - 30.5) / 30, (y + 0.5 - 20.5) / 14)
                image[y][x] = eclaircir((12, 105, 72), 1.0 - 0.25 * eloignement)
            elif d <= -1:
                image[y][x] = (240, 190, 60)
            elif d <= 0:
                image[y][x] = ROSE
    return image


TAPIS: list = construire_tapis()


# ----------------------------------------------------------------------------
# Les dés
# ----------------------------------------------------------------------------

def couleur_de(u: float, v: float, valeur: int, lueur: bool) -> tuple | None:
    """Couleur du dé au point (u, v) de sa face (de -1 à 1), None si hors du dé."""
    res = None
    n = (abs(u) ** 5 + abs(v) ** 5) ** 0.2      # < 1 : dans le carré arrondi
    if n <= 1.0:
        if n > 0.82:
            if u + v < 0:
                res = eclaircir(CORPS_DE, 1.4)      # arête éclairée (haut gauche)
            else:
                res = eclaircir(CORPS_DE, 0.6)      # arête dans l'ombre (bas droite)
        else:
            res = eclaircir(CORPS_DE, 1.0 - 0.09 * (u + v))
        for point in POINTS[valeur]:
            if math.hypot(u - point[0], v - point[1]) < 0.2:
                res = (250, 250, 250)
    elif lueur and n <= 1.14:
        res = OR
    return res


def dessiner_ombre(image: list, cx: float, sol: float, rayon_x: float) -> None:
    """Assombrit le tapis sous un dé."""
    for y in range(int(sol) - 3, int(sol) + 4):
        for x in range(int(cx - rayon_x) - 1, int(cx + rayon_x) + 2):
            if 0 <= y < HAUTEUR and 0 <= x < LARGEUR:
                if ((x + 0.5 - cx) / rayon_x) ** 2 + ((y + 0.5 - sol) / 2.3) ** 2 <= 1:
                    image[y][x] = eclaircir(image[y][x], 0.55)


def dessiner_de(image: list, cx: float, cy: float, angle: float, valeur: int,
                lueur: bool) -> None:
    """Dessine un dé tourné d'un certain angle."""
    c = math.cos(angle)
    s = math.sin(angle)
    portee = int(DEMI_DE * 1.6) + 2
    for y in range(max(0, int(cy) - portee), min(HAUTEUR, int(cy) + portee + 1)):
        for x in range(max(0, int(cx) - portee), min(LARGEUR, int(cx) + portee + 1)):
            dx = x + 0.5 - cx
            dy = y + 0.5 - cy
            couleur = couleur_de((dx * c + dy * s) / DEMI_DE, (-dx * s + dy * c) / DEMI_DE,
                                 valeur, lueur)
            if couleur is not None:
                image[y][x] = couleur


def image_des(positions: list, hauteurs: list, angles: list, faces: list,
              lueur: bool) -> list:
    """Image du tapis avec les deux dés (ombres puis dés)."""
    image = []
    for ligne in TAPIS:
        image.append(list(ligne))
    for i in range(2):
        rayon = DEMI_DE * 1.1 * (1 - hauteurs[i] / 30)
        dessiner_ombre(image, positions[i], 30.0, rayon)
    for i in range(2):
        dessiner_de(image, positions[i], 20.0 - hauteurs[i], angles[i], faces[i], lueur)
    return image


def afficher_image_des(image: list, titre: str, pied: str) -> None:
    """Redessine tout l'écran : titre, tapis, pied de page."""
    print("\033[H" + "\n".join([titre] + lignes_image(image) + [pied]))


def animation_couleur(de1: int, de2: int) -> None:
    """Lancer animé : les dés rebondissent, tournent, puis se posent."""
    titre = ligne_degrade("★  D É S  D U  C A S I N O  ★", LARGEUR,
                          lambda t: melanger(ROSE, CYAN, t))
    finales = [de1, de2]
    faces = [random.randint(1, 6), random.randint(1, 6)]
    nb_images = 48

    print("\033[2J", end="")
    for i in range(nb_images + 1):
        t = i / nb_images
        freinage = 1 - (1 - t) ** 3
        angles = [2 * math.pi * 2.5 * (1 - freinage), -2 * math.pi * 3 * (1 - freinage)]
        hauteurs = [12 * (1 - t) * abs(math.sin(t * 10)),
                    12 * (1 - t) * abs(math.sin(t * 10 + 1.3))]
        positions = [19 + 3 * (1 - t) * math.sin(t * 14), 42 + 3 * (1 - t) * math.sin(t * 14 + 2)]

        for k in range(2):
            if t > 0.85:
                faces[k] = finales[k]
            elif random.random() < 0.7 * (1 - t):
                faces[k] = random.randint(1, 6)

        image = image_des(positions, hauteurs, angles, faces, False)
        pulsation = melanger(CYAN, BLANC, abs(math.sin(i / 4)))
        pied = ligne_composee([("LES DÉS ROULENT...", pulsation, FOND)], LARGEUR)
        afficher_image_des(image, titre, pied)
        time.sleep(0.045)

    # les dés s'illuminent
    pied = ligne_composee([("TOTAL : ", OR, FOND),
                           (" " + str(de1) + " + " + str(de2) + " = " + str(de1 + de2) + " ",
                            BLANC, VIOLET)], LARGEUR)
    for j in range(8):
        image = image_des([19, 42], [0, 0], [0, 0], finales, j % 2 == 0)
        afficher_image_des(image, titre, pied)
        time.sleep(0.12)


def animation_simple(de1: int, de2: int) -> None:
    """Version texte pour les terminaux sans couleurs."""
    print()
    print("Les dés roulent", end="", flush=True)
    for i in range(6):
        time.sleep(0.25)
        print(".", end="", flush=True)
    print()
    print("Dé 1 :", de1, "- Dé 2 :", de2, "- Total :", de1 + de2)


def animer_lancer(de1: int, de2: int) -> None:
    """Anime le lancer de deux dés qui s'arrêtent sur les faces de1 et de2."""
    if couleurs_disponibles():
        animation_couleur(de1, de2)
    else:
        animation_simple(de1, de2)


# ----------------------------------------------------------------------------
# Écran de résultat
# ----------------------------------------------------------------------------

def issue_des(gain_net: float, mise: int) -> str:
    """Retourne jackpot (gros gain), gagne ou perdu."""
    res = "perdu"
    if gain_net >= 4 * mise:
        res = "jackpot"
    elif gain_net > 0:
        res = "gagne"
    return res


def construire_ecran_des(de1: int, de2: int, gain_net: float, mise: int, argent: float) -> list:
    """Construit la grille de l'écran de résultat (même mise en page que la roulette)."""
    genre = issue_des(gain_net, mise)
    style = STYLES[genre]
    grille = grille_vide()

    if style["debut"] is None:
        ecrire_degrade(grille, 0, style["banniere"], lambda t: melanger(OR, ROSE, t))
    else:
        ecrire_degrade(grille, 0, style["banniere"],
                       lambda t: melanger(style["debut"], style["fin"], t))

    dessiner_nombre(grille, 2, de1 + de2, style)

    pastille = "  " + str(de1) + " + " + str(de2) + "  "
    ecrire(grille, 11, (LARGEUR_ECRAN - len(pastille)) // 2, pastille, BLANC, VIOLET)

    if genre == "perdu":
        message = "PERDU : -" + f"{mise:g}" + " €"
    else:
        message = "BÉNÉFICE : +" + f"{gain_net:g}" + " €"
    ecrire_degrade(grille, 13, message, lambda t: melanger(BLANC, OR, 0.4 + 0.6 * t))
    ecrire_degrade(grille, 14, "Ton argent : " + f"{argent:g}" + " €",
                   lambda t: melanger(CYAN, ROSE, t))
    return grille


def resultat_simple(de1: int, de2: int, gain_net: float, mise: int) -> None:
    """Version texte pour les terminaux sans couleurs."""
    print()
    if gain_net > 0:
        print("Bravo ! Tu gagnes", gain_net, "euros de bénéfice.")
    else:
        print("Perdu ! Tu perds", mise, "euros.")


def ecran_resultat_des(de1: int, de2: int, gain_net: float, mise: int, argent: float) -> None:
    """Affiche l'écran de résultat du lancer (jackpot, gagné ou perdu)."""
    if couleurs_disponibles():
        animer_ecran(construire_ecran_des(de1, de2, gain_net, mise, argent),
                     issue_des(gain_net, mise))
    else:
        resultat_simple(de1, de2, gain_net, mise)
