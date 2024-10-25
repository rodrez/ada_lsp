# Tokenizes Ada source code
# This module tokenizes Ada code.
# The lexer will read Ada source code and break it down into tokens like identifiers, keywords, symbols, and literals.
# This makes it easier for the parser to work with structured data.

from enum import Enum, auto

class TokenType(Enum):
    IDENTIFIER = auto()
    KEYWORD = auto()
    SYMBOL = auto()
    LITERAL = auto()
    WHITESPACE = auto()

class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, '{self.value}')"

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.position = 0

    KEYWORDS = {'procedure', 'function', 'begin', 'end', 'if', 'then', 'else', 'while', 'for', 'loop', 'return'}
    SYMBOLS = {':=', ';', '(', ')', ',', '+', '-', '*', '/', '=', '<', '>', '<=', '>=', '/='}

    def tokenize(self):
        while self.position < len(self.source):
            if self.source[self.position].isspace():
                self.tokenize_whitespace()
            elif self.source[self.position].isalpha():
                self.tokenize_identifier_or_keyword()
            elif self.source[self.position].isdigit():
                self.tokenize_literal()
            else:
                self.tokenize_symbol()
        return self.tokens

    def tokenize_whitespace(self):
        start = self.position
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1
        self.tokens.append(Token(TokenType.WHITESPACE, self.source[start:self.position]))

    def tokenize_identifier_or_keyword(self):
        start = self.position
        while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
            self.position += 1
        value = self.source[start:self.position]
        if value in self.KEYWORDS:
            self.tokens.append(Token(TokenType.KEYWORD, value))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value))

    def tokenize_literal(self):
        start = self.position
        while self.position < len(self.source) and self.source[self.position].isdigit():
            self.position += 1
        self.tokens.append(Token(TokenType.LITERAL, self.source[start:self.position]))

    def tokenize_symbol(self):
        for symbol in sorted(self.SYMBOLS, key=len, reverse=True):
            if self.source.startswith(symbol, self.position):
                self.tokens.append(Token(TokenType.SYMBOL, symbol))
                self.position += len(symbol)
                return
        # If no known symbol is found, treat it as a single-character symbol
        self.tokens.append(Token(TokenType.SYMBOL, self.source[self.position]))
        self.position += 1

# Example usage
if __name__ == "__main__":
    ada_code = "procedure Hello is begin Put_Line(\"Hello, World!\"); end Hello;"
    lexer = Lexer(ada_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(token)
