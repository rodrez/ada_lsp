# Stores symbols (functions, variables) for quick lookup
# A basic symbol table to store and retrieve relevant symbols.
# This module maintains a dictionary of identifiers (e.g., functions, variables)
# and can provide autocomplete suggestions based on a prefix (e.g., proce → procedure).
from typing import List, Dict, Optional

from ada.parser.lexer import Token

class Symbol:
    def __init__(self, name: str, type: str, scope: str):
        self.name = name
        self.type = type  # e.g., 'function', 'variable', 'procedure'
        self.scope = scope

    def __repr__(self):
        return f"Symbol(name='{self.name}', type='{self.type}', scope='{self.scope}')"

class SymbolTable:
    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}

    def add_symbol(self, name: str, type: str, scope: str):
        self.symbols[name] = Symbol(name, type, scope)

    def get_symbol(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def remove_symbol(self, name: str):
        if name in self.symbols:
            del self.symbols[name]

    def get_suggestions(self, prefix: str) -> List[Symbol]:
        return [symbol for name, symbol in self.symbols.items() if name.startswith(prefix)]

    def get_symbols_in_scope(self, tokens: List[Token]) -> List[Symbol]:
        # Implement logic to determine the current scope based on tokens
        # For simplicity, let's assume it returns all symbols for now
        return list(self.symbols.values())

# Example usage
if __name__ == "__main__":
    symbol_table = SymbolTable()

    # Add some symbols
    symbol_table.add_symbol("print_hello", "procedure", "global")
    symbol_table.add_symbol("calculate_sum", "function", "global")
    symbol_table.add_symbol("user_input", "variable", "main")
    symbol_table.add_symbol("process_data", "procedure", "global")

    # Look up a symbol
    print(symbol_table.get_symbol("calculate_sum"))

    # Get suggestions based on a prefix
    suggestions = symbol_table.get_suggestions("p")
    print("Suggestions starting with 'p':")
    for suggestion in suggestions:
        print(suggestion)

    # Remove a symbol
    symbol_table.remove_symbol("user_input")

    # Verify removal
    print(symbol_table.get_symbol("user_input"))  # Should print None
