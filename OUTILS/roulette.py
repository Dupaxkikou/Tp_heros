"""
Mini-jeu de roulette française.
roulette(gameState) gère le pari et actualise l'argent du joueur.
"""
from ASCII.ascii_roulette import ascii_roulette

ROUGES: list = [
    1, 3, 5, 7, 9, 12, 14, 16, 18,
    19, 21, 23, 25, 27, 30, 32, 34, 36
]


def roulette(gameState: dict) -> int:
    """Joue à la roulette et renvoie le gain net de la partie."""

    gain_net: int = 0
    argent: int = gameState["argent"]

    print()
    print("========== TABLE DE ROULETTE ==========")
    print("Ton argent :", argent, "euros")

    if argent <= 0:
        print("Tu n'as plus d'argent pour jouer.")
        return gain_net

    print()
    print("1 - Miser sur un numéro (gain : 35 fois la mise)")
    print("2 - Miser sur rouge (gain : 1 fois la mise)")
    print("3 - Miser sur noir (gain : 1 fois la mise)")
    print("4 - Miser sur pair (gain : 1 fois la mise)")
    print("5 - Miser sur impair (gain : 1 fois la mise)")

    choix: str = input("Ton choix : ")
    if choix not in ["1", "2", "3", "4", "5"]:
        print("Choix invalide. Partie annulée.")
        return gain_net

    numero_mise: int = -1
    if choix == "1":
        numero_saisi: str = input("Sur quel numéro (0 à 36) ? ")
        if not numero_saisi.isdigit():
            print("Numéro invalide. Partie annulée.")
            return gain_net
        numero_mise = int(numero_saisi)
        if numero_mise < 0 or numero_mise > 36:
            print("Le numéro doit être compris entre 0 et 36.")
            return gain_net

    mise_saisie: str = input("Combien veux-tu miser ? ")
    if not mise_saisie.isdigit():
        print("Mise invalide. Partie annulée.")
        return gain_net

    mise: int = int(mise_saisie)
    if mise <= 0 or mise > argent:
        print("Tu dois miser une somme positive que tu possèdes.")
        return gain_net

    print()
    print("Tu mises", mise, "euros.")
    numero_gagnant: int = ascii_roulette()

    victoire: bool = False
    if choix == "1" and numero_gagnant == numero_mise:
        victoire = True
        gain_net = mise * 35
    elif choix == "2" and numero_gagnant in ROUGES:
        victoire = True
        gain_net = mise
    elif choix == "3" and numero_gagnant != 0 and numero_gagnant not in ROUGES:
        victoire = True
        gain_net = mise
    elif choix == "4" and numero_gagnant != 0 and numero_gagnant % 2 == 0:
        victoire = True
        gain_net = mise
    elif choix == "5" and numero_gagnant % 2 == 1:
        victoire = True
        gain_net = mise

    gameState["argent"] = argent - mise + gain_net

    print("Résultat :", numero_gagnant)
    if victoire:
        print("Bravo ! Tu gagnes", gain_net, "euros de bénéfice.")
    else:
        gain_net = -mise
        print("Perdu ! Tu perds", mise, "euros.")

    print("Il te reste", gameState["argent"], "euros.")
    return gain_net
