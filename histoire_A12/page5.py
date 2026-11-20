from OUTILS.des import lancer_des
from OUTILS.roulette import roulette


def page5(gameState: dict) -> int:
    res: int = -2
    gain_net: float = 0.0

    print()
    print("Tu descends dans la salle de jeux du Grand Casino Royal.")
    print("Deux tables attirent ton attention :")
    print("1 - La roulette")
    print("2 - La table de dés")

    choix: str = input("Où veux-tu tenter ta chance ? ").strip()
    if choix == "1":
        gain_net = roulette(gameState)
    elif choix == "2":
        gain_net = lancer_des(gameState)
    else:
        print("Tu hésites devant les tables sans t'installer.")

    if gameState["argent"] <= 0:
        print("Tu as tout perdu. Le casino te met à la porte.")
        res = -1
    elif gain_net == 0:
        print("Tu n'as pas placé de pari. Tu peux réessayer.")
        res = 5
    elif gain_net > 0:
        print("Avec tes gains, tu quittes la table la tête haute.")
        res = 0
    else:
        print("Tu quittes la table avant de perdre davantage.")
        res = 0

    return res
