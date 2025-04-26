# testdoc: Purpose
# To verify that valid Solidity identifiers (contract names, variable names,
# etc.) # are correctly recognized and returned as IDENTIFIER tokens.

# testdoc: Method
# Simple strings are passed to the lexer. Each must return a single token of
# type IDENTIFIER.

# testdoc: Coverage
# Covers legal identifier formats: camelCase, PascalCase, underscores,
# numbers (not leading).

# testdoc: Scope Limit
# This test does not check for reserved keywords or parser behavior.
import pytest
from solp.lexer.lexer import Lexer

IDENTIFIERS = [
    "x", "x1", "_x", "myVar", "CamelCase", "_under_score", "with123Numbers"
]


@pytest.mark.parametrize("identifier", IDENTIFIERS)
def test_identifier_token(identifier):
    lexer = Lexer(identifier)
    tokens = lexer.tokenize()
    assert len(tokens) == 1
    token = tokens[0]
    assert token.type == "IDENTIFIER"
    assert token.value == identifier
