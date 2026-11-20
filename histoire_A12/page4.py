def page4(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("Vous ouvrz le casier du cuisto ")
    print("Vous trouvez une malette etrange qui contient 400 euros de jetons de casinp")
    print("Que faites-vous ?")
    print("1 - Vous volez le contenus de la malette    2 - Lui expliquer qu'il y a confusion et que vous êtes juste le nv employé")
    choix: str = input("> ")

    if choix == "1":
        res = 
    elif choix == "2":
        res = 
    else:
        print("Choix innvalide.")
        res = 4
    return res