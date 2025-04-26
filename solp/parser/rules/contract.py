# arc42: 5.3.6 Contract Rule
# This rule parses Solidity contract declarations. It handles:
# - the contract keyword and name (header)
# - the opening and closing braces
# - delegation of contract members (e.g. functions, variables) to other rules
# The contract body is iterated token by token and parsed modularly via
# the dispatcher.
from solp.lexer.token_types import (
    IDENTIFIER,
    KEYWORD,
    KW_CONSTRUCTOR,
    KW_CONTRACT,
    KW_FUNCTION,
    KW_TYPES,
    RULE_FUNCTION,
    RULE_VARIABLE,
    SYM_LBRACE,
    SYM_RBRACE,
    SYMBOL,
)
from solp.solidity_ast.nodes import ContractNode


class ContractRule:
    def __init__(self, tokens, dispatcher):
        # arc42: 5.3.6.1 Initialization
        # The rule receives a token stream and a dispatcher used to
        # invoke sub-rules
        self.tokens = tokens
        self.dispatcher = dispatcher

    def parse(self):
        # arc42: 5.3.6.2 Entry Point
        # The main parsing method for a contract.
        name = self.parse_contract_header()
        members = self.parse_members()

        return ContractNode(name, members)

    def parse_contract_header(self):
        # arc42: 5.3.6.3 Contract Header
        # Parses the "contract" keyword, contract name, and opening brace
        self.tokens.expect(KEYWORD, KW_CONTRACT)
        self.tokens.expect(IDENTIFIER)
        name = self.tokens.last().value
        self.tokens.expect(SYMBOL, SYM_LBRACE)

        return name

    def parse_members(self):
        members = []
        while True:
            if self.tokens.current() is None:
                raise Exception("Unexpected EOF while parsing contract members")

            if self.tokens.match(SYMBOL, SYM_RBRACE):
                break

            member = self.next_member_or_skip()
            if member:
                members.append(member)

        return members

    def next_member_or_skip(self):
        # arc42: 5.3.6.5 Member Wrapper
        # Wraps `parse_member()` and ensures that the token stream advances
        # even if a member could not be parsed.
        member = self.parse_member()
        if member:
            return member
        self.tokens.advance()
        return None

    def parse_member(self):
        # arc42: 5.3.6.6 Member Dispatch
        # Checks which kind of member is next (e.g. function, variable)
        # and delegates to the corresponding rule via dispatcher.
        current = self.tokens.current()
        if not current:
            return None

        if current.type == KEYWORD and current.value == KW_FUNCTION:
            return self.dispatcher.parse_rule(RULE_FUNCTION)
        if current.type == KEYWORD and current.value in KW_TYPES:
            return self.dispatcher.parse_rule(RULE_VARIABLE)
        if current.type == KEYWORD and current.value == KW_CONSTRUCTOR:
            return self.dispatcher.parse_rule(KW_CONSTRUCTOR)
        return None
