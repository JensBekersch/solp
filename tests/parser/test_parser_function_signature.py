# testdoc: Purpose
# To test parsing of function parameters and return types
# in Solidity functions.
from solp.lexer.lexer import Lexer
from solp.parser.parser import Parser
from solp.solidity_ast.nodes import FunctionNode


def test_function_with_arguments_and_returns():
    code = """
    contract Token {
        function transfer(address to, uint amount) public returns (bool) {
        }
    }
    """
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    contract = parser.parse()

    fn = contract.members[0]
    assert isinstance(fn, FunctionNode)
    assert fn.name == "transfer"
    assert fn.visibility == "public"
    assert len(fn.parameters) == 2
    assert fn.parameters[0].var_type == "address"
    assert fn.parameters[0].name == "to"
    assert fn.parameters[1].var_type == "uint"
    assert fn.returns[0].var_type == "bool"
