def page7(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("En tant qu'honnête citoyen, vous décidez de vous rendre à votre entretien d'embauche.")
    print("Le chemin jusqu'au bureau est siiiiiiiiiiiiiiiiiiii longgg")
    print("TIENS, une porte ouverte qui mène à une suite")
    print("Que faites-vous ?")
    print("1 - Vous tapez une petite sieste en bien   2 - Vous passez votre chemin et vous allez directement à votre l'entretien d'embauche")
    choix: str = input("> ")

    if choix == "1":
        res = 9
    elif choix == "2":
        res = 11
    else:
        print("Choix innvalide.")
        res = 7
    return res