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
    
    def move(self, char):
        if char in self.transitions:
            return set(self.transitions[char])
        return set()
    

def nfa_to_dfa(start_state):
    # Mapping from DFA states (represented as frozensets of NFA states) to State objects
    dfa_states = {}

    # The start state of the DFA is the epsilon closure of the NFA's start state
    start_closure = start_state.epsilon_closure()
    dfa_start = State(frozenset(start_closure), any(s.is_accept for s in start_closure))
    dfa_states[frozenset(start_closure)] = dfa_start

    unprocessed_states = [dfa_start]

    while unprocessed_states:
        current_dfa_state = unprocessed_states.pop()
        nfa_state_set = set(current_dfa_state.label)

        # Check transitions for each character
        seen_chars = set()
        for nfa_state in nfa_state_set:
            for char in nfa_state.transitions:
                if char is not None and char not in seen_chars:
                    seen_chars.add(char)

                    # Find the move of the entire NFA state set for this character
                    move_set = set()
                    for state in nfa_state_set:
                        move_set.update(state.move(char))

                    # Compute the epsilon closure of the move set
                    next_states = set()
                    for state in move_set:
                        next_states.update(state.epsilon_closure())

                    next_states_frozenset = frozenset(next_states)
                    if next_states_frozenset not in dfa_states:
                        is_accept = any(s.is_accept for s in next_states)
                        new_dfa_state = State(next_states_frozenset, is_accept)
                        dfa_states[next_states_frozenset] = new_dfa_state
                        unprocessed_states.append(new_dfa_state)

                    # Add transition in the DFA
                    current_dfa_state.add_transition(char, dfa_states[next_states_frozenset])

    return dfa_start, dfa_states  # Return both the start state and all states



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
    dfa = nfa_to_dfa(nfa)

    with open("alphabetinput.txt", "r") as input_file:
        for test_input in input_file:
            test_input = test_input.strip()

            current_state = dfa
            accepted = True
            for char in test_input:
                if char in current_state.transitions:
                    current_state = current_state.transitions[char][0]
                else:
                    accepted = False
                    break

            if accepted and current_state.is_accept:
                print(f"Input: {test_input}, Result: Accepted")
            else:
                print(f"Input: {test_input}, Result: Rejected")

if __name__ == "__main__":
    main()


# Add this function to testdfa.py

def test_dfa(dfa, input_file_path):
    results = []
    with open(input_file_path, "r") as input_file:
        for test_input in input_file:
            test_input = test_input.strip()

            current_state = dfa
            accepted = True
            for char in test_input:
                if char in current_state.transitions:
                    current_state = current_state.transitions[char][0]
                else:
                    accepted = False
                    break

            if accepted and current_state.is_accept:
                results.append(f"Input: {test_input}, Result: Accepted")
            else:
                results.append(f"Input: {test_input}, Result: Rejected")
    
    return results

