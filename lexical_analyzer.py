import re

# C language keywords
keywords = {
    "auto", "break", "case", "char", "const", "continue",
    "default", "do", "double", "else", "enum", "extern",
    "float", "for", "goto", "if", "int", "long",
    "register", "return", "short", "signed", "sizeof",
    "static", "struct", "switch", "typedef", "union",
    "unsigned", "void", "volatile", "while"
}

# Operators
operators = {
    "+", "-", "*", "/", "%", "=",
    "==", "!=", "<", ">", "<=", ">=",
    "++", "--", "+=", "-=", "*=", "/=",
    "&&", "||", "!"
}

# Separators / Delimiters
separators = {
    "(", ")", "{", "}", "[", "]",
    ";", ",", ":"
}

# Special symbols
special_symbols = {
    "#", ".", "?", "~"
}


def lexical_analyzer(filename):
    try:
        with open(filename, "r") as file:
            source_code = file.read()
    except FileNotFoundError:
        print("Error: Input file not found.")
        return

    # Remove comments while counting them
    single_line_comments = re.findall(r'//.*', source_code)
    multi_line_comments = re.findall(r'/\*[\s\S]*?\*/', source_code)

    comment_count = len(single_line_comments) + len(multi_line_comments)

    # Remove comments for token analysis
    source_code = re.sub(r'//.*', '', source_code)
    source_code = re.sub(r'/\*[\s\S]*?\*/', '', source_code)

    # Token pattern
    token_pattern = r'''
        "(?:\\.|[^"\\])*"          | # String literals
        '(?:\\.|[^'\\])*'          | # Character literals
        \d+(?:\.\d+)?              | # Numbers
        ==|!=|<=|>=|\+\+|--|\+=|-=  | # Multi-character operators
        \*=|/=|&&|\|\|             |
        [A-Za-z_][A-Za-z0-9_]*     | # Identifiers / keywords
        [+\-*/%=<>!&|]             | # Operators
        [(){}\[\];,:]              | # Separators
        [#.?~]                       # Special symbols
    '''

    tokens = re.findall(token_pattern, source_code, re.VERBOSE)

    counts = {
        "Keywords": 0,
        "Identifiers": 0,
        "Operators": 0,
        "Constants/Literals": 0,
        "Separators/Delimiters": 0,
        "Special Symbols": 0
    }

    print("\n========== TOKENS ==========\n")

    for token in tokens:

        if token in keywords:
            token_type = "Keyword"
            counts["Keywords"] += 1

        elif token in operators:
            token_type = "Operator"
            counts["Operators"] += 1

        elif token in separators:
            token_type = "Separator/Delimiter"
            counts["Separators/Delimiters"] += 1

        elif token in special_symbols:
            token_type = "Special Symbol"
            counts["Special Symbols"] += 1

        elif re.fullmatch(r'\d+(?:\.\d+)?', token):
            token_type = "Constant"
            counts["Constants/Literals"] += 1

        elif token.startswith('"') or token.startswith("'"):
            token_type = "Literal"
            counts["Constants/Literals"] += 1

        elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', token):
            token_type = "Identifier"
            counts["Identifiers"] += 1

        else:
            continue

        print(f"{token_type:<20}: {token}")

    print("\n========== TOKEN COUNT ==========\n")

    for token_type, count in counts.items():
        print(f"{token_type:<25}: {count}")

    print(f"{'Comments':<25}: {comment_count}")

    # Save output
    with open("output.txt", "w") as output:
        output.write("========== TOKEN COUNT ==========\n\n")

        for token_type, count in counts.items():
            output.write(f"{token_type:<25}: {count}\n")

        output.write(f"{'Comments':<25}: {comment_count}\n")

    print("\nOutput saved to output.txt")


# Main program
if __name__ == "__main__":
    print("===== LEXICAL ANALYZER & TOKEN COUNTER =====")

    filename = input("Enter input file name: ")

    lexical_analyzer(filename)