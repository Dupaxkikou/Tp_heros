"""Jeu de deux dés : le joueur mise sur une somme paire ou impaire."""

import random

from ASCII.ascii_des import afficher_des


def des(gameState: dict) -> int:
    """Lance deux dés, met à jour l'argent et renvoie le gain net."""

    gain_net: int = 0
    argent: float = gameState["argent"]

    print()
    print("========== TABLE DE DÉS ==========")
    print(f"Ton argent : {argent:g} euros")

    if argent <= 0:
        print("Tu n'as plus d'argent pour jouer.")
    else:
        print()
        print("1 - Parier sur une somme paire")
        print("2 - Parier sur une somme impaire")

        choix: str = input("Ton choix (pair/impair) : ").strip().lower()
        if choix == "1":
            choix = "pair"
        elif choix == "2":
            choix = "impair"

        if choix != "pair" and choix != "impair":
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
                    de1: int = random.randint(1, 6)
                    de2: int = random.randint(1, 6)
                    somme: int = de1 + de2
                    afficher_des(de1, de2)

                    print(f"Les dés font {somme}.")
                    if somme % 2 == 0:
                        resultat: str = "pair"
                    else:
                        resultat = "impair"

                    if resultat == choix:
                        gain_net = mise
                        print("Bravo ! La somme est", resultat + ".")
                        print("Tu gagnes", gain_net, "euros de bénéfice.")
                    else:
                        gain_net = -mise
                        print("Perdu ! La somme est", resultat + ".")
                        print("Tu perds", mise, "euros.")

                    gameState["argent"] = argent + gain_net
                    print(f"Il te reste {gameState['argent']:g} euros.")

    return gain_net
