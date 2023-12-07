import os
from dfa import DFA, State
import pickle

# Assuming DFA and State classes are defined here or imported
# from dfa.py or another module

def read_dfa(file_path):
    """
    Reads a serialized DFA from a file and returns the DFA object.

    :param file_path: Path to the file containing the serialized DFA.
    :return: Deserialized DFA object.
    """
    with open(file_path, 'rb') as file:
        dfa = pickle.load(file)
    return dfa


def process_file(input_file, dfa, output_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    with open(output_file, 'w') as file:
        for line in lines:
            line = line.strip()
            result = "Accept" if dfa.accepts(line) else "Reject"
            file.write(f"{line}: {result}\n")

def main():
    dfa = read_dfa()  # Initialize your DFA here

    input_file = "alphabetinput.txt"
    output_folder = "dotfiles"
    output_file = os.path.join(output_folder, "results.dot")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    process_file(input_file, dfa, output_file)

if __name__ == "__main__":
    main()
