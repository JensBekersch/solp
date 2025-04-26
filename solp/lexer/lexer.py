# arc42: 3. System Scope and Context
# The lexer is the first stage of the parsing pipeline. It takes Solidity
# source code and converts it into a sequence of lexical tokens without any
# knowledge of syntax structure.

# arc42: 5. Building Block View
# Component: Lexer
# This module includes the main `Lexer` class which is responsible for
# scanning the input source string and identifying language elements like
# keywords, identifiers, literals, operators, and symbols.

# arc42: 5. Building Block View
# Component: Token Definitions
# This lexer uses token definitions from `definitions/keywords.py`,
# `operators.py`, and `symbols.py`, etc. These are maintained as centralized
# reference lists for testability and consistency.

# arc42: 5.2 Lexer Internal Structure
# The Lexer operates linearly over the input source code, character by
# character. Each recognized unit (identifier, keyword, number, operator, etc.)
# is converted into a Token object.

# arc42: 5.2.12 Symbols
# Symbols such as `{`, `;`, and `(` are matched directly by checking if the
# current character exists in the predefined SYMBOLS list. Each match results
# in a single SYMBOL token.

# arc42: 5.3 Token Object
# Each Token includes:
# - type (e.g. KEYWORD, IDENTIFIER, OPERATOR)
# - value (string representation)
# - position (line, column)
# - subtype (optional: e.g. operator group)

# arc42: 8. Crosscutting Concepts – Testing Strategy
# Every lexer function is individually tested using unit tests.
# For example, each keyword has a dedicated test to ensure recognition.
# Tests also document edge cases and serve as regression guards for future
# updates to Solidity.
from solp.lexer.token import Token
from solp.lexer.definitions.keywords import KEYWORDS
from solp.lexer.definitions.operators import OPERATOR_GROUPS
from solp.lexer.definitions.symbols import SYMBOLS

KEYWORDS = set(KEYWORDS)

OPERATORS = sorted(
    {op for group in OPERATOR_GROUPS.values() for op in group},
    key=len, reverse=True
)


def get_operator_group(op):
    for group, ops in OPERATOR_GROUPS.items():
        if op in ops:
            return group
    return "unknown"


class Lexer:
    def __init__(self, code):
        # arc42: 5.2.1 Initialization
        # Initializes lexer with source code string.
        # Maintains position tracking (line, column) for accurate error
        # reporting.
        self.code = code
        self.position = 0
        self.line = 1
        self.col = 1

    def tokenize(self):
        # arc42: 5.2.2 Entry Point – tokenize()
        # Main method that performs the lexical scan. Returns a list of Token
        # objects. Skips whitespace and comments. Delegates recognition to
        # helper methods.
        tokens = []
        while self.position < len(self.code):
            current = self.code[self.position]

            if current.isspace():
                self._consume_whitespace()
            elif current == "/" and self._peek() == "/":
                self._consume_line_comment()
            elif current == "/" and self._peek() == "*":
                self._consume_block_comment()
            elif current.isalpha() or current == "_":
                tokens.append(self._consume_identifier_or_keyword())
            elif current.isdigit():
                tokens.append(self._consume_number())
            elif current in SYMBOLS:
                tokens.append(Token("SYMBOL", current, self.line, self.col))
                self._advance()
            elif self._match_operator():
                op = self._consume_operator()
                group = get_operator_group(op)
                tokens.append(Token(
                    "OPERATOR", op, self.line, self.col, group
                ))
            elif current in ('"', "'"):
                tokens.append(self._consume_string())
            else:
                raise Exception(
                    f"Unexpected character '{current}' "
                    f"at line {self.line}, col {self.col}")
        return tokens

    def _advance(self, amount=1):
        # arc42: 5.2.3 Position Tracking – _advance()
        # Advances the lexer position by 'amount' characters.
        # Updates line/column state.
        for _ in range(amount):
            if self.code[self.position] == "\n":
                self.line += 1
                self.col = 1
            else:
                self.col += 1
            self.position += 1

    def _peek(self):
        # arc42: 5.2.4 Lookahead – _peek()
        # Returns the next character (without advancing). Used for comment
        # detection and operator matching.
        return self.code[self.position + 1] if self.position + 1 < len(
            self.code) else ""

    def _consume_whitespace(self):
        # arc42: 5.2.5 Whitespace Skipping
        # Advances past whitespace characters. No tokens are generated for
        # whitespace.
        while self.position < len(self.code) and self.code[self.position] \
                .isspace():
            self._advance()

    def _consume_line_comment(self):
        # arc42: 5.2.6 Line Comments
        # Skips everything until newline. Used for // comments.
        while self.position < \
                len(self.code) and self.code[self.position] != "\n":
            self._advance()

    def _consume_block_comment(self):
        # arc42: 5.2.7 Block Comments
        # Skips multiline comment enclosed in /* ... */
        self._advance(2)
        while not (self.code[self.position] == "*" and self._peek() == "/"):
            self._advance()
        self._advance(2)

    def _consume_identifier_or_keyword(self):
        # arc42: 5.2 Lexer internals
        # This method extracts either a language keyword or an identifier from
        # the source. It scans from the current position until a
        # non-alphanumeric character is found.
        start = self.position
        while self.position < len(self.code) and (
                self.code[self.position].isalnum() or
                self.code[self.position] == "_"):
            self._advance()
        value = self.code[start:self.position]
        type_ = "KEYWORD" if value in KEYWORDS else "IDENTIFIER"
        return Token(type_, value, self.line, self.col)

    def _consume_number(self):
        # arc42: 5.2.9 Numeric Literals
        # Parses integer literals (decimal only for now).
        start = self.position
        while self.position < len(self.code) and self.code[self.position] \
                .isdigit():
            self._advance()
        value = self.code[start:self.position]
        return Token("NUMBER", value, self.line, self.col)

    def _match_operator(self):
        # arc42: 5.2.10 Operator Detection
        # Checks whether any known operator starts at the current position.
        for op in OPERATORS:
            if self.code.startswith(op, self.position):
                return True
        return False

    def _consume_operator(self):
        # arc42: 5.2.11 Operator Consumption
        # Extracts the matched operator and advances the input pointer.
        for op in OPERATORS:
            if self.code.startswith(op, self.position):
                self._advance(len(op))
                return op
        return ""


    def _consume_string(self):
        # arc42: 5.2.13 String Literals
        # Handles double-quoted and single-quoted string literals.
        quote_char = self.code[self.position]
        assert quote_char in ('"', "'")
        self._advance()

        start = self.position
        value = ""
        while self.position < len(self.code) and self.code[
            self.position] != quote_char:
            if self.code[self.position] == "\\" and self._peek() == quote_char:
                value += quote_char
                self._advance(2)
            else:
                value += self.code[self.position]
                self._advance()

        if self.position >= len(self.code):
            raise Exception(
                f"Unterminated string starting at line {self.line}, "
                f"col {self.col}")

        self._advance()
        return Token("STRING", value, self.line, self.col)
