# In export_dfa_to_dot.py
import os
from testdfa import regex_to_nfa, nfa_to_dfa

def dfa_to_dot(dfa_start, dfa_states, filename):
    state_id_map = {state: f"S{i}" for i, state in enumerate(dfa_states)}

    with open(filename, 'w') as file:
        file.write("digraph DFA {\n")
        file.write("    rankdir=LR;\n")
        file.write("    node [shape = doublecircle]; " + " ".join([state_id_map[state] for state in dfa_states if dfa_states[state].is_accept]) + ";\n")
        file.write("    node [shape = circle];\n")

        for state, state_obj in dfa_states.items():
            for char, targets in state_obj.transitions.items():
                for target in targets:
                    file.write(f"    \"{state_id_map[state]}\" -> \"{state_id_map[target.label]}\" [ label = \"{char}\" ];\n")

        file.write("}\n")


if __name__ == "__main__":
    regex = input("Enter a regular expression (^...$ format): ")
    nfa = regex_to_nfa(regex)
    dfa_start, dfa_states = nfa_to_dfa(nfa)  # Receive both the start state and all states

    if not os.path.exists("dotfiles"):
        os.makedirs("dotfiles")

    dfa_to_dot(dfa_start, dfa_states, "dotfiles/dfa.dot")
    print("DFA has been exported to dotfiles/dfa.dot")
