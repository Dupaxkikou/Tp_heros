
import time
import os
import msvcrt

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
    chaleur = 5

    largeur = 30

    while time.time() - debut < duree and cuisson < 100:

        # Gestion des touches
        if msvcrt.kbhit():
            touche = msvcrt.getwch().lower()

            if touche == "z":
                chaleur = min(10, chaleur + 1)

            elif touche == "s":
                chaleur = max(0, chaleur - 1)

        # Évolution de la température
        temperature_cible = 20 + chaleur * 18
        temperature += (temperature_cible - temperature) * 0.08

        # Évolution de la cuisson
        if temperature > 60:
            cuisson += (temperature - 60) * 0.0008

        cuisson = min(100, cuisson)

        # Temps restant
        temps_restant = max(0, int(duree - (time.time() - debut)))

        # Couleurs
        if temperature < 70:
            couleur_temp = bleu
        elif temperature < 120:
            couleur_temp = vert
        else:
            couleur_temp = rouge

        # Barres de progression
        barre_temp = int(min(temperature, 200) / 200 * largeur)
        barre_cuisson = int(cuisson / 100 * largeur)

        affichage_temp = (
            couleur_temp
            + "█" * barre_temp
            + reset
            + "░" * (largeur - barre_temp)
        )

        affichage_cuisson = (
            jaune
            + "█" * barre_cuisson
            + reset
            + "░" * (largeur - barre_cuisson)
        )

        # Affichage
        os.system("cls")

        print("========== CUISSON ==========\n")

        print(f"Temps restant : {temps_restant} secondes\n")

        print(f"Température : {int(temperature)} °C")
        print(f"[{affichage_temp}]")

        print(f"\nCuisson : {int(cuisson)} %")
        print(f"[{affichage_cuisson}]")

        print(f"\nChaleur de la casserole : {chaleur}/10")

        print("\n========== COMMANDES ==========")
        print("[Z] Augmenter la chaleur")
        print("[S] Diminuer la chaleur")

        time.sleep(0.1)

    os.system("cls")

    if cuisson >= 100:
        print(vert + "BRAVO ! Cuisson réussie !" + reset)
        res = 1
    else:
        print(rouge + "TEMPS ÉCOULÉ ! Cuisson incomplète." + reset)
        res = 0

    return res

