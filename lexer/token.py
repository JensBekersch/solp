# arc42: 5. Building Block View
# Class: Token
# Represents a lexical unit in the Solidity code, with type, value and source
# location.
class Token:
    def __init__(self, type_, value, line=0, col=0, subtype=None):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
        self.subtype = subtype

    def __repr__(self):
        return (
            f"Token({self.type}, {repr(self.value)}, "
            f"line={self.line}, col={self.col}"
            + (f", subtype={self.subtype}" if self.subtype else "")
            + ")"
        )
