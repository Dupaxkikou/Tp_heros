"""Table de dés : on parie que le total de deux dés sera plus ou moins de 7."""

import random

from ASCII.ascii_des import animer_lancer, ecran_resultat_des


# Les deux paris possibles : le bénéfice est égal à la mise
PARIS: list = ["1", "2"]


def _afficher_regles() -> None:
    """Affiche les deux paris possibles."""

    print()
    print("On lance deux dés : le total va de 2 à 12.")
    print()
    print("1 - Moins de 7   (total de 2 à 6)    bénéfice : 1 fois la mise")
    print("2 - Plus de 7    (total de 8 à 12)   bénéfice : 1 fois la mise")
    print()
    print("Si le total fait exactement 7, tu perds ta mise.")


def _pari_gagne(choix: str, de1: int, de2: int) -> bool:
    """Dit si le pari choisi est gagnant pour ce lancer."""

    total: int = de1 + de2
    gagne: bool = False

    if choix == "1":
        gagne = total < 7
    elif choix == "2":
        gagne = total > 7

    return gagne


def lancer_des(gameState: dict) -> float:
    """Joue un pari au lancer de dés et renvoie le gain net."""

    gain_net: float = 0.0
    argent: float = gameState["argent"]

    print()
    print("========== TABLE DE DÉS ==========")
    print(f"Ton argent : {argent:g} euros")

    if argent <= 0:
        print("Tu n'as plus d'argent pour jouer.")
    else:
        _afficher_regles()

        choix: str = input("Ton choix : ").strip()
        if choix not in PARIS:
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
                    de1: int = random.randint(1, 6)
                    de2: int = random.randint(1, 6)
                    animer_lancer(de1, de2)

                    if _pari_gagne(choix, de1, de2):
                        gain_net = mise
                    else:
                        gain_net = -mise

                    gameState["argent"] = argent + gain_net
                    ecran_resultat_des(de1, de2, gain_net, mise, gameState["argent"])
                    print()
                    print(f"Il te reste {gameState['argent']:g} euros.")

    return gain_net
