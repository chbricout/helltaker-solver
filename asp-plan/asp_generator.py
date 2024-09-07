"""Module pour créer le code ASP et executer clingo"""
import timeit
from typing import List
import clingo
from helltaker_utils import grid_from_file


def asp_plan(infos) -> str:
    """fonction planificateur utilisant ASP"""

    asp_code = ""
    with open("helltaker_charles.lp", "r") as file_asp:
        asp_base = file_asp.readlines()
        file_asp.close()
        asp_code = f"#const n={infos['max_steps']}.\n"
        for line in asp_base:
            asp_code += line

    asp_code += convert_to_asp(infos["grid"])

    ctl = clingo.Control(["-n 1"])
    ctl.add("base", [], asp_code)
    ctl.ground([("base", [])])

    with ctl.solve(yield_=True) as handle:
        for model in handle:
            chemin = {}
            path = ""
            for atom in model.symbols(atoms=True):
                if atom.match("do", 2):
                    chemin[atom.arguments[1].number] = (
                        atom.arguments[0].arguments[1].name
                    )
            for i in range(len(chemin)):
                if chemin[i] == "up":
                    path += "h"
                elif chemin[i] == "down":
                    path += "b"
                elif chemin[i] == "left":
                    path += "g"
                elif chemin[i] == "right":
                    path += "d"
            return path
    return ""


def convert_to_asp(grid: List[List[str]]) -> str:
    """Fonction qui convertit la grille de caractère en regles ASP"""
    asp_code = ""

    for i in range(len(grid) - 1):
        for j in range(len(grid[i]) - 1):
            if grid[i][j] != "#":
                rule = f"case(pos({j},{i})).\n"
                asp_code += rule

            if grid[i][j] == "H":
                rule = f"fluent(me(pos({j},{i})),0).\n"
                asp_code += rule
            elif grid[i][j] == "D":
                rule = f"demone(pos({j},{i})).\n"
                asp_code += rule
            elif grid[i][j] == "B":
                rule = f"fluent(bloc(pos({j},{i})),0).\n"
                asp_code += rule
            elif grid[i][j] == "K":
                rule = f"fluent(cle(pos({j},{i}),true),0).\n"
                asp_code += rule
            elif grid[i][j] == "L":
                rule = f"fluent(porte(pos({j},{i}),true),0).\n"
                asp_code += rule
            elif grid[i][j] == "M":
                rule = f"fluent(mob(pos({j},{i})),0).\n"
                asp_code += rule
            elif grid[i][j] == "S":
                rule = f"pique(pos({j},{i})).\n"
                asp_code += rule
            elif grid[i][j] == "T":
                rule = f"fluent(piege(pos({j},{i}),false),0).\n"
                asp_code += rule
            elif grid[i][j] == "U":
                rule = f"fluent(piege(pos({j},{i}),true),0).\n"
                asp_code += rule
            elif grid[i][j] == "O":
                rule = f"pique(pos({j},{i})).\n fluent(bloc(pos({j},{i})),0).\n"
                asp_code += rule
            elif grid[i][j] == "P":
                rule = f"fluent(piege(pos({j},{i}),false),0).\nfluent(bloc(pos({j},{i})),0).\n"
                asp_code += rule
            elif grid[i][j] == "Q":
                rule = f"fluent(piege(pos({j},{i}),true),0).\nfluent(bloc(pos({j},{i})),0).\n"
                asp_code += rule
    return asp_code


if __name__ == "__main__":
    testASP = timeit.Timer(
        "l = asp_plan(infos_level); print(l)", "from __main__ import asp_plan, infos_level",
    )

    for niveau in range(1, 10):
        infos_level = grid_from_file("../levels/level{}.txt".format(niveau))

        print("\nRECHERCHE NIVEAU {} :\n--------------------------------".format(niveau))
        print("temps : ", testASP.timeit(1))
