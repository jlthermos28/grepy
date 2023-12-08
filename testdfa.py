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
    
class NFA:
    def __init__(self, start_state, states):
        self.start_state = start_state
        self.states = states

    

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
    # Stack for holding NFAs
    nfa_stack = []

    for char in regex:
        if char == '*':
            # Pop the last NFA and apply Kleene star
            last_nfa = nfa_stack.pop()
            nfa_star = apply_kleene_star(last_nfa)
            nfa_stack.append(nfa_star)
        elif char == '|':
            # Assuming that | is binary (i.e., there are two operands, one before and one after the |)
            nfa_right = nfa_stack.pop()
            nfa_left = nfa_stack.pop()
            nfa_union = create_union_nfa(nfa_left, nfa_right)
            nfa_stack.append(nfa_union)
        else:
            # Create a basic NFA for a single character
            new_nfa = create_basic_nfa(char)
            nfa_stack.append(new_nfa)

    # Combine all NFAs in the stack to form the final NFA
    final_nfa = combine_nfas(nfa_stack)
    return final_nfa

def apply_kleene_star(sub_nfa):
    new_start = State("new_start")
    new_accept = State("new_accept", is_accept=True)

    # Connect the new start to the sub-NFA's start state and directly to new accept state
    new_start.add_transition(None, sub_nfa.start_state)
    new_start.add_transition(None, new_accept)

    # Ensure all accept states of the sub-NFA transition to new accept and loop back
    for state in sub_nfa.states:
        if state.is_accept:
            state.add_transition(None, new_accept)
            state.add_transition(None, new_start)
            state.is_accept = False

    new_accept.add_transition(None, new_start)  # Allows for repeated occurrences

    sub_nfa.states.add(new_start)
    sub_nfa.states.add(new_accept)
    return NFA(new_start, sub_nfa.states.union({new_accept}))




def create_union_nfa(nfa1, nfa2):
    # Create new start and accept states
    new_start = State("new_start")
    new_accept = State("new_accept", is_accept=True)

    # Add epsilon transitions from the new start state to the start states of nfa1 and nfa2
    new_start.add_transition(None, nfa1.start_state)
    new_start.add_transition(None, nfa2.start_state)

    # Add epsilon transitions from the accept states of nfa1 and nfa2 to the new accept state
    for state in nfa1.states.union(nfa2.states):
        if state.is_accept:
            state.is_accept = False  # Old accept states are no longer accept states
            state.add_transition(None, new_accept)

    # Combine the states from nfa1 and nfa2 with the new start and accept states
    combined_states = nfa1.states.union(nfa2.states, {new_start, new_accept})

    # Return the new NFA
    return NFA(new_start, combined_states)


def create_basic_nfa(char):
    # Create start and accept states
    start_state = State("start")
    accept_state = State("accept", is_accept=True)

    # Add a transition for the character
    start_state.add_transition(char, accept_state)

    # The set of states includes both the start and accept states
    states = {start_state, accept_state}

    # Return the NFA
    return NFA(start_state, states)


def combine_nfas(nfa_stack):
    if not nfa_stack:
        raise ValueError("No NFAs to combine")

    if len(nfa_stack) == 1:
        return nfa_stack[0]

    # Initialize combined NFA starting with the first NFA in the stack
    combined_nfa = nfa_stack[0]

    for next_nfa in nfa_stack[1:]:
        # Connect accept states of current NFA to start state of next NFA
        for state in combined_nfa.states:
            if state.is_accept:
                state.add_transition(None, next_nfa.start_state)
                state.is_accept = False

        combined_nfa.states.update(next_nfa.states)

    # Mark the accept states of the last NFA in the stack as accept states of the combined NFA
    for state in nfa_stack[-1].states:
        if state.is_accept:
            state.is_accept = True

    return combined_nfa



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




def test_dfa(dfa, input_file_path):
    results = []
    with open(input_file_path, "r") as input_file:
        for test_input in input_file:
            test_input = test_input.strip()

            # Start at the DFA's start state
            current_state = dfa

            # Add handling for the start anchor (^)
            if '^' in current_state.transitions:
                current_state = current_state.transitions['^'][0]
            else:
                results.append(f"Input: {test_input}, Result: Rejected")
                continue

            accepted = True
            for char in test_input:
                if char in current_state.transitions:
                    current_state = current_state.transitions[char][0]
                else:
                    accepted = False
                    break

            # Add handling for the end anchor ($)
            if accepted and '$' in current_state.transitions:
                current_state = current_state.transitions['$'][0]
                if not current_state.is_accept:
                    accepted = False

            if accepted and current_state.is_accept:
                results.append(f"Input: {test_input}, Result: Accepted")
            else:
                results.append(f"Input: {test_input}, Result: Rejected")
    
    return results

