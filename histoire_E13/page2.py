def page2(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("Vous arrivez dans la cuisine, vous mourrez de faim.")
    print("Des raviolis son posés sur le plan de travail.")
    print("Que faites-vous ?")
    print("1 - Vous les cuisinez    2 - Vous tapez les meilleurs biscuit qui depasse du verstiaire d'un cuisinier")
    choix: str = input("> ")

    if choix == "1":
        res = 6
    elif choix == "2":
        res = 4
    else:
        print("Choix invalide.")
        res = 2  
    return res
