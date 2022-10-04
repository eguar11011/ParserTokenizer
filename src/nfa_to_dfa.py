import json
from pprint import pprint
from copy import deepcopy


def set_e_closure(state_set: set[str], nfa):
    """
    Calculates the epsilon-closure of a set of states of a NFA.
    """
    e_closure = state_set
    while True:
        e_closure_prime = deepcopy(e_closure)
        for state in e_closure:
            e_closure_prime |= {
                x[1]
                for x in nfa["transition_function"].get(state, state)
                if x[0] == "$"
            }

        if e_closure_prime == e_closure:
            break
        else:
            e_closure = e_closure_prime

    return e_closure


def move(state_set: set[str], letter: str, nfa: dict):
    """
    Calculates the state set that results from moving from a state in `state_set`
    with a given `letter`
    """
    move_set = set()
    for state in state_set:
        move_set |= {
            x[1] for x in nfa["transition_function"].get(state, []) if x[0] == letter
        }

    return move_set


def set_contruction(nfa: dict):
    """
    Set construction of a DFA from a eps-NFA
    """
    dfa = dict()
    dfa["letters"] = [x for x in nfa["letters"] if x != "$"]
    dfa["transition_function"] = dict()
    dfa["states"] = [set_e_closure(set(nfa["start_states"]), nfa)]
    dfa["start_states"] = [set_e_closure(set(nfa["start_states"]), nfa)]
    dfa["final_states"] = []

    unmarked = [set_e_closure(set(nfa["start_states"]), nfa)]

    while unmarked:
        A = unmarked.pop()
        for letter in dfa["letters"]:
            U = set_e_closure(move(A, letter, nfa), nfa)
            if U not in dfa["states"]:
                if U & set(nfa["final_states"]):
                    dfa["final_states"].append(U)

                dfa["states"].append(U)
                unmarked.append(U)
            dfa["transition_function"][state_set_to_string(A)] = dfa[
                "transition_function"
            ].get(state_set_to_string(A), []) + [
                letter,
                state_set_to_string(U),
            ]

    return dfa


def state_set_to_string(state_set: set[str]):
    return ",".join(sorted(list(state_set), key=lambda x: int(x[1:])))


def load_nfa():
    with open("test_nfa.json", "r") as inpjson:
        nfa = json.loads(inpjson.read())
    return nfa


if __name__ == "__main__":
    nfa = load_nfa()

    dfa = set_contruction(nfa)

    # pprint(nfa.keys())
    # print(nfa.keys())
    # pprint(nfa["transition_function"])
    # pprint(set_e_closure(set(nfa["start_states"]), nfa))
