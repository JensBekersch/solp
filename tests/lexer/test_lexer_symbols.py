# testdoc: Purpose
# To ensure the lexer correctly identifies all Solidity structural symbols
# and punctuators.

# testdoc: Method
# Each symbol is tested individually. The lexer should return a single token of
# type "SYMBOL"
# and the correct value.

# testdoc: Coverage
# Tests every character defined in `symbols.py`. No duplicates or subsets
# should be skipped.

# testdoc: Scope Limit
# This test does not validate position tracking (line/col) or Token class
# internals.
import pytest
from lexer.lexer import Lexer
from lexer.definitions.symbols import SYMBOLS


def lex(code):
    return Lexer(code).tokenize()


def get_token_type_and_value(code):
    tokens = lex(code)
    assert len(tokens) == 1, f"Expected one token for '{code}', got: {tokens}"
    return tokens[0].type, tokens[0].value


@pytest.mark.parametrize("symbol", SYMBOLS)
def test_symbol_lexing_only(symbol):
    token_type, token_value = get_token_type_and_value(symbol)
    assert token_type == "SYMBOL", f"Expected SYMBOL, got {token_type}"
    assert token_value == symbol, f"Token value mismatch: " \
                                  f"expected {symbol}, got {token_value}"
