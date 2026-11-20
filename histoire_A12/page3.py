def page3(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("Vous entrez dans le casino. Un receptionniste vous acceuillle avec un grand sourire")
    print(f"Monsieur {gameState['nom']} ! Votre suite love roooooom  est prête")
    print( "Il vous prend visiblement pour un riche client...")
    print("Que faites-vous ?")
    print("1 - Jouer le jeu et profiter de la suite   2 - Lui expliquer qu'il y a confusion et que vous êtes juste le nv employé")
    choix: str = input("> ")

    if choix == "1":
        res = 5
    elif choix == "2":
        res = 7
    else:
        print("Choix invalide.")
        res = 3
    return res
