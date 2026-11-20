from OUTILS.des import des


def page6(gameState: dict) -> int:
    res: int = -2

    print()
    print("Le cuisinier te surprend près de son vestiaire.")
    print("Il te propose un pari sur deux dés pour décider si tu repars avec ses biscuits.")

    gain_net: int = des(gameState)

    if gameState["argent"] <= 0:
        print("Tu n'as plus d'argent et le cuisinier te chasse du casino.")
        res = -1
    elif gain_net == 0:
        print("Le pari n'a pas eu lieu. Le cuisinier te laisse réessayer.")
        res = 6
    elif gain_net > 0:
        print("Tu remportes le pari et repars avec des biscuits.")
        gameState["inventaire"].append("biscuits")
        res = 0
    else:
        print("Tu perds le pari et quittes la cuisine les mains vides.")
        res = 0

    return res
