# arc42: 5.3.1 Token Stream
# The TokenStream wraps a flat list of tokens and provides controlled,
# lookahead-based navigation for parser rules. It ensures safe access to
# tokens using a cursor-based API.
#
# Responsibilities:
# - Provide peekable access to the current and upcoming tokens
# - Offer utility functions for advancing and consuming tokens
# - Centralize matching and error reporting for expected patterns
# - Prevent out-of-bounds access by returning None safely

class TokenStream:
    def __init__(self, tokens):
        # arc42: 5.3.1.1 Initialization
        # The token list is stored, and the internal cursor
        # is initialized to 0.
        self.tokens = tokens
        self.index = 0

    def peek(self, offset=0):
        # arc42: 5.3.1.2 Peek
        # Returns the token at a given offset from the current index,
        # or None if the offset would go out of bounds.
        if self.index + offset < len(self.tokens):
            return self.tokens[self.index + offset]
        return None

    def current(self):
        # arc42: 5.3.1.3 Current
        # Shortcut for self.peek(0), returns the current token.
        return self.peek(0)

    def advance(self):
        # arc42: 5.3.1.4 Advance
        # Moves the cursor forward and returns the consumed token.
        tok = self.current()
        self.index += 1
        return tok

    def match(self, type_, value=None):
        # arc42: 5.3.1.5 Match
        # If the current token matches the expected type and value,
        # advances the stream and returns True. Otherwise returns False.
        tok = self.current()
        if tok and tok.type == type_ and (value is None or tok.value == value):
            self.advance()
            return True
        return False

    def expect(self, type_, value=None):
        # arc42: 5.3.1.6 Expect
        # Like match(), but raises an exception if the match fails.
        # Used to enforce expected grammar structure in rules.
        if self.match(type_, value):
            return
        raise Exception(f"Expected {type_} {value or ''} "
                        f"but got {self.current()}")

    def last(self):
        # arc42: 5.3.1.7 Last
        # Returns the last consumed token, or None if no tokens have
        # been consumed yet.
        return self.tokens[self.index - 1] if self.index > 0 else None
