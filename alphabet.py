def read_file(file_path):
    """
    Reads the contents of a file and returns it as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_alphabet(file_contents):
    """
    Extracts the unique characters from the file contents and returns them as a set.
    """
    return set(file_contents)

def read_alphabet_from_file(file_path="alphabetinput.txt"):
    """
    Reads the contents of 'alphabetinput.txt' and returns the unique characters as a set.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return set(file.read())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return set()

if __name__ == "__main__":
    # Example usage for reading from 'alphabetinput.txt'
    default_alphabet = read_alphabet_from_file()
    print("Alphabet from 'alphabetinput.txt':", default_alphabet)