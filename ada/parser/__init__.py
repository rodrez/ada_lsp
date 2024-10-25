# Analyzes tokens and provides structured data for completion
# Analyzes the tokens provided by lexer.py.
# It doesn’t need to parse the entire Ada syntax initially. Instead, it can focus on extracting function and variable names, which are necessary for autocomplete.
from ada.parser.lexer import Lexer 


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer

