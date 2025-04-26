# arc42: 5.3.2 Rule Dispatcher
# The RuleDispatcher acts as a central registry and delegation hub for
# all parser rules.Each rule (function, contract, variable, statements)
# is encapsulated in its own class. The dispatcher maps rule names to their
# respective parser classes and ensures correct instantiation and dependency
# injection (e.g., passing the token stream and dispatcher itself).
#
# Benefits:
# - Centralized control over parsing behavior
# - Loose coupling between parser components
# - Easy extensibility: new rules can be added in one place
# - Enables unit testing of each rule in isolation
from solp.parser.rules.constructor import ConstructorRule
from solp.parser.rules.function import FunctionRule
from solp.parser.rules.variable import VariableRule
from solp.parser.rules.statement import StatementRule
from solp.parser.rules.contract import ContractRule

# arc42: 5.3.2.1 Rule Name Constants
# These constants define all supported parser rules to avoid magic strings.
RULE_CONTRACT = "contract"
RULE_FUNCTION = "function"
RULE_VARIABLE = "variable"
RULE_STATEMENTS = "statements"
RULE_CONSTRUCTOR = "constructor"


class RuleDispatcher:
    def __init__(self, token_stream):
        # arc42: 5.3.2.2 Initialization
        # The dispatcher holds a reference to the active token stream and
        # is passed to rule classes that require further delegation.
        self.tokens = token_stream

    def parse_rule(self, rule_name):
        # arc42: 5.3.2.3 Rule Delegation
        # This method maps the rule_name to a corresponding parser class,
        # creates the parser instance, injects required dependencies,
        # and returns the resulting AST node.
        #
        # This dispatcher currently supports:
        # - contract: ContractRule
        # - function: FunctionRule
        # - variable: VariableRule
        # - statements: StatementRule

        if rule_name == RULE_CONTRACT:
            return ContractRule(self.tokens, self).parse()

        if rule_name == RULE_FUNCTION:
            return FunctionRule(self.tokens, self).parse()

        if rule_name == RULE_VARIABLE:
            return VariableRule(self.tokens).parse()

        if rule_name == RULE_STATEMENTS:
            return StatementRule(self.tokens).parse()

        if rule_name == RULE_CONSTRUCTOR:
            return ConstructorRule(self.tokens, self).parse()

        # arc42: 5.3.2.4 Error Handling
        # Raises a descriptive exception for unknown rules
        raise Exception(f"Unknown parse rule: {rule_name}")
