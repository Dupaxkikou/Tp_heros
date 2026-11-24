"""
touche : lecture d'une touche en temps réel (sans attendre Entrée), pour les mini-jeux.

Fonctions :
    touches_disponibles()    True si le terminal permet cette lecture
    activer_touches()        à appeler avant de lire les touches, retourne l'ancien réglage
    attendre_touche(duree)   attend une touche (au plus duree secondes) : la touche ou ""
    vider_touches()          oublie les touches déjà tapées
    desactiver_touches(x)    à appeler à la fin, avec la valeur rendue par activer_touches()

Fonctionne dans un vrai terminal (Windows, Mac, Linux), mais pas dans IDLE ni dans Thonny.
Utilise des modules hors programme (msvcrt, termios, select) : ils sont nécessaires pour
lire le clavier sans attendre Entrée.
"""

import atexit
import os
import sys
import time


def touches_disponibles() -> bool:
    """True si on est dans un vrai terminal (donc ni IDLE ni Thonny)."""

    res: bool = False
    if sys.stdin is not None and sys.stdin is sys.__stdin__:
        res = sys.stdin.isatty()
    return res


def activer_touches() -> object:
    """Passe le terminal en lecture immédiate des touches (pas d'écho, pas d'Entrée)."""

    anciens: object = None
    if os.name != "nt":
        import termios
        import tty

        fichier: int = sys.stdin.fileno()
        anciens = termios.tcgetattr(fichier)
        tty.setcbreak(fichier)
        # même si le programme plante, le terminal retrouvera son réglage normal
        atexit.register(termios.tcsetattr, fichier, termios.TCSADRAIN, anciens)
    return anciens


def desactiver_touches(anciens: object) -> None:
    """Remet le terminal comme avant activer_touches()."""

    if anciens is not None:
        import termios

        termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, anciens)


def attendre_touche(duree: float) -> str:
    """Attend une touche pendant duree secondes au plus. Retourne la touche, ou "" sinon."""

    res: str = ""
    if os.name == "nt":
        import msvcrt

        fin: float = time.time() + duree
        while res == "" and time.time() < fin:
            if msvcrt.kbhit():
                res = msvcrt.getwch()
            else:
                time.sleep(0.003)
    else:
        import select

        if select.select([sys.stdin], [], [], duree)[0]:
            res = os.read(sys.stdin.fileno(), 1).decode(errors="ignore")
    return res


def vider_touches() -> None:
    """Oublie toutes les touches tapées jusqu'ici."""

    while attendre_touche(0) != "":
        pass
