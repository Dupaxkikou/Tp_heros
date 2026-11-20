def menu() -> dict:
    """Création du personnage : retourne le dictionnaire gameState."""
    print("=== CRÉATION DU PERSONNAGE ===")
    nom: str = input("Quel est votre nom ? ")
    gameState: dict = {
        "nom": nom,
        "argent": 100,
        "reputation": 0,
        "inventaire": [],
    }
    print(f"Bienvenue, {nom} ! \n")
    return gameState
