from nfa import regex_to_nfa
from dfa import nfa_to_dfa, process_file
from alphabet import read_file, extract_alphabet
import os

def main():
    regex = input("Enter a regular expression: ")
    file_path = "alphabetinput.txt"  
    file_contents = read_file(file_path)
    alphabet = extract_alphabet(file_contents)
    print(f"Alphabet in the file: {alphabet}")

    # Generate NFA from regex
    nfa = regex_to_nfa(regex)

    # Convert NFA to DFA
    dfa = nfa_to_dfa(nfa)

    # Process the file with DFA
    process_file(file_path, dfa)

    # Output NFA and DFA in DOT format
    with open("nfa.dot", "w") as nfa_file:
        nfa_file.write(nfa.to_dot_format())

    with open("dfa.dot", "w") as dfa_file:
        dfa_file.write(dfa.to_dot_format())

    # Ensure 'dotfiles' subdirectory exists
    os.makedirs("dotfiles", exist_ok=True)

    # Output NFA and DFA in DOT format in the 'dotfiles' subfolder
    with open("dotfiles/nfa.dot", "w") as nfa_file:
        nfa_file.write(nfa.to_dot_format())

    with open("dotfiles/dfa.dot", "w") as dfa_file:
        dfa_file.write(dfa.to_dot_format())

if __name__ == "__main__":
    main()
