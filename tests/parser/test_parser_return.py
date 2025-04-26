# testdoc: Purpose
# To test parsing of return statements with and without values.

# testdoc: Method
# Validates that return statements inside a function body are parsed into
# ReturnNode, with or without a value (e.g. `return;` vs. `return x;`).
from solp.lexer.lexer import Lexer
from solp.parser.parser import Parser
from solp.solidity_ast.nodes import ReturnNode


def test_return_with_value():
    code = """
    contract Test {
        function get() public returns (uint) {
            return value;
        }
    }
    """
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    contract = parser.parse()

    fn = contract.members[0]
    assert isinstance(fn.body[0], ReturnNode)
    assert fn.body[0].value == "value"


def test_return_without_value():
    code = """
    contract Test {
        function close() public {
            return;
        }
    }
    """
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    contract = parser.parse()

    fn = contract.members[0]
    assert isinstance(fn.body[0], ReturnNode)
    assert fn.body[0].value is None
