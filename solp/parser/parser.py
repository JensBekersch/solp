# arc42: 5.3.1 Main Parser
# The Parser coordinates the parsing process using a recursive descent
# strategy. It serves as the central entry point to initiate parsing from a
# list of tokens.
#
# Responsibilities:
# - Convert raw tokens into a navigable token stream
# - Instantiate and coordinate the RuleDispatcher
# - Delegate parsing to the top-level ContractRule
#
# This parser does not implement parsing logic itself.
# All grammar rules are modularized in dedicated rule classes
# (ContractRule, FunctionRule, etc.)

from solp.parser.dispatcher import RuleDispatcher
from solp.parser.rules.contract import ContractRule
from solp.parser.token_stream import TokenStream


class Parser:
    def __init__(self, tokens):
        # arc42: 5.3.1.1 Initialization
        # The parser wraps the token list in a TokenStream for controlled
        # access and sets up the RuleDispatcher used to invoke rule-based
        # parsing logic.
        self.tokens = TokenStream(tokens)
        self.rules = RuleDispatcher(self.tokens)

    def parse(self):
        # arc42: 5.3.1.2 Entry Point
        # Starts the parsing process and returns the root AST node.
        # In this grammar, a contract is always the top-level structure.
        return self.parse_contract()

    def parse_contract(self):
        # arc42: 5.3.1.3 Contract Delegation
        # Delegates contract parsing to ContractRule.
        return ContractRule(self.tokens, self.rules).parse()
