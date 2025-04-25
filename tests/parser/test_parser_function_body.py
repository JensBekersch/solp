# testdoc: Purpose
# To test parsing of basic function body statements, e.g. assignments.
from lexer.lexer import Lexer
from parser.parser import Parser
from solidity_ast.nodes import StatementNode


def test_function_body_assignment():
    code = """
    contract Wallet {
        function deposit() public payable {
            balance += msg.value;
        }
    }
    """
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    contract = parser.parse()
    fn = contract.members[0]

    assert len(fn.body) == 1
    stmt = fn.body[0]
    assert isinstance(stmt, StatementNode)
    assert stmt.type == "assignment"
    assert stmt.left == "balance"
    assert stmt.operator == "+="
    assert stmt.right == "msg.value"
