
import time

def page6(gameState: dict) -> int:
    res: int = -2

    rouge = "\033[31m"
    jaune = "\033[33m"
    bleu = "\033[34m"
    vert = "\033[32m"
    reset = "\033[0m"

    debut = time.time()
    duree = 30

    cuisson = 0.0
    temperature = 20.0
    chaleur = 0

    largeur = 30

    print("\033[2J\033[H", end="")

    while time.time() - debut < duree and cuisson < 100:

        # Température cible selon la chaleur
        temperature_cible = 20 + chaleur * 45

        temperature += (temperature_cible - temperature) * 0.08

        # Progression de la cuisson
        if temperature > 60:
            cuisson += (temperature - 60) * 0.0008

        cuisson = min(100, cuisson)

        temps_restant = max(0, int(duree - (time.time() - debut)))

        # Couleur température
        if temperature < 70:
            couleur_temp = bleu
        elif temperature < 120:
            couleur_temp = vert
        else:
            couleur_temp = rouge

        # Barres
        barre_temp = int(min(temperature, 200) / 200 * largeur)
        barre_cuisson = int(cuisson / 100 * largeur)

        affichage_temp = (
            couleur_temp + "█" * barre_temp + reset
            + "░" * (largeur - barre_temp)
        )

        affichage_cuisson = (
            jaune + "█" * barre_cuisson + reset
            + "░" * (largeur - barre_cuisson)
        )

        print("\033[H", end="")

        print("========== CUISSON ==========\n")
        print(f"Temps restant : {temps_restant} secondes\n")

        print(f"Température : {int(temperature)} °C")
        print(f"[{affichage_temp}]\n")

        print(f"Cuisson : {int(cuisson)} %")
        print(f"[{affichage_cuisson}]\n")

        print(f"Chaleur de la casserole : {chaleur}/4\n")

        print("========== COMMANDES ==========")
        print("[Z] Augmenter la chaleur")
        print("[S] Diminuer la chaleur")

        # Commande du joueur
        touche = input("\nTon choix (Z/S ou Entrée) : ").lower()

        if touche == "z":
            chaleur = min(4, chaleur + 1)

        elif touche == "s":
            chaleur = max(0, chaleur - 1)

    print("\n")

    if cuisson >= 100:
        print(vert + "BRAVO ! Cuisson réussie !" + reset)
        res = 1
    else:
        print(rouge + "TEMPS ÉCOULÉ !" + reset)
        res = 0

    return res
