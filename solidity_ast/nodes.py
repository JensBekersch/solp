# arc42: 5.4 AST Nodes
# These represent the tree structure of Solidity source code after parsing.
from typing import Any


class ContractNode:
    def __init__(self, name, members):
        self.type = "Contract"
        self.name = name
        self.members = members


class VariableNode:
    def __init__(self, var_type, name, visibility=None):
        self.type = "Variable"
        self.var_type = var_type
        self.name = name
        self.visibility = visibility


class FunctionNode:
    def __init__(self, name, visibility=None, is_payable=False,
                 parameters=None, returns=None, body=None):
        self.type = "Function"
        self.name = name
        self.visibility = visibility
        self.is_payable = is_payable
        self.parameters = parameters or []
        self.returns = returns or []
        self.body = body or []


class StatementNode:
    type: str
    expr: Any

    def __init__(self, type_, **kwargs):
        self.type = type_
        for k, v in kwargs.items():
            setattr(self, k, v)


class ReturnNode:
    def __init__(self, value=None):
        self.type = "Return"
        self.value = value


class CallNode:
    def __init__(self, function, arguments):
        self.type = "Call"
        self.function = function
        self.arguments = arguments


class IfNode:
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class ConstructorNode:
    def __init__(self, parameters, visibility, body):
        self.parameters = parameters
        self.visibility = visibility
        self.body = body


class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForNode:
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body
