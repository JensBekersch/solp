# testdoc: Purpose
# To ensure the lexer correctly identifies and extracts string literals,
# enclosed in single or double quotes.

# testdoc: Method
# Various quoted string inputs are lexed and compared to expected values.
# Escape sequences are treated as literal characters for now.

# testdoc: Coverage
# Single-quoted and double-quoted strings, escaped quote inside string.

# testdoc: Scope Limit
# Does not validate full escape sequence rules (e.g. \n, \xFF)
import pytest
from lexer.lexer import Lexer

CASES = [
    ('"hello"', "hello"),
    ("'world'", "world"),
    ('"He said \\"Hi\\""', 'He said "Hi"'),
    ("'It\\'s ok'", "It's ok"),
]


@pytest.mark.parametrize("code,expected", CASES)
def test_string_token(code, expected):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    token = tokens[0]
    assert token.type == "STRING"
    assert token.value == expected
