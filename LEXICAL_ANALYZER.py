import re

# Token classes
TOKEN_KEYWORD = 'Keyword'
TOKEN_IDENTIFIER = 'ID'
TOKEN_NUMBER = 'Int Const'
TOKEN_OPERATOR = 'Operator'
TOKEN_DATATYPE = 'DataType'
TOKEN_UNKNOWN = 'Unknown'
TOKEN_FLOATCONST = 'Float Const'
TOKEN_CHARCONST = 'Char Const'
TOKEN_STRINGCONST = 'String Const'


# Keywords and operators

keywords = {
    'sealed': 'sealed',
    'abstract':'abstract',
    'while': 'while',
    'for': 'for',
    'if': 'if',
    'else': 'else',
    'do': 'do',
    'switch': 'switch',
    'case': 'case',
    'default': 'default',
    'void': 'void',
    'break': 'break_Continue',
    'continue': 'break_Continue',
    'return': 'return',
    'class': 'class',
    'enum': 'enum',
    'private': 'Access Modifier',
    'public': 'Access Modifier',
    'protected': 'Access_Modifiers',
    'static': 'static',
    'virtual': 'virtual',
    'this': 'this',
    'super': 'Super',
    'arr': 'Array',
    'main': 'main',
    'int': 'DataType',
    'float': 'DataType',
    'char': 'DataType',
    'double': 'DataType',
    'string': 'DataType',
}

operators = {
    '++': 'inc/dec',
    '--': 'inc/dec',
    '+=': 'PMMDM',
    '*=': 'PMMDM',
    '-=': 'PMMDM',
    '/=': 'PMMDM',
    '%=': 'PMMDM',
    '+': 'PM',
    '-': 'PM',
    '*': 'MDM',
    '/': 'MDM',
    '%': 'MDM',
    '<': 'RO',
    '>': 'RO',
    '<=': 'RO',
    '>=': 'RO',
    '!=': 'RO',
    '==': 'RO',
    '&&': 'LO',
    '||': 'LO',
    '!': '!',
    '=': '=',
    ':': ':',
    '.': '.',
    ',': ',',
    '(': '(',
    ')': ')',
    '{': '{', 
    '}': '}',
    '[': '[',
    ']': ']',
    ';': ';'
}

# Regular expressions
pattern_float = re.compile(r'\d+\.\d+')
pattern_number = re.compile(r'\d+')
pattern_char = re.compile(r"'.'")
pattern_string = re.compile(r'"[^"]*"')
pattern_identifier = re.compile(r'[a-zA-Z_][a-zA-Z0-9_]*')
pattern_operator = re.compile('|'.join(re.escape(op) for op in sorted(operators.keys(), key=len, reverse=True)))

def tokenize(source_code):
    tokens = []
    lines = source_code.split('\n')
    
    for line_number, line in enumerate(lines, start=0):
        position = 0
        while position < len(line):
            # Skip whitespace
            if line[position].isspace():
                position += 1
                continue
            
            # Check for char constants
            char_match = pattern_char.match(line, position)
            if char_match:
                tokens.append((TOKEN_CHARCONST, char_match.group(0)[1:-1], line_number))
                position = char_match.end()
                continue
            
            # Check for string constants
            string_match = pattern_string.match(line, position)
            if string_match:
                tokens.append((TOKEN_STRINGCONST, string_match.group(0)[1:-1], line_number))
                position = string_match.end()
                continue
            
            # Check for float numbers
            float_match = pattern_float.match(line, position)
            if float_match:
                tokens.append((TOKEN_FLOATCONST, float_match.group(0), line_number))
                position = float_match.end()
                continue
            
            # Check for integer numbers
            number_match = pattern_number.match(line, position)
            if number_match:
                tokens.append((TOKEN_NUMBER, number_match.group(0), line_number))
                position = number_match.end()
                continue
            
            # Check for punctuators and operators
            for token, token_type in operators.items():
                if line.startswith(token, position):
                    tokens.append((token_type, token, line_number))
                    position += len(token)
                    break
            else:
                # Check for keywords and identifiers
                identifier_match = pattern_identifier.match(line, position)
                if identifier_match:
                    identifier = identifier_match.group(0)
                    if identifier in keywords:
                        tokens.append((keywords[identifier], identifier, line_number))
                    else:
                        tokens.append((TOKEN_IDENTIFIER, identifier, line_number))
                    position = identifier_match.end()
                else:
                    # If none of the patterns match, it's an unknown token
                    position += 1

    return tokens

def main():
    source_code = """



int main(){
    int A[4] = {1,2,3,4};
    int A[3] = {2,3,4}
    
    return 0;
        }
    """
    
    tokens = tokenize(source_code)
    
    with open('tokens.txt', 'w') as file:
        for token in tokens:
            token_type, token_value, line_number = token
            file.write(f"{token_type}, {token_value}, Line: {line_number}\n")
        # Add a "$" symbol at the end to serve as a termination marker
        file.write("$, $, Line: {line_number + 1}\n")

if __name__ == "__main__":
    main()
