# testdoc: Purpose
# To test if the parser can correctly extract contract and function structures.
from lexer.lexer import Lexer
from parser.parser import Parser


def test_parse_simple_contract():
    code = """
    contract Wallet {
        function deposit() public payable {
        }
    }
    """
    tokens = Lexer(code).tokenize()
    parser = Parser(tokens)
    contract = parser.parse()

    assert contract.name == "Wallet"
    assert len(contract.members) == 1
    fn = contract.members[0]
    assert fn.name == "deposit"
    assert fn.visibility == "public"
    assert fn.is_payable is True
