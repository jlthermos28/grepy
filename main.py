# Import necessary functions from other modules
from alphabet import read_alphabet
from nfa import regex_to_nfa
from dfa import nfa_to_dfa
from dfaoutput import process_file
import os

def main():
    # Step 1: Read and Learn the Alphabet
    alphabet = read_alphabet("alphabetinput.txt")
    print("Learned alphabet:", alphabet)

    # Step 2: Input Regular Expression
    regex = input("Enter a regular expression: ")

    # Step 3: Convert Regex to NFA
    nfa = regex_to_nfa(regex)

    # Step 4: Convert NFA to DFA
    dfa = nfa_to_dfa(nfa)

    # Step 5: Process File and Output Results
    input_file = "alphabetinput.txt"
    output_folder = "dotfiles"
    output_file = os.path.join(output_folder, "results.dot")
    process_file(input_file, dfa, output_file)
    print(f"Results written to {output_file}")

if __name__ == "__main__":
    main()
