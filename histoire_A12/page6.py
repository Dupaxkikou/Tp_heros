def page6(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
<<<<<<< HEAD
    print("")
    print("")
    print( "")
    print("")
    print("1 -    2 - ")
    choix: str = input("> ")

    if choix == "1":
        res = 
    elif choix == "2":
        res = 
    else:
        print("Choix invalide.")
        res = 
=======
    print("Vous sortez donc une poële,vous sortez les raviolis")
    print("Avec ce palais de doberman (vous êtes censé être croupier pas cuisinier), vous faites frire les raviolis")
    print("L'huile est trop chaude, donc on met un peu d'eau pour refroidir")
    print("Vous vous reveillez avec les sourcils brulés et la cuisine est en feu !")
    print("Que faites-vous ?")
    print("1 - Vous partez en courant     2 - Vous vous mettez a la recherche d'un extincteur")
    choix: str = input("> ")

    if choix == "1":
        res = 12
    elif choix == "2":
        res = 18
    else:
        print("Choix invalide.")
        res = 6
>>>>>>> 3625a32f5eb0504446ad3e5851454bca551966df
    return res