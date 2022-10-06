# Conversion from eps-NFA to DFA

import heapq
from copy import deepcopy


def set_e_closure(state_set: set[str], nfa: dict) -> set[str]:
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


def move(state_set: set[str], letter: str, nfa: dict) -> tuple[set, set]:
    """
    Calculates the state set that results from moving from a state in
    `state_set` with a given `letter`.
    """
    move_set = set()
    S = set()

    for state in state_set:
        for label, state in nfa["transition_function"].get(state, []):
            if label != "$" and intersection(label, letter):
                move_set.add(state)
                S.add(tuple(intersection(label, letter)))

    return move_set, S


def intersection(inter_a, inter_b) -> list[int]:
    """
    Calculates the intersection of two intervals.
    """
    min_inter = min([inter_a, inter_b])
    max_inter = max([inter_a, inter_b])

    if max_inter[0] <= min_inter[1]:
        return [max_inter[0], min_inter[1]]
    else:
        return []


def set_construction(nfa: dict):
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
        for letter in disjoin_intervals(dfa["letters"]):
            state_set, interval = move(A, letter, nfa)

            if not interval:
                continue

            U = set_e_closure(state_set, nfa)

            if U not in dfa["states"]:
                if U & set(nfa["final_states"]):
                    dfa["final_states"].append(U)

                dfa["states"].append(U)
                unmarked.append(U)

            for segment in disjoin_intervals(interval):
                dfa["transition_function"][state_set_to_string(A)] = dfa[
                    "transition_function"
                ].get(state_set_to_string(A), []) + [(segment, state_set_to_string(U))]

    dfa["start_states"] = [state_set_to_string(state) for state in dfa["start_states"]]
    dfa["final_states"] = [state_set_to_string(state) for state in dfa["final_states"]]
    dfa["states"] = [state_set_to_string(state) for state in dfa["states"]]

    return dfa


def state_set_to_string(state_set: set[str]):
    return ",".join(sorted(list(state_set), key=lambda x: int(x[1:])))


def disjoin_intervals(intervals):
    """
    Returns a disjoint list of intervals from the input `input`
    """
    intervals = list(intervals)
    heapq.heapify(intervals)
    disjoint_intervals = []

    while len(intervals) != 1:
        old_min = heapq.heappop(intervals)
        new_min = heapq.heappop(intervals)

        if old_min[1] >= new_min[0]:
            left = (old_min[0], new_min[0])
            right = (new_min[0] + 1, new_min[1])
            disjoint_intervals.append(left)
            heapq.heappush(intervals, right)
        else:
            disjoint_intervals.append(old_min)
            heapq.heappush(intervals, new_min)

    disjoint_intervals.append(intervals.pop())
    return disjoint_intervals


def consume(string: str, dfa: dict):
    current_state = dfa["start_states"][0]
    pos_match = 0

    for idx, char in enumerate(string):
        ordinal = ord(char)
        transition = False
        if current_state in dfa["transition_function"]:
            for label, state in dfa["transition_function"][current_state]:
                if ordinal >= label[0] and ordinal <= label[1]:
                    current_state = state
                    transition = True

            if transition == False:
                return pos_match

            if current_state in dfa["final_states"]:
                pos_match = idx + 1

    return pos_match

