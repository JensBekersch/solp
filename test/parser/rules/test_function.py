# testdoc: Purpose
# These tests verify the correctness of each parsing component in FunctionRule.
# Each method is tested in isolation using a mock token stream and optional dispatcher.

# testdoc: Scope
# Covers:
# - Function header parsing
# - Parameter list parsing
# - Modifier (visibility/payable) parsing
# - Return type parsing
# - Full parse integration

from parser.rules.function import FunctionRule
from solidity_ast.nodes import FunctionNode
from lexer.token_types import (
    KEYWORD, IDENTIFIER, SYMBOL,
    KW_FUNCTION, KW_PAYABLE, KW_RETURNS,
    SYM_LPAREN, SYM_RPAREN, SYM_LBRACE, SYM_RBRACE, SYM_COMMA,
)


class MockToken:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class MockTokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current(self):
        return self.tokens[self.index] if self.index < len(
            self.tokens) else None

    def last(self):
        return self.tokens[self.index - 1]

    def expect(self, type_, value=None):
        tok = self.current()
        assert tok.type == type_
        if value:
            assert tok.value == value
        self.advance()

    def match(self, type_, value=None):
        tok = self.current()
        if tok and tok.type == type_ and (value is None or tok.value == value):
            self.advance()
            return True
        return False

    def advance(self):
        self.index += 1


class MockDispatcher:
    def __init__(self, rule_output):
        self.rule_output = rule_output
        self.calls = []

    def parse_rule(self, rule_name):
        self.calls.append(rule_name)
        return self.rule_output.get(rule_name, [])


def test_parse_function_header():
    # testdoc: Should extract function name correctly after 'function' keyword
    tokens = [
        MockToken(KEYWORD, KW_FUNCTION),
        MockToken(IDENTIFIER, "doSomething"),
    ]
    rule = FunctionRule(MockTokenStream(tokens), dispatcher=None)
    name = rule._parse_function_header()
    assert name == "doSomething"


def test_parse_parameters():
    # testdoc: Should extract parameter list into VariableNode objects
    tokens = [
        MockToken(SYMBOL, SYM_LPAREN),
        MockToken(KEYWORD, "uint"),
        MockToken(IDENTIFIER, "amount"),
        MockToken(SYMBOL, SYM_COMMA),
        MockToken(KEYWORD, "address"),
        MockToken(IDENTIFIER, "to"),
        MockToken(SYMBOL, SYM_RPAREN),
    ]
    rule = FunctionRule(MockTokenStream(tokens), dispatcher=None)
    params = rule.parse_parameters()
    assert len(params) == 2
    assert params[0].var_type == "uint"
    assert params[0].name == "amount"
    assert params[1].var_type == "address"
    assert params[1].name == "to"


def test_parse_modifiers():
    # testdoc: Should detect visibility and payable modifiers correctly
    tokens = [
        MockToken(KEYWORD, "public"),
        MockToken(KEYWORD, KW_PAYABLE),
    ]
    rule = FunctionRule(MockTokenStream(tokens), dispatcher=None)
    visibility, is_payable = rule.parse_modifiers()
    assert visibility == "public"
    assert is_payable is True


def test_parse_returns():
    # testdoc: Should parse unnamed return types inside 'returns(...)'
    tokens = [
        MockToken(KEYWORD, KW_RETURNS),
        MockToken(SYMBOL, SYM_LPAREN),
        MockToken(KEYWORD, "bool"),
        MockToken(SYMBOL, SYM_COMMA),
        MockToken(KEYWORD, "uint"),
        MockToken(SYMBOL, SYM_RPAREN),
    ]
    rule = FunctionRule(MockTokenStream(tokens), dispatcher=None)
    returns = rule.parse_returns()
    assert len(returns) == 2
    assert returns[0].var_type == "bool"
    assert returns[0].name == ""
    assert returns[1].var_type == "uint"


def test_full_function_parse():
    # testdoc: Should integrate header, parameters, modifiers,
    # returns, and body
    tokens = [
        MockToken(KEYWORD, KW_FUNCTION),
        MockToken(IDENTIFIER, "transfer"),
        MockToken(SYMBOL, SYM_LPAREN),
        MockToken(KEYWORD, "uint"),
        MockToken(IDENTIFIER, "amount"),
        MockToken(SYMBOL, SYM_RPAREN),
        MockToken(KEYWORD, "public"),
        MockToken(KEYWORD, KW_RETURNS),
        MockToken(SYMBOL, SYM_LPAREN),
        MockToken(KEYWORD, "bool"),
        MockToken(SYMBOL, SYM_RPAREN),
        MockToken(SYMBOL, SYM_LBRACE),
        MockToken(SYMBOL, SYM_RBRACE),
    ]
    dispatcher = MockDispatcher(rule_output={"statements": ["stmt1", "stmt2"]})
    rule = FunctionRule(MockTokenStream(tokens), dispatcher)
    fn = rule.parse()

    assert isinstance(fn, FunctionNode)
    assert fn.name == "transfer"
    assert fn.parameters[0].var_type == "uint"
    assert fn.returns[0].var_type == "bool"
    assert fn.visibility == "public"
    assert fn.body == ["stmt1", "stmt2"]
