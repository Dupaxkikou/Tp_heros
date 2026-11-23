def page1(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    print("                  ")
    print(f"{gameState['nom']}, 23h10 : vous arrivez devant le GRAND CASINO ROYAL pour votre premier jour de travail.")
    print("Un jeune RS6 full black ABERRANTTT ffro est garé devant l'entrée. Le directeur est introuvable...")
    print(f"Que faites-vous ,{gameState['nom']} ?")
    print("1 - Entrer par la grande porte du casino   2 - Passer discrètement par la cuisine")
    choix: str = input("> ")

    if choix == "1":
        res = 3
    elif choix == "2":
        res = 2
    else:
        print("Choix invalide.")
        res = 1               # on reste sur cette page

    return res


