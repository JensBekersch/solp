# testdoc: Purpose
# To ensure the Token class behaves correctly as a data structure for
# lexical tokens.
# This includes construction, default values, and string representation.

# testdoc: Method
# Tokens are manually instantiated and checked for correct field assignment
# and __repr__ output.

# testdoc: Coverage
# Covers all public fields: type, value, line, col, subtype

# testdoc: Scope Limit
# This test does not depend on lexer logic or actual tokenization behavior.
from solp.lexer.token import Token


def test_token_init_minimal():
    token = Token("IDENTIFIER", "foo")
    assert token.type == "IDENTIFIER"
    assert token.value == "foo"
    assert token.line == 0
    assert token.col == 0
    assert token.subtype is None


def test_token_init_full():
    token = Token("OPERATOR", "+=", line=10, col=5, subtype="assignment")
    assert token.type == "OPERATOR"
    assert token.value == "+="
    assert token.line == 10
    assert token.col == 5
    assert token.subtype == "assignment"


def test_token_repr():
    token = Token("KEYWORD", "function", line=1, col=2)
    repr_str = repr(token)
    assert "Token(KEYWORD, 'function'" in repr_str
    assert "line=1" in repr_str
    assert "col=2" in repr_str
