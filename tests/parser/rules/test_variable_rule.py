# testdoc: Purpose
# To verify that top-level variable declarations are parsed correctly
# by VariableRule.

# testdoc: Scope
# This includes type, optional visibility, and name extraction.
from solp.parser.rules.variable import VariableRule
from solp.solidity_ast.nodes import VariableNode
from solp.lexer.token_types import KEYWORD, IDENTIFIER, SYMBOL, SYM_SEMICOLON


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

    def expect(self, type_, value=None):
        tok = self.current()
        assert tok.type == type_
        if value:
            assert tok.value == value
        self.advance()

    def advance(self):
        self.index += 1


def test_parse_variable_no_visibility():
    # testdoc: Should parse a variable without visibility modifier
    tokens = [
        MockToken(KEYWORD, "uint"),
        MockToken(IDENTIFIER, "balance"),
        MockToken(SYMBOL, SYM_SEMICOLON),
    ]
    rule = VariableRule(MockTokenStream(tokens))
    node = rule.parse()
    assert isinstance(node, VariableNode)
    assert node.var_type == "uint"
    assert node.name == "balance"
    assert node.visibility is None


def test_parse_variable_with_visibility():
    # testdoc: Should parse a variable with visibility modifier
    tokens = [
        MockToken(KEYWORD, "address"),
        MockToken(KEYWORD, "public"),
        MockToken(IDENTIFIER, "owner"),
        MockToken(SYMBOL, SYM_SEMICOLON),
    ]
    rule = VariableRule(MockTokenStream(tokens))
    node = rule.parse()
    assert node.var_type == "address"
    assert node.name == "owner"
    assert node.visibility == "public"
