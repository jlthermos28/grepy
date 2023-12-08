class State:
    def __init__(self, accept=False):
        self.accept = accept
        self.edges = {}  # Dictionary to hold transitions: {character: state}

class NFA:
    def __init__(self, start_state):
        self.start_state = start_state

def regex_to_nfa(regex):
    if not regex.startswith('^') or not regex.endswith('$'):
        raise ValueError("Regex must start with '^' and end with '$'")

    # Remove ^ and $ since they are not to be processed in the loop
    regex = regex[1:-1]

    nfa_stack = []

    for char in regex:
        if char == '*':
            nfa = nfa_stack.pop()
            start = State()
            accept = State(accept=True)
            start.edges[''] = [nfa.start_state, accept]
            nfa.start_state.edges[''] = [accept, nfa.start_state]
            nfa_stack.append(NFA(start))
        elif char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            start = State()
            accept = State(accept=True)
            start.edges[''] = [nfa1.start_state, nfa2.start_state]
            for state in [nfa1.start_state, nfa2.start_state]:
                if state.accept:
                    state.accept = False
                    state.edges[''] = [accept]
            nfa_stack.append(NFA(start))
        else:
            accept = State(accept=True)
            start = State()
            start.edges[char] = [accept]
            nfa_stack.append(NFA(start))

    while len(nfa_stack) > 1:
        nfa2 = nfa_stack.pop()
        nfa1 = nfa_stack.pop()
        nfa1.start_state.edges[''] = [nfa2.start_state]
        nfa_stack.append(NFA(nfa1.start_state))

    # The final NFA should start with a special start state and end with a special end state
    final_nfa = nfa_stack.pop()
    start_state = State()
    end_state = State(accept=True)

    # Connect the start state to the NFA's start state
    start_state.edges[''] = [final_nfa.start_state]

    # Correctly iterating over the states to find the accept state
    for state in final_nfa.start_state.edges.values():
        for s in state:
            if s.accept:
                s.accept = False
                s.edges[''] = [end_state]

    return NFA(start_state)

# Example usage
nfa = regex_to_nfa("^a*b|c$")


def match(nfa, string):
    def dfs(state, pos):
        if pos == len(string):
            return state.accept
        if string[pos] in state.edges:
            for next_state in state.edges[string[pos]]:
                if dfs(next_state, pos + 1):
                    return True
        if '' in state.edges:
            for next_state in state.edges['']:
                if dfs(next_state, pos):
                    return True
        return False

    return dfs(nfa.start_state, 0)

# Create NFA from regex
nfa = regex_to_nfa("^a*b|c$")

# Test strings
test_strings = ["ab", "aab", "b", "c", "ac", "abc", "aabc"]

# Check each string
for s in test_strings:
    print(f"Does '{s}' match '^a*b|c$'? {match(nfa, s)}")

