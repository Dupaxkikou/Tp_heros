"""Jeu de roulette française : tirage, paris et argent du joueur."""

import random

from ASCII.ascii_roulette import ROUGES, animer_tirage, ecran_resultat


ROUE: list = [
    0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13,
    36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14,
    31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26,
]


def _lancer_bille() -> int:
    """Tire la case gagnante au hasard et anime la bille jusqu'à cette case."""

    index_gagnant: int = random.randint(0, len(ROUE) - 1)
    animer_tirage(ROUE, index_gagnant)
    return ROUE[index_gagnant]


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
        print("1 - Miser sur rouge (bénéfice : 1 fois la mise)")
        print("2 - Miser sur noir (bénéfice : 1 fois la mise)")
        print("3 - Miser sur vert (le zéro, bénéfice : 35 fois la mise)")

        choix: str = input("Ton choix : ").strip()
        if choix not in ["1", "2", "3"]:
            print("Choix invalide. Partie annulée.")
        else:
            mise_saisie: str = input("Combien veux-tu miser ? ").strip()
            if not mise_saisie.isdecimal():
                print("Mise invalide. Partie annulée.")
            else:
                mise: int = int(mise_saisie)
                if mise <= 0 or mise > argent:
                    print("Tu dois miser une somme positive que tu possèdes.")
                else:
                    print()
                    print("Tu mises", mise, "euros.")
                    numero_gagnant: int = _lancer_bille()

                    if choix == "1" and numero_gagnant in ROUGES:
                        gain_net = mise
                    elif choix == "2" and numero_gagnant != 0 and numero_gagnant not in ROUGES:
                        gain_net = mise
                    elif choix == "3" and numero_gagnant == 0:
                        gain_net = mise * 35
                    elif choix in ["1", "2"] and numero_gagnant == 0:
                        gain_net = -mise / 2
                    else:
                        gain_net = -mise

                    gameState["argent"] = argent + gain_net

                    ecran_resultat(numero_gagnant, gain_net, mise, gameState["argent"])
                    print()
                    print(f"Il te reste {gameState['argent']:g} euros.")

    return gain_net
