import time

from ASCII.ascii_discretion import CENTRE, LARGEUR_BARRE, scene
from ASCII.ascii_gameover import couleurs_disponibles
from OUTILS.touche import (activer_touches, attendre_touche, desactiver_touches,
                           touches_disponibles, vider_touches)


TOTAL_PAS: int = 8
ERREURS_PERMISES: int = 2
PAGE_SUIVANTE: int = 12        # page où l'on arrive si on sort sans réveiller personne

MESSAGES_ERREUR: list = [
    "CRAC ! Le parquet grince... elle remue un peu.",
    "CRAAAC ! Elle ouvre un oeil... une erreur de plus = fin !",
    "CRAAAAC ! Elle se réveille !",
]


def _demi_zone(pas: int) -> int:
    """Taille de la zone verte : elle rétrécit au fil des pas."""
    res: int = 4
    if pas >= 6:
        res = 2
    elif pas >= 3:
        res = 3
    return res


def _position_curseur(duree: float, vitesse: float) -> int:
    """Case du curseur : il va et vient sur la barre."""
    longueur: int = LARGEUR_BARRE - 1
    trajet: float = (vitesse * duree) % (2 * longueur)
    if trajet > longueur:
        trajet = 2 * longueur - trajet
    return int(trajet)


def _jouer_un_pas(pas: int, erreurs: int) -> int:
    """Le curseur va et vient jusqu'à un appui sur ESPACE.
    Retourne la case où il était, ou -1 si le joueur a trop attendu."""
    vitesse: float = 20 + 4 * pas          # le curseur accélère à chaque pas
    zone: int = _demi_zone(pas)
    debut: float = time.time()
    resultat: int = -1
    fini: bool = False

    vider_touches()
    while not fini:
        duree: float = time.time() - debut
        curseur: int = _position_curseur(duree, vitesse)
        print("\033[H" + scene(pas, TOTAL_PAS, curseur, zone, erreurs, ERREURS_PERMISES, "", True),
              end="", flush=True)

        touche: str = attendre_touche(0.03)
        if touche == " ":
            resultat = curseur
            fini = True
        elif duree > 6:
            fini = True
    return resultat


def page11(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("Tu te lèves sans un bruit. Elle dort toujours à côté de toi.")
    print("Le parquet est très vieux : chaque pas doit être parfait.")
    print()
    print("Un curseur va et vient sur une barre. Appuie sur la barre ESPACE")
    print("quand il est dans la zone verte pour faire un pas silencieux.")
    print(f"Il faut faire {TOTAL_PAS} pas jusqu'à la porte. À la {ERREURS_PERMISES + 1}e erreur, elle se réveille !")

    if not (touches_disponibles() and couleurs_disponibles()):
        print()
        print("(Ce mini-jeu demande un vrai terminal, pas IDLE ni Thonny : tu passes sans bruit.)")
        res = PAGE_SUIVANTE
    else:
        input("Appuie sur Entrée pour commencer... ")
        anciens: object = activer_touches()
        print("\033[2J", end="")

        pas: int = 0
        erreurs: int = 0
        while pas < TOTAL_PAS and erreurs <= ERREURS_PERMISES:
            curseur: int = _jouer_un_pas(pas, erreurs)
            reussi: bool = abs(curseur - CENTRE) <= _demi_zone(pas)
            message: str = "Pas silencieux !"
            if reussi:
                pas = pas + 1
            else:
                erreurs = erreurs + 1
                message = MESSAGES_ERREUR[erreurs - 1]
                if curseur == -1:
                    message = "Tu hésites trop : elle remue dans son sommeil !"

            print("\033[H" + scene(pas, TOTAL_PAS, max(curseur, 0), _demi_zone(pas), erreurs,
                                   ERREURS_PERMISES, message, reussi), end="", flush=True)
            time.sleep(0.9)

        desactiver_touches(anciens)
        print("\033[2J\033[H", end="")

        if erreurs > ERREURS_PERMISES:
            print("Elle se réveille en sursaut et se met à hurler à pleins poumons !")
            print("La sécurité du casino arrive en courant.")
            res = -1
        else:
            print("Tu atteins la porte et la refermes sans un bruit.")
            print("Direction l'entretien d'embauche !")
            res = PAGE_SUIVANTE
    return res
