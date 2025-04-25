# arc42: 5.3.7 Function Rule
# This rule parses Solidity function declarations.
# Responsibilities:
# - Parse the function header (keyword and name)
# - Parse the parameter list
# - Parse optional function modifiers (visibility, payable)
# - Parse optional return types (via 'returns')
# - Parse the function body using the delegated 'statements' rule
# Output: A fully constructed FunctionNode in the AST
from solidity_ast.nodes import FunctionNode, VariableNode
from lexer.token_types import (
    KEYWORD, IDENTIFIER, SYMBOL,
    KW_FUNCTION, KW_VISIBILITY, KW_PAYABLE, KW_RETURNS, RULE_STATEMENTS,
    SYM_LPAREN, SYM_RPAREN, SYM_LBRACE, SYM_RBRACE, SYM_COMMA, SYM_EMPTY,
)


class FunctionRule:
    def __init__(self, tokens, dispatcher):
        # arc42: 5.3.7.1 Initialization
        # Inputs:
        # - tokens: a token stream used for lookahead and matching
        # - dispatcher: used to invoke subrules (e.g. statements)
        self.tokens = tokens
        self.dispatcher = dispatcher

    def parse(self):
        # arc42: 5.3.7.2 Entry Point
        # Combines all subparsers to build a complete FunctionNode
        name = self._parse_function_header()
        parameters = self.parse_parameters()
        visibility, is_payable = self.parse_modifiers()
        returns = self.parse_returns()

        self.tokens.expect(SYMBOL, SYM_LBRACE)
        body = self.dispatcher.parse_rule(RULE_STATEMENTS)
        self.tokens.expect(SYMBOL, SYM_RBRACE)

        return FunctionNode(
            name=name,
            parameters=parameters,
            visibility=visibility,
            is_payable=is_payable,
            returns=returns,
            body=body
        )

    def _parse_function_header(self):
        # arc42: 5.3.7.2.1 Function Header
        # Matches 'function' keyword and extracts function name (identifier)
        self.tokens.expect(KEYWORD, KW_FUNCTION)
        self.tokens.expect(IDENTIFIER)
        return self.tokens.last().value

    def parse_parameters(self):
        # arc42: 5.3.7.3 Parameters
        # Parses parameter list enclosed in parentheses
        # Example: (uint amount, address recipient)
        parameters = []
        self.tokens.expect(SYMBOL, SYM_LPAREN)
        while not self.tokens.match(SYMBOL, SYM_RPAREN):
            if parameters:
                self.tokens.expect(SYMBOL, SYM_COMMA)
            type_ = self.tokens.current().value
            self.tokens.expect(KEYWORD)
            name = self.tokens.current().value
            self.tokens.expect(IDENTIFIER)
            parameters.append(VariableNode(type_, name))
        return parameters

    def parse_modifiers(self):
        # arc42: 5.3.7.4 Visibility / Modifiers
        # Parses optional visibility modifiers
        # (public/private/internal/external)
        # and 'payable' flag
        visibility = None
        is_payable = False
        while True:
            tok = self.tokens.current()
            if tok is None or tok.type != KEYWORD:
                break
            if tok.value in KW_VISIBILITY:
                visibility = tok.value
                self.tokens.advance()
            elif tok.value == KW_PAYABLE:
                is_payable = True
                self.tokens.advance()
            else:
                break
        return visibility, is_payable

    def parse_returns(self):
        # arc42: 5.3.7.5 Return Types
        # Parses optional return types defined using 'returns (...)'
        # Currently supports unnamed return types only
        # (e.g., returns (bool, uint))
        if not self.tokens.match(KEYWORD, KW_RETURNS):
            return []
        self.tokens.expect(SYMBOL, SYM_LPAREN)
        returns = []
        while not self.tokens.match(SYMBOL, SYM_RPAREN):
            if returns:
                self.tokens.expect(SYMBOL, SYM_COMMA)
            type_ = self.tokens.current().value
            self.tokens.expect(KEYWORD)
            returns.append(VariableNode(type_, SYM_EMPTY))
        return returns
