from nfa import nfa  # Import the NFA from nfa.py
import os 


class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = frozenset(nfa_states)
        self.is_accept = any(state.is_accept for state in nfa_states)
        self.transitions = {}  # Dictionary to hold state transitions

    def add_transition(self, symbol, state):
        self.transitions[symbol] = state

def epsilon_closure(state, seen=None):
    """ Find the epsilon closure of a given NFA state. """
    if seen is None:
        seen = set()
    if state not in seen:
        seen.add(state)
        for edge in state.edges:
            if edge.label is None:  # Epsilon transition
                epsilon_closure(edge, seen)
    return seen

def move(states, symbol):
    """ Return the set of states to which there is a transition on symbol from any state in states. """
    return set(edge for state in states for edge in state.edges if edge.label == symbol)

def nfa_to_dfa(nfa):
    initial_closure = epsilon_closure(nfa.start)
    dfa_start = DFAState(initial_closure)
    states = {dfa_start.nfa_states: dfa_start}
    unmarked = [dfa_start]

    while unmarked:
        current = unmarked.pop()
        for symbol in set(edge.label for state in current.nfa_states for edge in state.edges if edge.label):
            target_closure = epsilon_closure(move(current.nfa_states, symbol))
            target_state = states.get(target_closure)
            if target_state is None:
                target_state = DFAState(target_closure)
                states[target_closure] = target_state
                unmarked.append(target_state)
            # Here you would add the transition from current to target_state on symbol
            current.add_transition(symbol, target_state)
    return states.values()  # Return the set of DFA states

def dfa_to_dot(dfa_states, filename="dfa_graph.dot"):
    subfolder = "dotfiles"
    os.makedirs(subfolder, exist_ok=True)  # Create the subfolder if it doesn't exist

    dot_str = "digraph DFA {\n"
    dot_str += "    rankdir=LR;\n"
    dot_str += "    node [shape = doublecircle];\n"

    # Mark accepting states
    for state in dfa_states:
        if state.is_accept:
            dot_str += f"    \"{state}\";\n"

    dot_str += "    node [shape = circle];\n"

    # Transitions
    for state in dfa_states:
        for symbol, next_state in state.transitions:  # Assuming each state has a 'transitions' attribute
            dot_str += f"    \"{state}\" -> \"{next_state}\" [ label = \"{symbol}\" ];\n"

    dot_str += "}"

    output_path = os.path.join(subfolder,filename)

    # Write to file
    with open(output_path, 'w') as file:
        file.write(dot_str)


# Convert NFA to DFA
dfa_states = nfa_to_dfa(nfa)


# Call the dfa_to_dot function with the desired filename (e.g., 'my_dfa_graph.dot')
dfa_to_dot(dfa_states, filename="my_dfa_graph.dot")