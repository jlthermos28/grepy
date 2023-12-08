from alphabet import read_alphabet
from testdfa import regex_to_nfa, nfa_to_dfa, test_dfa
from testdot import dfa_to_dot

def main():
    # Read alphabet
    alphabet = read_alphabet("alphabetinput.txt")
    print("Learned alphabet:", alphabet)

    # Convert regex to DFA and export to DOT file
    regex = input("Enter a regular expression (^...$ format): ")
    nfa = regex_to_nfa(regex)
    dfa_start, dfa_states = nfa_to_dfa(nfa)

    dfa_to_dot(dfa_start, dfa_states, "dotfiles/dfa.dot")
    print("DFA has been exported to dotfiles/dfa.dot")

    # Test DFA against text file
    test_results = test_dfa(dfa_start, "alphabetinput.txt")
    for result in test_results:
        print(result)

if __name__ == "__main__":
    main()
