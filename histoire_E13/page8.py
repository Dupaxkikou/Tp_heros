from ASCII.ascii_feu import ascii_feu

def page8(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu 

    print("Que faites-vous ?")
    print("1 - Vous partez en courant     2 - Vous vous mettez a la recherche d'un extincteur")
    choix: str = input("> ")

    if choix == "1":
        res = 12
    elif choix == "2":
        res = 10
    else:
        print("Choix invalide.")
        res = 8
    return res