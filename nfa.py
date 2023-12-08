class State:
    def __init__(self, label=None, edges=None, is_accept=False):
        self.label = label
        self.edges = edges if edges else []
        self.is_accept = is_accept  # Indicates if this state is an accepting state
    def epsilon_closure(self, seen=None):
        if seen is None:
            seen = set()
        if self not in seen:
            seen.add(self)
            for edge in self.edges:
                if edge.label is None:  # Epsilon transition
                    edge.epsilon_closure(seen)
        return seen

    def match(self, input_str):
        if not input_str:
            return self.is_accept

        for edge in self.edges:
            if edge.label == input_str[0]:
                return edge.target.match(input_str[1:])
        return False


class Fragment:
    """ An NFA fragment with a start state and an accept state. """
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept
    
    def accepts(self, input_str):
        for state in self.start.epsilon_closure():
            if state.match(input_str):
                return True
        return False

def regex_to_postfix(infix_regex):
    """ Convert infix regex to postfix. """
    precedence = {'*': 3, '.': 2, '|': 1}
    postfix, stack = "", []

    for char in infix_regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()  # Pop '('
        elif char in precedence:
            while stack and precedence.get(stack[-1], 0) >= precedence[char]:
                postfix += stack.pop()
            stack.append(char)
        else:
            postfix += char

    while stack:
        postfix += stack.pop()

    return postfix

def regex_to_nfa(postfix):
    stack = []
    for char in postfix:
        if char == '.':
            frag2 = stack.pop()
            frag1 = stack.pop()
            frag1.accept.edges.append(frag2.start)
            stack.append(Fragment(frag1.start, frag2.accept))
        elif char == '|':
            frag2 = stack.pop()
            frag1 = stack.pop()
            accept = State()
            start = State(edges=[frag1.start, frag2.start])
            frag1.accept.edges.append(accept)
            frag2.accept.edges.append(accept)
            stack.append(Fragment(start, accept))
        elif char == '*':
            frag = stack.pop()
            accept = State()
            start = State(edges=[frag.start, accept])
            frag.accept.edges.append(frag.start)
            frag.accept.edges.append(accept)
            stack.append(Fragment(start, accept))
        else:
            accept = State()
            start = State(label=char, edges=[accept])
            stack.append(Fragment(start, accept))

    return stack.pop() if stack else None

# Taking user input for regex
infix_regex = input("Enter a regular expression (should start with ^ and end with $): ")

# Validate the input
if not infix_regex.startswith('^') or not infix_regex.endswith('$'):
    print("Error: The regular expression must start with '^' and end with '$'.")
else:
    # Remove ^ and $ for processing
    infix_regex = infix_regex[1:-1]
    postfix_regex = regex_to_postfix(infix_regex)
    nfa = regex_to_nfa(postfix_regex)

    if nfa:
        print("NFA created successfully.")
    else:
        print("Error in creating NFA.")



if __name__ == "__main__":
    # Taking user input for regex
    infix_regex = input("Enter a regular expression (should start with ^ and end with $): ")

    # Validate the input
    if not infix_regex.startswith('^') or not infix_regex.endswith('$'):
        print("Error: The regular expression must start with '^' and end with '$'.")
    else:
        # Remove ^ and $ for processing
        infix_regex = infix_regex[1:-1]
        postfix_regex = regex_to_postfix(infix_regex)
        nfa = regex_to_nfa(postfix_regex)

        if nfa:
            print("NFA created successfully.")
        else:
            print("Error in creating NFA.")