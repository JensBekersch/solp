# testdoc: Purpose
# To verify that integer literals are correctly recognized as NUMBER tokens.

# testdoc: Method
# Various numeric strings (decimal only) are passed to the lexer.

# testdoc: Coverage
# Covers positive integers in decimal form (hex, exp-form to be added later).

# testdoc: Scope Limit
# Does not test signed numbers, floats, hex, or scientific notation.
import pytest
from solp.lexer.lexer import Lexer

NUMBERS = ["0", "1", "42", "999", "1234567890"]


@pytest.mark.parametrize("number", NUMBERS)
def test_number_token(number):
    lexer = Lexer(number)
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    token = tokens[0]
    assert token.type == "NUMBER"
    assert token.value == number
