# lexer/token_types.py

# Token types
KEYWORD = "KEYWORD"
IDENTIFIER = "IDENTIFIER"
SYMBOL = "SYMBOL"
OPERATOR = "OPERATOR"
NUMBER = "NUMBER"
STRING = "STRING"

# Keywords
KW_CONTRACT = "contract"
KW_FUNCTION = "function"
KW_RETURN = "return"
KW_TYPES = {"uint", "string", "address", "bool"}
KW_VISIBILITY = {"public", "private", "internal", "external"}
KW_PAYABLE = "payable"
KW_RETURNS = "returns"
KW_CONSTRUCTOR = "constructor"

# Rule names (for dispatcher)
RULE_FUNCTION = "function"
RULE_VARIABLE = "variable"
RULE_STATEMENTS = "statements"
RULE_ASSIGNMENT = "assignment"
RULE_EXPRESSION = "expression"
RULE_REQUIRE = "require"
RULE_IF = "if"
RULE_ELSE = "else"
RULE_REVERT = "revert"
RULE_ASSERT = "assert"
RULE_EMIT = "emit"
RULE_CONSTRUCTOR = "constructor"
RULE_WHILE = "while"
RULE_FOR = "for"
RULE_BREAK = "break"
RULE_CONTINUE = "continue"

# Common symbols
SYM_LBRACE = "{"
SYM_RBRACE = "}"
SYM_LPAREN = "("
SYM_RPAREN = ")"
SYM_SEMICOLON = ";"
SYM_DOT = "."
SYM_COMMA = ","
SYM_EMPTY = ""
