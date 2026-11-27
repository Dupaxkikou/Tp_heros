def page5(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("         ")
    print("tu rentre dans ta suite ")
    print("tu va dans la chambre pour faire un dodo avant ton entretient")
    print("Dans la table de chevet tu trouve un papier avec un code dessus, tu le prend et tu le met dans ta poche")
    print("le code est 1911, tu devrais le retenir pour plus tard")
    print("Quand tu as bien retenu le code appuie sur n'importe quelle touche pour t'endormir")
    choix: str = input("> ")


    if choix == "":
            res = 9
    else:
            res = 9
    return res 