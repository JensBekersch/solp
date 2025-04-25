# testdoc: Purpose
# To test parsing of contract-level variable declarations.

# testdoc: Method
# Various declarations with types and optional visibility are parsed and their
# resulting AST nodes are validated.

from lexer.lexer import Lexer
from parser.parser import Parser
from solidity_ast.nodes import VariableNode


def test_parse_variable_declarations():
    code = """
    contract Test {
        uint balance;
        string name;
        address public owner;
    }
    """
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    contract = parser.parse()

    assert contract.name == "Test"
    assert len(contract.members) == 3

    v1, v2, v3 = contract.members
    assert isinstance(v1, VariableNode)
    assert v1.var_type == "uint"
    assert v1.name == "balance"

    assert v2.var_type == "string"
    assert v2.name == "name"
    assert v2.visibility is None

    assert v3.var_type == "address"
    assert v3.name == "owner"
    assert v3.visibility == "public"
