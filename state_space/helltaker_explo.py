"""Ce module sert a realiser la recherche par exploration d'un niveau de helltaker"""
from typing import Callable, FrozenSet, Iterator, Tuple, List, Optional, Dict
import heapq
from pprint import pprint
import timeit
from helltaker_utils import grid_from_file
from helltaker_model import (
    case_is_only_case,
    case_is_only_cle,
    case_is_only_piege,
    case_is_only_pique,
    case_is_only_porte,
    case_is_piege,
    case_is_porte,
    is_next_demone,
    get_next,
    switch_traps,
    grid_to_state,
    State,
)


CASES: FrozenSet[Tuple[int, int]] = frozenset()
DEMONES: FrozenSet[Tuple[int, int]] = frozenset()


def successeurs(state: State) -> Iterator[Tuple[State, str]]:
    """Retourne un iterateur des successeurs de l'état state"""
    new_state = state._asdict()
    for direction in "hbgd":
        next_el = get_next(direction, state.me)

        new_state = state._asdict()
        new_state["mobs"] = set(new_state["mobs"])
        new_state["blocs"] = set(new_state["blocs"])

        if next_el in CASES and new_state["coupRestant"] > 0:
            if case_is_only_cle(state, next_el):
                new_state["cle"] = (next_el[0], next_el[1], False)
                new_state["me"] = next_el
                new_state["coupRestant"] -= 1
            elif case_is_only_porte(state, next_el):
                if not state.cle[2]:  # alors on a ramassé la clé
                    new_state["me"] = next_el
                    new_state["coupRestant"] -= 1
                    new_state["porte"] = (next_el[0], next_el[1], False)
                else:
                    new_state["coupRestant"] -= 1
            elif case_is_only_pique(state, next_el):
                new_state["me"] = next_el
                new_state["coupRestant"] -= 1
            elif case_is_only_case(state, next_el):
                new_state["me"] = next_el
                new_state["coupRestant"] -= 1
            elif case_is_only_piege(state, next_el):
                new_state["me"] = next_el
                new_state["coupRestant"] -= 1
            elif next_el in state.blocs:
                n_next = get_next(direction, next_el)
                if not n_next in CASES:
                    new_state["coupRestant"] -= 1
                elif (
                    n_next in state.blocs
                    or n_next in state.mobs
                    or case_is_porte(state, n_next)
                    or n_next in DEMONES
                ):
                    new_state["coupRestant"] -= 1
                else:
                    new_state["blocs"].remove(next_el)
                    new_state["blocs"].add(n_next)
                    new_state["coupRestant"] -= 1
            elif next_el in state.mobs:
                n_next = get_next(direction, next_el)
                if not n_next in CASES:
                    new_state["coupRestant"] -= 1
                    new_state["mobs"].remove(next_el)

                elif (
                    n_next in state.blocs
                    or n_next in state.mobs
                    or case_is_porte(state, n_next)
                ):
                    new_state["coupRestant"] -= 1
                    new_state["mobs"].remove(next_el)
                else:
                    new_state["mobs"].remove(next_el)
                    new_state["mobs"].add(n_next)
                    new_state["coupRestant"] -= 1

            if new_state["me"] in state.piques or case_is_piege(state, new_state["me"]):
                new_state["coupRestant"] -= 1
            for mob in frozenset(new_state["mobs"]):
                if mob in state.piques or case_is_piege(state, mob):
                    new_state["mobs"].remove(mob)
            new_state["mobs"] = frozenset(new_state["mobs"])
            new_state["blocs"] = frozenset(new_state["blocs"])
            new_state["pieges"] = frozenset(switch_traps(new_state["pieges"]))
            yield State(**new_state), direction


def search(
    s_init: State,
    is_final: Callable[[State, FrozenSet[Tuple[int, int]]], bool],
    succ: Callable[[State], Iterator[Tuple[State, str]]],
    remove: Callable[[List[State]], Tuple[State, List[State]]],
    insert: Callable[[State, List[State]], List[State]],
) -> Optional[Tuple[State, Dict[State, Optional[Tuple[State, str]]]]]:
    """
    Fonction de recherche simple avec retour du chemin
    Arguments :
        - s_init: l'état initial
        - is_final: fonction pour verifier si l'état est final
        - succ: fonction successeur
        - remove : fonction pour enlever un element de la pile
        - insert : fonction pour ajouter un element dans la pile
    Retour:
        - l'état final
        _ un dictionnaire permettant de remonter les états
    """
    explo = [s_init]
    save: Dict[State, Optional[Tuple[State, str]]] = {s_init: None}
    while explo:
        state, explo = remove(explo)
        if is_final(state, DEMONES):
            return state, save
        else:
            for new_state, direction in succ(state):
                if not new_state in save:
                    save[new_state] = (state, direction)
                    insert(new_state, explo)
    return None


class HTPriorityItem:
    """Classe pour représenter les états des jeux dans une liste de priorité"""

    def __init__(self, state: State, start: int, score: int) -> None:
        self.state = state
        self.start = start
        self.score = score

    def __lt__(self, other):
        return self.start + self.score < other.start + other.score


