"""Ce module contient tout le code en rapport avec la modelisation de Helltaker"""
from collections import namedtuple
from typing import Tuple, List, Optional, Dict, FrozenSet


State = namedtuple(
    "State", ["me", "blocs", "mobs", "piques", "pieges", "cle", "porte", "coupRestant"]
)


def grid_to_state(grid: Dict[str, List[List[str]]]):
    """
    Retourne un dictionnaire représentant le jeu
    Arguments :
        - grid : le dictionnaire retourné par grid_from_file
    Retour : un dictionnaire contenant:
        - "state" : l'état initial
        - "demones" : les cases des demones
        - "cases" : les cases valides du jeu
    """
    cases: List[Tuple[int, int]] = []
    demone: List[Tuple[int, int]] = []
    me: Tuple[int, int]
    blocs: List[Tuple[int, int]] = []
    mobs: List[Tuple[int, int]] = []
    piques: List[Tuple[int, int]] = []
    pieges: List[Tuple[int, int, bool]] = []
    cle: Tuple[int, int, bool] = (-1, -1, False)
    porte: Tuple[int, int, bool] = (-1, -1, False)
    coup_restant = grid["max_steps"]
    j = 0
    for ligne in grid["grid"]:
        i = 0
        for case in ligne:
            if case != "#":
                cases.append((i, j))

            if case == "D":
                demone.append((i, j))
            elif case == "H":
                me = (i, j)
            elif case == "B":
                blocs.append((i, j))
            elif case == "K":
                cle = (i, j, True)
            elif case == "L":
                porte = (i, j, True)
            elif case == "M":
                mobs.append((i, j))
            elif case == "S":
                piques.append((i, j))
            elif case == "T":
                pieges.append((i, j, False))
            elif case == "U":
                pieges.append((i, j, True))
            elif case == "O":
                blocs.append((i, j))
                piques.append((i, j))
            elif case == "P":
                blocs.append((i, j))
                pieges.append((i, j, False))
            elif case == "Q":
                blocs.append((i, j))
                pieges.append((i, j, True))

            i += 1
        j += 1

    pieges = switch_traps(pieges)

    return {
        "state": State(
            me,
            frozenset(blocs),
            frozenset(mobs),
            frozenset(piques),
            frozenset(pieges),
            cle,
            porte,
            coup_restant,
        ),
        "demones": frozenset(demone),
        "cases": frozenset(cases),
    }


def get_next(direction: str, coord: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """Retourne la coordonnee adjacente en fonction de la direction"""
    if direction == "h":
        return (coord[0], coord[1] - 1)
    elif direction == "b":
        return (coord[0], coord[1] + 1)
    elif direction == "g":
        return (coord[0] - 1, coord[1])
    elif direction == "d":
        return (coord[0] + 1, coord[1])
    return None


def switch_traps(pieges: List) -> List:
    """Effectue la bascule des pieges entre safe et unsafe"""
    n_pieges = []
    for piege in pieges:
        n_pieges.append((piege[0], piege[1], not piege[2]))

    return n_pieges


def is_next_demone(state: State, demones: FrozenSet[Tuple[int, int]]) -> bool:
    """test la presence d'une demonde sur une case adjacente"""
    for demone in demones:
        if abs(demone[0] - state.me[0]) == 0 and abs(demone[1] - state.me[1]) == 1:
            return True
        elif abs(demone[0] - state.me[0]) == 1 and abs(demone[1] - state.me[1]) == 0:
            return True

    return False


def case_is_cle(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'une clé sur la case next"""
    return case == state.cle[0:2] and state.cle[2]


def case_is_porte(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'une porte (fermée) sur la case next"""
    return state.porte[0:2] == case and state.porte[2]


def case_is_piege(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'un piege (unsafe) sur la case next"""
    for piege in state.pieges:
        if case == piege[0:2] and piege[2]:
            return True
    return False


def case_is_only_cle(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'une clé uniquement (rien d'autre) sur la case next"""
    return (
        case_is_cle(state, case)
        and not case in state.mobs
        and not case in state.blocs
        and not case_is_piege(state, case)
        and not case in state.piques
        and not case_is_porte(state, case)
    )


def case_is_only_piege(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'un piege (unsafe) uniquement (rien d'autre) sur la case next"""
    return (
        not case_is_cle(state, case)
        and not case in state.mobs
        and not case in state.blocs
        and case_is_piege(state, case)
        and not case in state.piques
        and not case_is_porte(state, case)
    )


def case_is_only_porte(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'une porte (fermée) uniquement (rien d'autre) sur la case next"""
    return (
        case_is_porte(state, case)
        and not case in state.mobs
        and not case in state.blocs
        and not case_is_piege(state, case)
        and not case in state.piques
        and not case_is_cle(state, case)
    )


def case_is_only_case(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'une case uniquement (rien d'autre) sur la case next"""
    return (
        not case_is_porte(state, case)
        and not case in state.mobs
        and not case in state.blocs
        and not case_is_piege(state, case)
        and not case in state.piques
        and not case_is_cle(state, case)
    )


def case_is_only_pique(state: State, case: Tuple[int, int]) -> bool:
    """Test la presence d'un pique uniquement (rien d'autre) sur la case next"""
    return (
        not case_is_porte(state, case)
        and not case in state.mobs
        and not case in state.blocs
        and not case_is_piege(state, case)
        and case in state.piques
        and not case_is_cle(state, case)
    )
