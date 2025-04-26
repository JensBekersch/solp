# readme: Project Description
# Solidity Parser Library – A modular Python library for lexical and structural
# analysis of Solidity smart contracts. Designed for extensibility,
# transparency, and full testability.
from solp.lexer.lexer import Lexer
from solp.parser.parser import Parser


def parse_contract(source_code: str):
    """
    Parses Solidity source code into an AST ContractNode.

    :param source_code: Solidity source code as string
    :return: ContractNode representing the parsed AST
    :raises: ParseError if the source code cannot be parsed
    """
    tokens = Lexer(source_code).tokenize()
    parser = Parser(tokens)

    return parser.parse()
