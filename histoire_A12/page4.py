def page4(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("Vous ouvrz le casier du cuisto ")
    print("Vous trouvez une malette étrange qui contient 400 euros de jetons de casinp")
    print("Que faites-vous ?")
    print("1 - Vous volez le contenus de la malette    2 - Vous passez votre chemin et vous allez directement à votre l'entretien d'embauche")
    choix: str = input("> ")

    if choix == "1":
        gameState["inventaire"].append("malette de jetons")
        res = 11
    elif choix == "2":
        res = 11
    else:
        print("Choix innvalide.")
        res = 4
    return res