def search_sort(
    s_init: State,
    is_final: Callable[[State, FrozenSet[Tuple[int, int]]], bool],
    succ: Callable[[State], Iterator[Tuple[State, str]]],
    score: Callable[[State], int],
) -> Optional[Tuple[State, Dict[State, Optional[Tuple[State, str]]]]]:
    """
    Fonction de recherche pour A* avec retour du chemin
    Arguments :
        - s_init: l'état initial
        - is_final: fonction pour verifier si l'état est final
        - succ: fonction successeur
        - score : la fonction qui determine le "score" d'un état
    Retour:
        - l'état final
        _ un dictionnaire permettant de remonter les états
    """
    explo = [HTPriorityItem(s_init, 0, score(s_init))]
    save: Dict[State, Optional[Tuple[State, str]]] = {s_init: None}
    while explo:
        state_item = heapq.heappop(explo)
        if is_final(state_item.state, DEMONES):
            return state_item.state, save
        else:
            for new_state, direction in succ(state_item.state):
                if not new_state in save:
                    save[new_state] = (state_item.state, direction)
                    heapq.heappush(
                        explo,
                        HTPriorityItem(
                            new_state, state_item.start + 1, score(new_state)
                        ),
                    )
    return None


def rm_largeur(explo):
    """Fonction remove pour l'exploration en largeur"""
    return explo.pop(0), explo


def ins_largeur(state, explo):
    """Fonction inserer pour l'exploration en largeur"""
    explo.append(state)
    return explo


def rm_profondeur(explo):
    """Fonction remove pour l'exploration en profondeur"""
    return explo.pop(), explo


def ins_profondeur(state, explo):
    """Fonction insérer pour l'exploration en profondeur"""
    return explo.append(state)


def dict2path(state_final, path_dict):
    """Algorithme du petit poucet pour recréer le chemin"""
    path = []
    parent = path_dict[state_final]
    while not parent is None:
        path.append(parent[1])
        state_final = parent[0]
        parent = path_dict[state_final]
    path.reverse()
    return "".join(path)


def distance_etat_fin(state: State) -> int:
    """Heuristique prenant en compte la clé """
    dist = 100000
    dist_key = 0
    if state.cle[2]:
        dist_key = abs(state.me[0] - state.cle[0]) + abs(state.me[1] - state.cle[1])
        for demone in DEMONES:
            temp = abs(state.cle[0] - demone[0]) + abs(state.cle[1] - demone[1])
            if temp < dist:
                dist = temp
        return dist_key + dist
    else:
        for demone in DEMONES:
            temp = abs(state.me[0] - demone[0]) + abs(state.me[1] - demone[1])

            if temp < dist:
                dist = temp
        return dist


def distance_etat_fin_no_cle(state: State) -> int:
    """Heuristique ne prenant pas en compte la clé """
    dist = 100000
    for demone in DEMONES:
        temp = abs(state.me[0] - demone[0]) + abs(state.me[1] - demone[1])

        if temp < dist:
            dist = temp
    return dist


def find_plan(infos) -> str:
    """Effectue une recherche A* avec l'heuristique optimale"""
    niveau = grid_to_state(infos)
    global DEMONES
    DEMONES = niveau["demones"]
    global CASES
    CASES = niveau["cases"]
    init_s = niveau["state"]

    heuristique: Callable[[State], int]
    if init_s.cle[2]:
        heuristique = distance_etat_fin
    else:
        heuristique = distance_etat_fin_no_cle

    result = search_sort(init_s, is_next_demone, successeurs, heuristique)
    if result:
        return dict2path(*result)
    return ""


if __name__ == "__main__":

    testProf = timeit.Timer(
        "l = search(s, is_next_demone, successeurs, rm_profondeur, ins_profondeur)",
        "from __main__ import search, s, is_next_demone, pprint, successeurs,\
             rm_profondeur, ins_profondeur, dict2path",
    )
    testLarg = timeit.Timer(
        "l = search(s, is_next_demone, successeurs, rm_largeur, ins_largeur)",
        "from __main__ import search, s, is_next_demone, pprint, successeurs,\
             rm_largeur, ins_largeur, dict2path",
    )
    testAet_noCle = timeit.Timer(
        "l = search_sort(s, is_next_demone, successeurs,distance_etat_fin_no_cle)",
        "from __main__ import search_sort, s, is_next_demone, pprint, successeurs,\
            distance_etat_fin_no_cle, dict2path",
    )
    testAet_Cle = timeit.Timer(
        "l = search_sort(s, is_next_demone, successeurs,distance_etat_fin)",
        "from __main__ import search_sort, s, is_next_demone, pprint, successeurs,\
            distance_etat_fin, dict2path",
    )

    for i in range(1, 10):
        g = grid_from_file("../levels/level{}.txt".format(i))
        jeu = grid_to_state(g)
        DEMONES = jeu["demones"]
        CASES = jeu["cases"]
        s = jeu["state"]

        print("\nRECHERCHE NIVEAU {} :\n--------------------------------".format(i))
        print("profondeur : ", testProf.timeit(1))
        print("largeur: ", testLarg.timeit(1))
        print("A* heuristique sans clé : ", testAet_noCle.timeit(1))
        print("A* heuristique avec clé : ", testAet_Cle.timeit(1))
