# testdoc: Purpose
# To ensure each Solidity keyword is correctly recognized by the lexer
# and assigned the type 'KEYWORD'.

# testdoc: Method
# A parameterized test case automatically checks each keyword defined
# in `keywords.py`. For each input, the lexer should return a single token
# with the correct type and value.

# testdoc: Coverage
# Full coverage of all Solidity language keywords currently known.
# This test will fail if any are added or changed without adjusting the test
# list.

# testdoc: Edge Cases
# Detects typographical errors or accidental keyword renaming in the keyword
# list.
import pytest
from lexer.lexer import Lexer
from lexer.definitions.keywords import KEYWORDS

CONTRACT = "contract"
INTERFACE = "interface"
LIBRARY = "library"
FUNCTION = "function"
MODIFIER = "modifier"
CONSTRUCTOR = "constructor"
IF = "if"
ELSE = "else"
WHILE = "while"
FOR = "for"
DO = "do"
RETURN = "return"
EMIT = "emit"
REQUIRE = "require"
REVERT = "revert"
PUBLIC = "public"
PRIVATE = "private"
INTERNAL = "internal"
EXTERNAL = "external"
VIEW = "view"
PURE = "pure"
PAYABLE = "payable"
CONSTANT = "constant"
STORAGE = "storage"
MEMORY = "memory"
CALLDATA = "calldata"
MAPPING = "mapping"
EVENT = "event"
ENUM = "enum"
STRUCT = "struct"
IMPORT = "import"
PRAGMA = "pragma"
RETURNS = "returns"
OVERRIDE = "override"
VIRTUAL = "virtual"
ASSEMBLY = "assembly"
NEW = "new"
DELETE = "delete"
BREAK = "break"
CONTINUE = "continue"
UNCHECKED = "unchecked"
TRY = "try"
CATCH = "catch"
THROW = "throw"
ADDRESS = "address"
BOOL = "bool"
STRING = "string"
BYTES = "bytes"
INT = "int"
UINT = "uint"
FIXED = "fixed"
UFIXED = "ufixed"
BYTE = "byte"
TRUE = "true"
FALSE = "false"
THIS = "this"
SUPER = "super"
MSG = "msg"
TX = "tx"
BLOCK = "block"

ALL_KEYWORDS = [CONTRACT, INTERFACE, LIBRARY, FUNCTION, MODIFIER, CONSTRUCTOR,
                IF, ELSE, WHILE, FOR, DO, RETURN, EMIT, REQUIRE, REVERT,
                PUBLIC, PRIVATE, INTERNAL, EXTERNAL, VIEW, PURE, PAYABLE,
                CONSTANT, STORAGE, MEMORY, CALLDATA, MAPPING, EVENT, ENUM,
                STRUCT, IMPORT, PRAGMA, RETURNS, OVERRIDE, VIRTUAL, ASSEMBLY,
                NEW, DELETE, BREAK, CONTINUE, UNCHECKED, TRY, CATCH, THROW,
                ADDRESS, BOOL, STRING, BYTES, INT, UINT, FIXED, UFIXED, BYTE,
                TRUE, FALSE, THIS, SUPER, MSG, TX, BLOCK]


def lex(code):
    return Lexer(code).tokenize()


def get_single_token_value(code):
    tokens = lex(code)
    assert len(tokens) == 1, f"Expected one token, got {tokens}"
    return tokens[0]


def test_keyword_count():
    assert len(ALL_KEYWORDS) == len(KEYWORDS)


@pytest.mark.parametrize("keyword", ALL_KEYWORDS)
def test_keyword_token_recognition(keyword):
    token = get_single_token_value(keyword)

    assert token.type == "KEYWORD", \
        f"{keyword} should be recognized as KEYWORD"
    assert token.value == keyword
