from OUTILS.roulette import roulette


def page5(gameState: dict) -> int:
    res: int = -2

    print()
    print("Tu descends dans la salle de jeux du Grand Casino Royal.")
    print("Une roulette attire ton attention : tu décides de tenter ta chance.")

    gain_net: float = roulette(gameState)

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
