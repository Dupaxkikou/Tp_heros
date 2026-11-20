"""Jeu de roulette française : tirage, paris et argent du joueur."""

import random
import time

from ASCII.ascii_roulette import afficher_roulette


ROUE: list = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
]

ROUGES: list = [
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36,
]


def _lancer_bille() -> int:
    """Effectue un tirage et anime la bille pendant environ quatre secondes."""

    nombre_cases: int = len(ROUE)
    index_depart: int = random.randint(0, nombre_cases - 1)
    index_gagnant: int = random.randint(0, nombre_cases - 1)
    distance: int = (index_gagnant - index_depart) % nombre_cases
    distance = distance + nombre_cases * 3

    nombre_images: int = 40
    image: int = 0
    while image < nombre_images:
        position: int = (index_depart + distance * image // (nombre_images - 1)) % nombre_cases
        afficher_roulette(ROUE, ROUGES, position)

        pause: float = 0.025 + image * 0.15 / (nombre_images - 1)
        time.sleep(pause)
        image = image + 1

    numero_gagnant: int = ROUE[index_gagnant]
    afficher_roulette(ROUE, ROUGES, index_gagnant, numero_gagnant)
    return numero_gagnant


def roulette(gameState: dict) -> float:
    """Joue un pari rouge, noir ou vert et renvoie le gain net."""

    gain_net: float = 0.0
    argent: float = gameState["argent"]

    print()
    print("========== TABLE DE ROULETTE ==========")
    print(f"Ton argent : {argent:g} euros")

    if argent <= 0:
        print("Tu n'as plus d'argent pour jouer.")
    else:
        print()
        print("1 - Rouge  |  2 - Noir  |  3 - Vert (zéro)")
        print("Rouge/noir : bénéfice égal à la mise ; vert : 35 fois la mise.")

        choix: str = input("Ton choix (rouge/noir/vert) : ").strip().lower()
        if choix == "1":
            choix = "rouge"
        elif choix == "2":
            choix = "noir"
        elif choix == "3":
            choix = "vert"

        if choix not in ["rouge", "noir", "vert"]:
            print("Choix invalide. Partie annulée.")
        else:
            mise_saisie: str = input("Combien veux-tu miser ? ").strip()
            if not mise_saisie.isdigit():
                print("Mise invalide. Partie annulée.")
            else:
                mise: int = int(mise_saisie)
                if mise <= 0 or mise > argent:
                    print("Tu dois miser une somme positive que tu possèdes.")
                else:
                    print()
                    print("Tu mises", mise, "euros.")
                    numero_gagnant: int = _lancer_bille()

                    if choix == "rouge" and numero_gagnant in ROUGES:
                        gain_net = mise
                    elif choix == "noir" and numero_gagnant != 0 and numero_gagnant not in ROUGES:
                        gain_net = mise
                    elif choix == "vert" and numero_gagnant == 0:
                        gain_net = mise * 35
                    elif choix in ["rouge", "noir"] and numero_gagnant == 0:
                        gain_net = -mise / 2
                    else:
                        gain_net = -mise

                    gameState["argent"] = argent + gain_net

                    print()
                    if gain_net > 0:
                        print("Bravo ! Tu gagnes", gain_net, "euros de bénéfice.")
                    elif numero_gagnant == 0 and choix in ["rouge", "noir"]:
                        print("Le zéro sort : la règle du partage te fait perdre", mise / 2, "euros.")
                    else:
                        print("Perdu ! Tu perds", mise, "euros.")

                    print("Résultat :", numero_gagnant)
                    print(f"Il te reste {gameState['argent']:g} euros.")

    return gain_net
