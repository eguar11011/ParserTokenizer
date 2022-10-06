from graphviz import Digraph


def draw_dfa(dfa, title=""):
    state_name = {}
    i = 0
    for state in dfa["states"]:
        state_name[state] = "q{}".format(i).translate(
            str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        )
        i += 1

    dfa_graph = Digraph()
    dfa_graph.attr(rankdir="LR")

    if title == "":
        title = r"\n\nDFA"
    else:
        title = r"\n\nDFA: " + title
    dfa_graph.attr(label=title, fontsize="25")

    # mark final states
    dfa_graph.attr("node", shape="doublecircle")
    for state in dfa["final_states"]:
        dfa_graph.node(state_name[state])

    # add an initial edge
    dfa_graph.attr("node", shape="none")
    dfa_graph.node("")

    dfa_graph.attr("node", shape="circle")
    dfa_graph.edge("", state_name[dfa["start_states"][0]])

    for state, transitions in dfa["transition_function"].items():
        for transition in transitions:
            interval, transition_state = transition
            dfa_graph.edge(
                state_name[state],
                state_name[transition_state],
                label=interval_to_string(interval),
            )

    return dfa_graph


def interval_to_string(interval):
    left, right = interval

    if left == right:
        return chr(left)
    else:
        return f"{chr(left)}-{chr(right)}"
