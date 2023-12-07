class State:
    """ A state with one or two edges, all edges labeled by label. """

    def __init__(self, label=None, edges=None):
        self.label = label
        self.edges = edges if edges else []

    def __str__(self):
        return f"State(label={self.label}, edges={self.edges})"

class Fragment:
    """ An NFA fragment with a start state and an accept state. """

    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def regex_to_nfa(pattern):
    """ Convert a regular expression pattern to a NFA. """
    stack = []
    for char in pattern:
        if char == '*':
            frag = stack.pop()
            accept = State()
            start = State(edges=[frag.start, accept])
            frag.accept.edges = [frag.start, accept]
            stack.append(Fragment(start, accept))
        elif char == '|':
            frag2 = stack.pop()
            frag1 = stack.pop()
            accept = State()
            start = State(edges=[frag1.start, frag2.start])
            frag1.accept.edges = [accept]
            frag2.accept.edges = [accept]
            stack.append(Fragment(start, accept))
        else:
            accept = State()
            start = State(char, [accept])
            stack.append(Fragment(start, accept))

    # Simulating the effect of '^' and '$'
    if stack:
        final_frag = stack.pop()
        start_state = State(edges=[final_frag.start])
        final_frag.accept.edges = [State()]
        final_nfa = Fragment(start_state, final_frag.accept.edges[0])
    else:
        raise Exception("Syntax error in regex")

    return final_nfa


if __name__ == "__main__":
    regex = input("Enter a regular expression: ")
    nfa = regex_to_nfa(regex)
    print("NFA for the given regex:", nfa.start)
