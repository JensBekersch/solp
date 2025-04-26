# arc42: 5.3.8 Variable Rule
# This rule parses top-level state variable declarations in Solidity contracts.
# A variable can include:
# - a type (e.g., uint, address)
# - an optional visibility modifier (public/private/internal/external)
# - a name (identifier)
# - a semicolon to terminate the declaration
from solp.solidity_ast.nodes import VariableNode
from solp.lexer.token_types import (
    KEYWORD, IDENTIFIER, SYMBOL,
    KW_VISIBILITY, SYM_SEMICOLON,
)


class VariableRule:
    def __init__(self, tokens):
        # arc42: 5.3.8.1 Initialization
        # This rule does not need a dispatcher; parsing is self-contained.
        self.tokens = tokens

    def parse(self):
        # arc42: 5.3.8.2 Entry Point
        # Parses a variable declaration like: `uint balance;`
        var_type = self.tokens.current().value
        self.tokens.expect(KEYWORD)

        visibility = None
        if self.tokens.current().type == KEYWORD and \
                self.tokens.current().value in KW_VISIBILITY:
            visibility = self.tokens.current().value
            self.tokens.advance()

        name = self.tokens.current().value
        self.tokens.expect(IDENTIFIER)
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)

        return VariableNode(var_type=var_type, name=name,
                            visibility=visibility)
