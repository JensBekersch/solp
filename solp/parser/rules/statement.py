# arc42: 5.3.9 Statement Rule
# The StatementRule handles parsing of statements within function bodies.
#
# Supported:
# - return statements (`return;`, `return expr;`)
# - assignment statements (e.g. `x = 1;`, `y += 2;`)
# - expression statements (e.g. `require(x > 0);`)
#
from solp.solidity_ast.nodes import (
    StatementNode,
    ReturnNode,
    CallNode,
    IfNode,
    WhileNode,
    ForNode,
)
from solp.utils.errors import INVALID_EXPRESSION_START, EXPECTED_AFTER_DOT
from solp.lexer.token_types import (
    KEYWORD,
    IDENTIFIER,
    SYMBOL,
    OPERATOR,
    KW_RETURN,
    SYM_SEMICOLON,
    SYM_LBRACE,
    SYM_RBRACE,
    RULE_ASSIGNMENT,
    RULE_EXPRESSION,
    RULE_REQUIRE,
    SYM_LPAREN,
    SYM_RPAREN,
    SYM_COMMA,
    SYM_DOT,
    RULE_IF,
    RULE_ELSE,
    RULE_REVERT,
    RULE_ASSERT,
    RULE_EMIT,
    RULE_WHILE,
    RULE_FOR,
    RULE_BREAK,
    RULE_CONTINUE,
)


