import time

def page6(gameState: dict) -> int:
    res: int = -2                     # par défaut : cas non prévu

    rouge = "\033[31m"
    jaune = "\033[33m"
    bleu = "\033[34m"
    vert = "\033[32m"
    reset = "\033[0m"

    debut :float = time.time()
    duree :int = 30  
    cuisson :int = 0
    temperature :int = 20
    chaleur :int = 0

    while (time.time() - debut < duree) and cuisson != 100:
        temps_restant :int = int(duree - (time.time() - debut))
        print ("Temps restant : {temps_restant} secondes")
        
        
        
        
        time.sleep(0,5)

    return res 
