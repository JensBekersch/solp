# testdoc: Purpose
# To test parsing of expression-based statements such as `require(...)`
# or other function calls that are used as standalone statements.

# testdoc: Scope
# Focuses on function call expressions inside function bodies, specifically
# those wrapped in a StatementNode of type "expression".

from solp.lexer.lexer import Lexer
from solp.parser.parser import Parser
from solp.solidity_ast.nodes import CallNode, StatementNode


def test_require_call_statement():
    # testdoc: Parses `require(x > 0);` as an expression statement
    # with a CallNode
    code = """
    contract Test {
        function check(uint x) public {
            require(x);
        }
    }
    """
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    contract = parser.parse()

    stmt = contract.members[0].body[0]
    assert isinstance(stmt, StatementNode)
    assert stmt.type == "expression"
    assert isinstance(stmt.expr, CallNode)
    assert stmt.expr.function == "require"
    assert isinstance(stmt.expr.arguments, list)
    assert len(stmt.expr.arguments) == 1
