def page9(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("Tu a dormis pendant 1h")
    print("En te reveillant tu vois une femme en train de dormir sur le lit en string ficelle Victoria Secret à côté de toi")
    print("Que fais-tu ?")
    print("1 - Tu passes pas par 4 chemin et tu proposes une collab avec elle   2 - tu sors discretement de la chambre pour aller a ton entretien")
    choix: str = input("> ")

    if choix == "1":
        res = 15
    elif choix == "2":
        res = 11
    else:
        print("Choix invalide.")
        res = 9
    return res