# testdoc: Purpose
# To test each method of ContractRule in isolation. This supports modular,
# high-confidence development of parser rules and allows fine-grained
# diagnostics on failure.

# testdoc: Scope
# Each test focuses on one method from ContractRule (header parsing,
# member loop, etc.). Token stream and dispatcher are mocked or simplified
# as needed.

from solp.parser.rules.contract import ContractRule
from solp.solidity_ast.nodes import ContractNode


# --- Mocks ---


class MockToken:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


class MockTokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def current(self):
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def expect(self, type_, value=None):
        tok = self.current()
        assert tok and tok.type == type_
        if value:
            assert tok.value == value
        self.advance()

    def match(self, type_, value=None):
        tok = self.current()
        if tok and tok.type == type_ and (value is None or tok.value == value):
            self.advance()
            return True
        return False

    def advance(self):
        self.index += 1

    def last(self):
        if self.index == 0:
            return None
        return self.tokens[self.index - 1]


class MockDispatcher:
    def __init__(self, tokens, mapping):
        self.tokens = tokens
        self.mapping = mapping
        self.calls = []

    def parse_rule(self, name):
        self.calls.append(name)
        self.tokens.advance()  # Simulate token consumption
        return self.mapping[name]


# --- Tests ---


def test_parse_contract_header():
    # testdoc: Verifies contract header parsing
    tokens = [
        MockToken("KEYWORD", "contract"),
        MockToken("IDENTIFIER", "MyContract"),
        MockToken("SYMBOL", "{"),
    ]
    stream = MockTokenStream(tokens)
    rule = ContractRule(stream, dispatcher=None)
    name = rule.parse_contract_header()
    assert name == "MyContract"


def test_parse_member_returns_function():
    # testdoc: Verifies function member is correctly delegated to dispatcher
    tokens = [MockToken("KEYWORD", "function")]
    stream = MockTokenStream(tokens)
    dispatcher = MockDispatcher(stream, {"function": "<FunctionNode>"})
    rule = ContractRule(stream, dispatcher)
    assert rule.parse_member() == "<FunctionNode>"
    assert dispatcher.calls == ["function"]


def test_parse_member_returns_variable():
    # testdoc: Verifies variable declaration is delegated to dispatcher
    tokens = [MockToken("KEYWORD", "uint")]
    stream = MockTokenStream(tokens)
    dispatcher = MockDispatcher(stream, {"variable": "<VariableNode>"})
    rule = ContractRule(stream, dispatcher)
    assert rule.parse_member() == "<VariableNode>"
    assert dispatcher.calls == ["variable"]


def test_next_member_or_skip_returns_member():
    # testdoc: If member is valid, it is returned unchanged
    tokens = [MockToken("KEYWORD", "function")]
    stream = MockTokenStream(tokens)
    dispatcher = MockDispatcher(stream, {"function": "<Function>"})
    rule = ContractRule(stream, dispatcher)
    result = rule.next_member_or_skip()
    assert result == "<Function>"


def test_next_member_or_skip_advances_on_none():
    # testdoc: If member parsing fails, token stream is advanced and None is returned
    tokens = [MockToken("KEYWORD", "unknown")]
    stream = MockTokenStream(tokens)
    dispatcher = MockDispatcher(stream, {})
    rule = ContractRule(stream, dispatcher)
    result = rule.next_member_or_skip()
    assert result is None
    assert stream.index == 1


def test_parse_members_collects_members():
    # testdoc: Should collect multiple members until closing brace
    tokens = [
        MockToken("KEYWORD", "function"),
        MockToken("KEYWORD", "function"),
        MockToken("SYMBOL", "}"),
    ]
    stream = MockTokenStream(tokens)
    dispatcher = MockDispatcher(stream, {"function": "X"})
    rule = ContractRule(stream, dispatcher)
    result = rule.parse_members()
    assert result == ["X", "X"]


def test_parse_full_contract():
    # testdoc: Integration of header + body parsing into ContractNode
    tokens = [
        MockToken("KEYWORD", "contract"),
        MockToken("IDENTIFIER", "Test"),
        MockToken("SYMBOL", "{"),
        MockToken("KEYWORD", "function"),
        MockToken("SYMBOL", "}"),
    ]
    stream = MockTokenStream(tokens)
    dispatcher = MockDispatcher(stream, {"function": "Fn"})
    rule = ContractRule(stream, dispatcher)
    contract = rule.parse()
    assert isinstance(contract, ContractNode)
    assert contract.name == "Test"
    assert contract.members == ["Fn"]
