# arc42: 5.3.10 Constructor Rule
# Handles parsing of Solidity constructors.
# Constructors:
# - use the keyword `constructor`
# - may include parameters and visibility
# - have no name or return type
# - contain a standard statement block
# Results in a ConstructorNode for use in ContractNode.members
from solp.solidity_ast.nodes import ConstructorNode, VariableNode
from solp.lexer.token_types import (
    KEYWORD, IDENTIFIER, SYMBOL,
    KW_VISIBILITY, SYM_LPAREN, SYM_RPAREN, SYM_LBRACE, SYM_RBRACE, SYM_COMMA,
    RULE_STATEMENTS, RULE_CONSTRUCTOR,
)


class ConstructorRule:
    def __init__(self, tokens, dispatcher):
        self.tokens = tokens
        self.dispatcher = dispatcher

    def parse(self):
        self.tokens.expect(KEYWORD, RULE_CONSTRUCTOR)
        parameters = self._parse_parameters()
        visibility = self._parse_visibility()

        self.tokens.expect(SYMBOL, SYM_LBRACE)
        body = self.dispatcher.parse_rule(RULE_STATEMENTS)
        self.tokens.expect(SYMBOL, SYM_RBRACE)

        return ConstructorNode(parameters, visibility, body)

    def _parse_parameters(self):
        params = []
        self.tokens.expect(SYMBOL, SYM_LPAREN)
        while not self.tokens.match(SYMBOL, SYM_RPAREN):
            if params:
                self.tokens.expect(SYMBOL, SYM_COMMA)
            typ = self.tokens.current().value
            self.tokens.expect(KEYWORD)
            name = self.tokens.current().value
            self.tokens.expect(IDENTIFIER)
            params.append(VariableNode(typ, name))
        return params

    def _parse_visibility(self):
        tok = self.tokens.current()
        if tok.type == KEYWORD and tok.value in KW_VISIBILITY:
            self.tokens.advance()
            return tok.value
        return None
