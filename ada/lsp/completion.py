# Core logic for autocomplete (parsing and suggestion generation)

# This is where the autocomplete logic resides.
# It will receive the partial text or cursor position from the client and query the ada_parser module to get relevant completion suggestions.
# The completions are then packaged into JSON format and sent back through the JSON-RPC layer.

from ada.parser.symbol_table import SymbolTable
from ada.parser.lexer import Lexer
from typing import List, Dict

class CompletionEngine:
    def __init__(self):
        self.symbol_table = SymbolTable()
        # Remove the Lexer initialization from here
        # self.lexer = Lexer()

    def complete(self, partial_text: str, context: str = "") -> List[Dict[str, str]]:
        # Create a new Lexer instance with the context as the source
        lexer = Lexer(context)
        
        # Use the lexer to tokenize the context
        tokens = lexer.tokenize()
        
        # Use the symbol table to get relevant completions based on context
        relevant_symbols = self.symbol_table.get_symbols_in_scope(tokens)
        
        # Filter and format completions
        completions = [
            {"label": symbol.name, "kind": symbol.kind, "detail": symbol.detail}
            for symbol in relevant_symbols
            if symbol.name.startswith(partial_text)
        ]
        
        return completions

# Example usage
if __name__ == "__main__":
    engine = CompletionEngine()
    
    # Simulate a completion request
    partial_text = "proc"
    context = "package Body_Name is\n    "
    
    completions = engine.complete(partial_text, context)
    for completion in completions:
        print(f"{completion['label']} ({completion['kind']}): {completion['detail']}")
