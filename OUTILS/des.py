"""Table de dés : on parie sur le total d'un lancer de deux dés."""

import random

from ASCII.ascii_des import animer_lancer, ecran_resultat_des


# Multiplicateur de gain (bénéfice = mise x multiplicateur) pour chaque pari
MULTIPLICATEURS: dict = {"1": 1, "2": 1, "3": 4, "4": 5}


def _afficher_regles() -> None:
    """Affiche les paris possibles avec leurs chances de gagner."""

    print()
    print("On lance deux dés : le total va de 2 à 12.")
    print()
    print("1 - Moins de 7   (total de 2 à 6)       chances : 42 %   bénéfice : 1 fois la mise")
    print("2 - Plus de 7    (total de 8 à 12)      chances : 42 %   bénéfice : 1 fois la mise")
    print("3 - Exactement 7                        chances : 17 %   bénéfice : 4 fois la mise")
    print("4 - Double (deux dés identiques)        chances : 17 %   bénéfice : 5 fois la mise")


def _pari_gagne(choix: str, de1: int, de2: int) -> bool:
    """Dit si le pari choisi est gagnant pour ce lancer."""

    total: int = de1 + de2
    gagne: bool = False

    if choix == "1":
        gagne = total < 7
    elif choix == "2":
        gagne = total > 7
    elif choix == "3":
        gagne = total == 7
    elif choix == "4":
        gagne = de1 == de2

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
        if choix not in MULTIPLICATEURS:
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
                        gain_net = mise * MULTIPLICATEURS[choix]
                    else:
                        gain_net = -mise

                    gameState["argent"] = argent + gain_net
                    ecran_resultat_des(de1, de2, gain_net, mise, gameState["argent"])
                    print()
                    print(f"Il te reste {gameState['argent']:g} euros.")

    return gain_net
