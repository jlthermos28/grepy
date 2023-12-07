def nfa_to_dfa(nfa):
    """
    Converts an NFA to a DFA using the subset construction algorithm.
    
    :param nfa: The NFA to convert.
    :return: A DFA.
    """
    initial_state = frozenset(get_closure(nfa.start))  # Start with the closure of the NFA's start state
    dfa_states = {initial_state: State()}
    unprocessed_states = [initial_state]
    dfa_accept_states = []

    while unprocessed_states:
        current = unprocessed_states.pop()
        for input_symbol in get_input_symbols(nfa):
            # Determine the set of NFA states reachable from 'current' on 'input_symbol'
            new_state = frozenset(transition(current, input_symbol))

            if new_state not in dfa_states:
                dfa_states[new_state] = State()
                unprocessed_states.append(new_state)

            # Add a transition in the DFA for this input symbol
            dfa_states[current].add_transition(input_symbol, dfa_states[new_state])

            # If any NFA accept state is in 'new_state', mark the corresponding DFA state as accept
            if any(state in nfa.accept_states for state in new_state):
                dfa_accept_states.append(dfa_states[new_state])

    return DFA(dfa_states[initial_state], dfa_accept_states)

def get_closure(state):
    """
    Computes the epsilon-closure of a given state in an NFA. The epsilon-closure
    is the set of states reachable from the given state on epsilon-transitions (transitions
    with None as the input symbol).
    
    :param state: The state for which epsilon-closure is to be computed.
    :return: A set containing all states in the epsilon-closure of the given state.
    """
    closure = set([state])
    stack = [state]

    while stack:
        current_state = stack.pop()
        for edge in current_state.edges:
            if edge.label is None and edge not in closure:
                closure.add(edge)
                stack.append(edge)

    return closure


def get_input_symbols(nfa):
    """
    Returns the set of input symbols for the given NFA, excluding epsilon (None) transitions.
    
    :param nfa: The NFA whose input symbols are to be extracted.
    :return: A set of input symbols used in the NFA.
    """
    symbols = set()
    states_to_process = [nfa.start]

    # Using a set to keep track of processed states to avoid infinite loops in cyclic NFAs
    processed_states = set()

    while states_to_process:
        state = states_to_process.pop()
        if state in processed_states:
            continue

        processed_states.add(state)

        if state.edges:
            for edge in state.edges:
                if edge.label is not None:
                    symbols.add(edge.label)
                if edge not in processed_states:
                    states_to_process.append(edge)

    return symbols


def transition(states, input_symbol):
    """
    Computes the set of states that can be reached from the given set of states on the given input symbol.
    This includes following any epsilon-transitions from the reached states.

    :param states: A set of states in the NFA.
    :param input_symbol: The input symbol for which the transitions are to be determined.
    :return: A set of states that are reachable from the input states on the given input symbol.
    """
    result = set()
    for state in states:
        for edge in state.edges:
            if edge.label == input_symbol:
                result.update(get_closure(edge))

    return result


# Definitions for State, DFA, etc., would also be required here

class State:
    """
    Represents a state in a DFA. Each state has transitions to other states
    based on input symbols.
    """
    def __init__(self):
        self.transitions = {}  # Dictionary mapping input symbols to States

    def add_transition(self, symbol, state):
        """
        Add a transition from this state to another state on a given input symbol.
        """
        self.transitions[symbol] = state

class DFA:
    """
    Represents a Deterministic Finite Automaton.
    """
    def __init__(self, start_state, accept_states):
        self.start_state = start_state
        self.accept_states = set(accept_states)

    def accepts(self, input_string):
        """
        Check if the DFA accepts a given input string.
        """
        current_state = self.start_state
        for symbol in input_string:
            if symbol in current_state.transitions:
                current_state = current_state.transitions[symbol]
            else:
                return False
        return current_state in self.accept_states
