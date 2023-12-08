import os

def dfa_to_dot(dfa_states, filename="dfa_graph.dot"):
    dot_str = "digraph DFA {\n"
    dot_str += "    rankdir=LR;\n"
    dot_str += "    node [shape = doublecircle];\n"

    # Mark accepting states
    for state in dfa_states:
        if state.is_accept:
            dot_str += f"    {id(state)};\n"

    dot_str += "    node [shape = circle];\n"

    # Transitions
    for state in dfa_states:
        for (symbol, next_state) in state.transitions:  # Assuming state.transitions is a list of (symbol, next_state) tuples
            dot_str += f"    {id(state)} -> {id(next_state)} [ label = \"{symbol}\" ];\n"

    dot_str += "}"

    # Create 'dotfiles' directory if it doesn't exist
    os.makedirs('dotfiles', exist_ok=True)

    # Write to file
    with open(f'dotfiles/{filename}', 'w') as file:
        file.write(dot_str)

# Example usage
# dfa_states = ... # Your DFA states
# dfa_to_dot(dfa_states)
