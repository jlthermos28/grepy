def read_alphabet(file_path):
    """
    Reads the alphabet from a given text file. Each line in the file is assumed to be a string
    containing characters from the alphabet.
    
    :param file_path: Path to the text file containing the alphabet.
    :return: A set containing unique alphabet characters.
    """
    alphabet = set()

    with open(file_path, 'r') as file:
        for line in file:
            # Add each character in the line to the alphabet set
            alphabet.update(line.strip())

    return alphabet

if __name__ == "__main__":
    alphabet = read_alphabet("alphabetinput.txt")
    print("Learned alphabet:", alphabet)
