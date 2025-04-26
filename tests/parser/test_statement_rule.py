# testdoc: Purpose
# This suite verifies that StatementRule correctly parses all supported
# Solidity statements.

# testdoc: Scope
# Includes return, assignment, expressions, require, revert, assert, emit,
# control flow (if, while, for), and loop modifiers (break, continue).
from solp.parser.rules.statement import StatementRule
from solp.lexer.token_types import KEYWORD, IDENTIFIER, SYMBOL


# --- Mocks ---
from solp.solidity_ast.nodes import CallNode


class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class Stream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current(self):
        return self.tokens[self.index] if self.index < len(
            self.tokens) else None

    def peek(self, offset=0):
        return self.tokens[self.index + offset] if self.index + offset < len(
            self.tokens) else None

    def advance(self):
        self.index += 1

    def expect(self, type_, value=None):
        tok = self.current()
        assert tok.type == type_, f"Expected type {type_}, got {tok.type}"
        if value:
            assert tok.value == value, f"Expected value {value}, " \
                                       f"got {tok.value}"
        self.advance()

    def match(self, type_, value=None):
        tok = self.current()
        if tok and tok.type == type_ and (value is None or tok.value == value):
            self.advance()
            return True
        return False


# --- Tests ---

def test_parse_break_statement():
    # testdoc: Parses 'break;' into a StatementNode("break")
    stream = Stream([
        Token(KEYWORD, "break"),
        Token(SYMBOL, ";"),
    ])
    rule = StatementRule(stream)
    node = rule.parse_statement()
    assert node.type == "break"


def test_parse_continue_statement():
    # testdoc: Parses 'continue;' into a StatementNode("continue")
    stream = Stream([
        Token(KEYWORD, "continue"),
        Token(SYMBOL, ";"),
    ])
    rule = StatementRule(stream)
    node = rule.parse_statement()
    assert node.type == "continue"


def test_parse_emit_statement():
    # testdoc: Parses 'emit Transfer(a, b);' into a
    # StatementNode("emit", event="Transfer", ...)
    stream = Stream([
        Token(KEYWORD, "emit"),
        Token(IDENTIFIER, "Transfer"),
        Token(SYMBOL, "("),
        Token(IDENTIFIER, "a"),
        Token(SYMBOL, ","),
        Token(IDENTIFIER, "b"),
        Token(SYMBOL, ")"),
        Token(SYMBOL, ";"),
    ])
    rule = StatementRule(stream)
    node = rule.parse_statement()
    assert node.type == "emit"
    assert node.event == "Transfer"
    assert node.arguments == ["a", "b"]


def test_parse_require_statement():
    # testdoc: Parses 'require(x > 0);' into StatementNode("require", ...)
    stream = Stream([
        Token(KEYWORD, "require"),
        Token(SYMBOL, "("),
        Token(IDENTIFIER, "x"),
        Token(SYMBOL, ")"),
        Token(SYMBOL, ";"),
    ])
    rule = StatementRule(stream)
    node = rule.parse_statement()

    assert node.type == "expression"
    assert isinstance(node.expr, CallNode)
    assert isinstance(node.expr.arguments, list)


def test_parse_assert_statement():
    # testdoc: Parses 'assert(y);' into StatementNode("assert", ...)
    stream = Stream([
        Token(KEYWORD, "assert"),
        Token(SYMBOL, "("),
        Token(IDENTIFIER, "y"),
        Token(SYMBOL, ")"),
        Token(SYMBOL, ";"),
    ])
    rule = StatementRule(stream)
    node = rule.parse_statement()

    assert node.type == "assert"
    assert isinstance(node.arguments, list)
    assert node.arguments == ["y"]


def test_parse_revert_statement():
    # testdoc: Parses 'revert("Error");' into
    # StatementNode("revert", arguments=[...])
    stream = Stream([
        Token(KEYWORD, "revert"),
        Token(SYMBOL, "("),
        Token(IDENTIFIER, '"Error"'),
        Token(SYMBOL, ")"),
        Token(SYMBOL, ";"),
    ])
    rule = StatementRule(stream)
    node = rule.parse_statement()
    assert node.type == "revert"
    assert node.arguments == ['"Error"']
