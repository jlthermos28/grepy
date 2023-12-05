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

if __name__ == "__main__":
    # Example usage
    file_path = "input.txt"
    contents = read_file(file_path)
    alphabet = extract_alphabet(contents)
    print("Alphabet:", alphabet)
