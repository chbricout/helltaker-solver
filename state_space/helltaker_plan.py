"""Module a appeler avec en argument le chemin vers une grille valide"""
import sys
from helltaker_utils import grid_from_file, check_plan
from helltaker_explo import find_plan


def main():
    """Fonction qui affiche le chemin resolovant le niveau passé en argument"""
    # récupération du nom du fichier depuis la ligne de commande
    filename = sys.argv[1]

    # récupération de al grille et de toutes les infos
    infos = grid_from_file(filename)

    # calcul du plan
    plan = find_plan(infos)

    # affichage du résultat
    if check_plan(plan):
        print("[OK]", plan)
    else:
        print("[Err]", plan, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