class StatementRule:
    def __init__(self, tokens, dispatcher=None):
        # arc42: 5.3.9.1 Initialization
        # Token stream is passed; dispatcher reserved for future
        # rule delegation.
        self.tokens = tokens

    def parse(self):
        # Parses a block of statements inside a function
        statements = []
        depth = 1  # count function-body braces
        while depth > 0:
            current = self.tokens.current()
            if not current:
                raise Exception("Unexpected EOF in function body")

            if current.type == SYMBOL and current.value == "}":
                break  # Stop parsing function body here

            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)

        return statements

    def parse_statement(self):
        # arc42: 5.3.9.3 Statement Dispatch
        # Dispatches to specific parsers based on token pattern.
        if self._is_return():
            return self._parse_return()
        if self._is_assignment():
            return self._parse_assignment()
        if self._is_require_call():
            return self._parse_require()
        if self._is_if():
            return self._parse_if()
        if self._is_revert():
            return self._parse_revert()
        if self._is_assert():
            return self._parse_assert()
        if self._is_emit():
            return self._parse_emit()
        if self._is_while():
            return self._parse_while()
        if self._is_for():
            return self._parse_for()
        if self._is_break():
            return self._parse_break()
        if self._is_continue():
            return self._parse_continue()
        return self._parse_expression_statement()

    def _is_return(self):
        return self._tok(KEYWORD, KW_RETURN)

    def _is_assignment(self):
        return self.tokens.current().type == IDENTIFIER

    def _parse_return(self):
        # arc42: 5.3.9.4 Return Statement
        self.tokens.expect(KEYWORD, KW_RETURN)
        if self._tok(SYMBOL, SYM_SEMICOLON):
            self.tokens.advance()
            return ReturnNode(value=None)
        value = self.parse_expression()
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)
        return ReturnNode(value=value)

    def _parse_require(self):
        self.tokens.expect(KEYWORD, RULE_REQUIRE)
        self.tokens.expect(SYMBOL, SYM_LPAREN)

        args = []
        while not self._tok(SYMBOL, SYM_RPAREN):
            if args:
                self.tokens.expect(SYMBOL, SYM_COMMA)
            args.append(self.parse_expression())

        self.tokens.expect(SYMBOL, SYM_RPAREN)
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)

        return StatementNode(
            RULE_EXPRESSION, expr=CallNode(RULE_REQUIRE, arguments=args)
        )

    def _parse_assignment(self):
        left = self.tokens.current().value
        self.tokens.expect(IDENTIFIER)

        if not self._is_operator():
            self._rewind()
            return None

        op = self.tokens.current().value
        self.tokens.expect(OPERATOR)
        right = self.parse_expression()
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)

        return StatementNode(RULE_ASSIGNMENT, left=left, operator=op, right=right)

    def _parse_if(self):
        # arc42: 5.3.9.6 If Statement
        # Parses conditional control flow with optional else blocks.
        # Supports syntax: if (cond) { ... } else { ... }
        self.tokens.expect(KEYWORD, RULE_IF)
        self.tokens.expect(SYMBOL, SYM_LPAREN)
        condition = self.parse_expression()
        self.tokens.expect(SYMBOL, SYM_RPAREN)

        self.tokens.expect(SYMBOL, SYM_LBRACE)
        then_block = self.parse()
        self.tokens.expect(SYMBOL, SYM_RBRACE)

        else_block = None
        if self._tok(KEYWORD, RULE_ELSE):
            self.tokens.advance()
            self.tokens.expect(SYMBOL, SYM_LBRACE)
            else_block = self.parse()
            self.tokens.expect(SYMBOL, SYM_RBRACE)

        return IfNode(condition=condition, then_block=then_block, else_block=else_block)

    def _parse_emit(self):
        # arc42: 5.3.9.8 Emit Statement
        # Parses event emission syntax:
        #   emit EventName(arg1, arg2);
        # The keyword "emit" is followed by an identifier and a
        # comma-separated argument list in parentheses. The result is a
        # StatementNode with type "emit", including the event name
        # and arguments.
        self.tokens.expect(KEYWORD, RULE_EMIT)
        event_name = self.tokens.current().value
        self.tokens.expect(IDENTIFIER)
        self.tokens.expect(SYMBOL, SYM_LPAREN)

        args = []
        while not self._tok(SYMBOL, SYM_RPAREN):
            if args:
                self.tokens.expect(SYMBOL, SYM_COMMA)
            args.append(self.parse_expression())

        self.tokens.expect(SYMBOL, SYM_RPAREN)
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)

        return StatementNode(RULE_EMIT, event=event_name, arguments=args)

    def _parse_while(self):
        # arc42: 5.3.9.9 While Statement
        # Parses Solidity while-loops of the form:
        #   while (condition) { ... }
        # Condition is an expression, body is a block of statements.
        self.tokens.expect(KEYWORD, RULE_WHILE)
        self.tokens.expect(SYMBOL, SYM_LPAREN)
        condition = self.parse_expression()
        self.tokens.expect(SYMBOL, SYM_RPAREN)

        self.tokens.expect(SYMBOL, SYM_LBRACE)
        body = self.parse()
        self.tokens.expect(SYMBOL, SYM_RBRACE)

        return WhileNode(condition, body)

    def _parse_for(self):
        # arc42: 5.3.9.10 For Statement
        # Parses Solidity for-loops of the form:
        #   for ([init]; [condition]; [increment]) { ... }
        # Each section is optional. Condition and increment are expressions.
        # Body is a list of statements. Result is a ForNode.
        self.tokens.expect(KEYWORD, RULE_FOR)
        self.tokens.expect(SYMBOL, SYM_LPAREN)

        # --- Initializer (can be statement or empty) ---
        init = None
        if not self._tok(SYMBOL, SYM_SEMICOLON):
            init = self.parse_statement()
        else:
            self.tokens.expect(SYMBOL, SYM_SEMICOLON)

        # --- Condition ---
        condition = None
        if not self._tok(SYMBOL, SYM_SEMICOLON):
            condition = self.parse_expression()
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)

        # --- Increment (expression or nothing) ---
        increment = None
        if not self._tok(SYMBOL, SYM_RPAREN):
            increment = self.parse_expression()
        self.tokens.expect(SYMBOL, SYM_RPAREN)

        # --- Body ---
        self.tokens.expect(SYMBOL, SYM_LBRACE)
        body = self.parse()
        self.tokens.expect(SYMBOL, SYM_RBRACE)

        return ForNode(init=init, condition=condition, increment=increment, body=body)

    def _parse_break(self):
        # arc42: 5.3.9.11 Break & Continue
        # Parses loop control statements:
        # - break;
        # - continue;
        # Each consists of a keyword followed by a semicolon.
        # Returned as StatementNode("break") or StatementNode("continue").
        self.tokens.expect(KEYWORD, RULE_BREAK)
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)
        return StatementNode(RULE_BREAK)

    def _parse_continue(self):
        self.tokens.expect(KEYWORD, RULE_CONTINUE)
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)
        return StatementNode(RULE_CONTINUE)

    def _parse_revert(self):
        return self._parse_builtin(RULE_REVERT)

    def _parse_assert(self):
        return self._parse_builtin(RULE_ASSERT)

    def _parse_expression_statement(self):
        expr = self.parse_expression()
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)
        return StatementNode(RULE_EXPRESSION, expr=expr)

    # TODO: Implement full expression parsing with precedence and binary
    #  operations
    def parse_expression(self):
        # arc42: 5.3.9.5 Expression Parser
        parts = []
        if not self._starts_expression():
            msg = INVALID_EXPRESSION_START.format(token=self.tokens.current())
            raise Exception(msg)

        parts.append(self.tokens.current().value)
        self.tokens.advance()

        while self.tokens.match(SYMBOL, SYM_DOT):
            if self.tokens.current().type not in {IDENTIFIER, KEYWORD}:
                raise Exception(EXPECTED_AFTER_DOT)
            parts.append(self.tokens.current().value)
            self.tokens.advance()

        full_name = SYM_DOT.join(parts)
        if not self.tokens.match(SYMBOL, SYM_LPAREN):
            return full_name

        args = []
        while True:
            if self._tok(SYMBOL, SYM_RPAREN):
                self.tokens.advance()
                break
            if args:
                self.tokens.expect(SYMBOL, SYM_COMMA)
            args.append(self.parse_expression())

        return CallNode(function=full_name, arguments=args)

    def _tok(self, type_, value=None):
        t = self.tokens.current()
        return t and t.type == type_ and (value is None or t.value == value)

    def _is_operator(self):
        return self.tokens.current().type == OPERATOR

    def _starts_expression(self):
        return self.tokens.current().type in {IDENTIFIER, KEYWORD}

    def _rewind(self):
        self.tokens.index -= 1

    def _parse_builtin(self, name):
        # arc42: 5.3.9.7 Revert and Assert Statements
        # Handles built-in Solidity control statements:
        # - revert("message");
        # - assert(condition);
        # Syntax and structure are unified with require(...) and reused
        # through a shared method.
        self.tokens.expect(KEYWORD, name)
        self.tokens.expect(SYMBOL, SYM_LPAREN)

        args = []
        while not self._tok(SYMBOL, SYM_RPAREN):
            if args:
                self.tokens.expect(SYMBOL, SYM_COMMA)
            args.append(self.parse_expression())

        self.tokens.expect(SYMBOL, SYM_RPAREN)
        self.tokens.expect(SYMBOL, SYM_SEMICOLON)

        return StatementNode(name, arguments=args)

    def _is_require_call(self):
        tok = self.tokens.current()
        return tok.type == KEYWORD and tok.value == RULE_REQUIRE

    def _is_if(self):
        return self._tok(KEYWORD, RULE_IF)

    def _is_revert(self):
        return self._tok(KEYWORD, RULE_REVERT)

    def _is_assert(self):
        return self._tok(KEYWORD, RULE_ASSERT)

    def _is_emit(self):
        return self._tok(KEYWORD, RULE_EMIT)

    def _is_while(self):
        return self._tok(KEYWORD, RULE_WHILE)

    def _is_for(self):
        return self._tok(KEYWORD, RULE_FOR)

    def _is_break(self):
        return self._tok(KEYWORD, RULE_BREAK)

    def _is_continue(self):
        return self._tok(KEYWORD, RULE_CONTINUE)
