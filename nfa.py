class State:
    def __init__(self, accept=False):
        self.accept = accept
        self.transitions = {}

    def add_transition(self, symbol, state):
        if symbol in self.transitions:
            self.transitions[symbol].append(state)
        else:
            self.transitions[symbol] = [state]

class NFA:
    def __init__(self):
        self.start_state = State()
        self.states = [self.start_state]

    def add_state(self, accept=False):
        state = State(accept)
        self.states.append(state)
        return state
    
    def to_dot_format(self):
        dot_str = "digraph NFA {\n"
        dot_str += "    rankdir=LR;\n"
        dot_str += "    node [shape = doublecircle];\n"

        # Mark accept states
        for state in self.states:
            if state.accept:
                dot_str += f"    {id(state)} [label=\"{id(state)}\"];\n"

        dot_str += "    node [shape = circle];\n"

        # Transitions
        for state in self.states:
            for symbol, next_states in state.transitions.items():
                for next_state in next_states:
                    dot_str += f"    {id(state)} -> {id(next_state)} [label=\"{symbol}\"];\n"

        dot_str += "}\n"
        return dot_str

def regex_to_nfa(regex):
    nfa_stack = []

    for char in regex:
        if char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa_stack.append(union(nfa1, nfa2))
        elif char == '*':
            nfa1 = nfa_stack.pop()
            nfa_stack.append(kleene_star(nfa1))
        else:
            nfa_stack.append(single_char_nfa(char))

    return nfa_stack.pop()

def single_char_nfa(char):
    start = State()
    accept = State(True)
    start.add_transition(char, accept)
    return NFA(start, [accept])

def union(nfa1, nfa2):
    start = State()
    accept = State(True)

    start.epsilon_transitions.append(nfa1.start_state)
    start.epsilon_transitions.append(nfa2.start_state)

    for accept_state in nfa1.accept_states:
        accept_state.epsilon_transitions.append(accept)
    for accept_state in nfa2.accept_states:
        accept_state.epsilon_transitions.append(accept)

    return NFA(start, [accept])

def kleene_star(nfa):
    start = State()
    accept = State(True)

    start.epsilon_transitions.append(nfa.start_state)
    start.epsilon_transitions.append(accept)

    for accept_state in nfa.accept_states:
        accept_state.epsilon_transitions.append(nfa.start_state)
        accept_state.epsilon_transitions.append(accept)

    return NFA(start, [accept])

if __name__ == "__main__":
    regex = input("Enter a regular expression: ")
    nfa = regex_to_nfa(regex)
    # Code to visualize or test the NFA
