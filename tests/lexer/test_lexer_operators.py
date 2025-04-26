# testdoc: Purpose
# To ensure the lexer identifies all Solidity operators correctly and returns
# one token per operator input with the correct type and value. We do not test
# the internals of the Token class here.

# testdoc: Method
# Each operator string is passed alone into the Lexer.
# We verify that the lexer returns a single token with the type "OPERATOR"
# and the expected value. No assumptions are made about internal Token
# structure.

# testdoc: Coverage
# Covers all operators listed in OPERATOR_GROUPS.

# testdoc: Scope Limit
# This test intentionally avoids testing the Token class itself
# (subtype, line, col). Those aspects are to be tested separately.
import pytest
from solp.lexer.lexer import Lexer
from solp.lexer.definitions.operators import OPERATOR_GROUPS

ALL_OPERATORS = [
    (op, group)
    for group, ops in OPERATOR_GROUPS.items()
    for op in ops
]


def lex(code):
    return Lexer(code).tokenize()


def get_token_type_and_value(code):
    tokens = lex(code)
    assert len(
        tokens) == 1, f"Expected one token for input '{code}', got: {tokens}"
    return tokens[0].type, tokens[0].value


@pytest.mark.parametrize("operator,group", ALL_OPERATORS)
def test_operator_lexing_only(operator, group):
    token_type, token_value = get_token_type_and_value(operator)
    assert token_type == "OPERATOR", f"Expected OPERATOR, got {token_type}"
    assert token_value == operator, f"Token value mismatch: " \
                                    f"expected {operator}" \
                                    f", got {token_value}"
