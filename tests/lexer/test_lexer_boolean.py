# testdoc: Purpose
# Booleans in Solidity are reserved keywords: `true` and `false`.

# testdoc: Method
# Check if these values are recognized as KEYWORD tokens with correct value.

import pytest

from solp.lexer.lexer import Lexer


@pytest.mark.parametrize("value", ["true", "false"])
def test_boolean_keywords(value):
    tokens = Lexer(value).tokenize()
    assert len(tokens) == 1
    token = tokens[0]
    assert token.type == "KEYWORD"
    assert token.value == value
