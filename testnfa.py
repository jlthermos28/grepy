class State:
    def __init__(self, label, is_accept=False):
        self.label = label
        self.is_accept = is_accept
        self.transitions = {}

    def add_transition(self, char, target_state):
        if char in self.transitions:
            self.transitions[char].append(target_state)
        else:
            self.transitions[char] = [target_state]

    def epsilon_closure(self):
        closure = set()
        stack = [self]

        while stack:
            state = stack.pop()
            closure.add(state)

            if None in state.transitions:
                for target_state in state.transitions[None]:
                    if target_state not in closure:
                        stack.append(target_state)

        return closure

def regex_to_nfa(regex):
    start_state = State("start")
    accept_state = State("accept", is_accept=True)
    start_state.add_transition(None, accept_state)

    current_state = start_state

    for char in regex:
        if char == '^':
            continue
        elif char == '$':
            current_state.add_transition(None, accept_state)
        else:
            new_state = State(char)
            current_state.add_transition(char, new_state)
            current_state = new_state

    return start_state

def main():
    regex = input("Enter a regular expression (^...$ format): ")
    nfa = regex_to_nfa(regex)

    with open("alphabetinput.txt", "r") as input_file:
        for test_input in input_file:
            test_input = test_input.strip()

            current_states = nfa.epsilon_closure()
            for char in test_input:
                next_states = set()
                for state in current_states:
                    if char in state.transitions:
                        next_states.update(state.transitions[char])
                current_states = set()
                for state in next_states:
                    current_states.update(state.epsilon_closure())

            if any(state.is_accept for state in current_states):
                print(f"Input: {test_input}, Result: Accepted")
            else:
                print(f"Input: {test_input}, Result: Rejected")

if __name__ == "__main__":
    main()
