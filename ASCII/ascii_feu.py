def ascii_feu() -> None:
    """Animation : le feu grandit dans la cuisine, étape par étape."""

    etapes: list = [
        "Une petite flamme apparaît sur le plan de travail...",
        "L'huile prend feu, les flammes montent !",
        "Le torchon et les rideaux s'enflamment !!",
        "LA CUISINE EST EN FEU !!!",
    ]

    for i in range(len(etapes)):
        hauteur: int = i + 2
        print()
        print(etapes[i])
        for ligne in range(hauteur):
            largeur: int = 2 * ligne + 1
            print(" " * (hauteur - ligne) + "^" * largeur)
        print("=" * (2 * hauteur + 1))
        if i < len(etapes) - 1:
            input("(Entrée pour continuer)")
    print()


if __name__ == "__main__":
    ascii_feu()