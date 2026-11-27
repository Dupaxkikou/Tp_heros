def page6(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print("Vous sortez donc une poële,vous sortez les raviolis")
    print("Avec ce palais de doberman (vous êtes censé être croupier pas cuisinier), vous faites frire les raviolis")
    print("L'huile est trop chaude, donc on met un peu d'eau pour refroidir")
    print("Vous vous reveillez avec les sourcils brulés et la cuisine est en feu !")
    print("Tu peux ancore annuler l'action, appuis sur une touche si tu veux revenir en arrière")
    choix: str = input("> ")


    if choix == "":
            res = 6
    else:
            res = 8
    return res 
