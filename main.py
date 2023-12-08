import alphabet  # Import the alphabet.py module
import dfa  # Assuming dfa.py contains the necessary functions and classes for DFA
from nfa import regex_to_postfix, regex_to_nfa  # Import relevant functions from nfa.py

def main():
    # Call the read_alphabet function from alphabet.py
    alphabet_set = alphabet.read_alphabet("alphabetinput.txt")
    print("Learned alphabet:", alphabet_set)

    # Take regex input from user
    infix_regex = input("Enter a regular expression (should start with ^ and end with $): ")

    # Validate the input
    if not infix_regex.startswith('^') or not infix_regex.endswith('$'):
        print("Error: The regular expression must start with '^' and end with '$'.")
        return

    # Remove ^ and $ for processing
    infix_regex = infix_regex[1:-1]

    # Convert infix regex to postfix
    postfix_regex = regex_to_postfix(infix_regex)

    # Convert postfix regex to NFA
    nfa_instance = regex_to_nfa(postfix_regex)

    if nfa_instance:
        print("NFA created successfully.")
        # Test if the NFA accepts or rejects lines from alphabetinput.txt
        with open("alphabetinput.txt", "r") as input_file:
            for line in input_file:
                # Remove trailing newline character
                line = line.strip()
                # Check if the NFA accepts or rejects the line
                if nfa_instance.accepts(line):
                    result = "Accepted"  
                else: 
                    result = "Rejected"
                print(f"Input: {line}, Result: {result}")
    else:
        print("Error in creating NFA.")

if __name__ == "__main__":
    main()
