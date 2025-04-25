# Testdokumentation (automatisch generiert)

## test_contract.py

### Purpose

To test each method of ContractRule in isolation. This supports modular,
high-confidence development of parser rules and allows fine-grained
diagnostics on failure.

### Scope

Each test focuses on one method from ContractRule (header parsing,
member loop, etc.). Token stream and dispatcher are mocked or simplified
as needed.


---

## test_function.py

### Purpose

These tests verify the correctness of each parsing component in FunctionRule.
Each method is tested in isolation using a mock token stream and optional dispatcher.

### Scope

Covers:
- Function header parsing
- Parameter list parsing
- Modifier (visibility/payable) parsing
- Return type parsing
- Full parse integration


---

## test_lexer_boolean.py

### Purpose

Booleans in Solidity are reserved keywords: `true` and `false`.

### Method

Check if these values are recognized as KEYWORD tokens with correct value.


---

## test_lexer_identifiers.py

### Purpose

To verify that valid Solidity identifiers (contract names, variable names,
etc.) # are correctly recognized and returned as IDENTIFIER tokens.

### Method

Simple strings are passed to the lexer. Each must return a single token of
type IDENTIFIER.

### Coverage

Covers legal identifier formats: camelCase, PascalCase, underscores,
numbers (not leading).

### Scope Limit

This test does not check for reserved keywords or parser behavior.


---

## test_lexer_keywords.py

### Purpose

To ensure each Solidity keyword is correctly recognized by the lexer
and assigned the type 'KEYWORD'.

### Method

A parameterized test case automatically checks each keyword defined
in `keywords.py`. For each input, the lexer should return a single token
with the correct type and value.

### Coverage

Full coverage of all Solidity language keywords currently known.
This test will fail if any are added or changed without adjusting the test
list.

### Edge Cases

Detects typographical errors or accidental keyword renaming in the keyword
list.


---

## test_lexer_numbers.py

### Purpose

To verify that integer literals are correctly recognized as NUMBER tokens.

### Method

Various numeric strings (decimal only) are passed to the lexer.

### Coverage

Covers positive integers in decimal form (hex, exp-form to be added later).

### Scope Limit

Does not test signed numbers, floats, hex, or scientific notation.


---

## test_lexer_operators.py

### Purpose

To ensure the lexer identifies all Solidity operators correctly and returns
one token per operator input with the correct type and value. We do not test
the internals of the Token class here.

### Method

Each operator string is passed alone into the Lexer.
We verify that the lexer returns a single token with the type "OPERATOR"
and the expected value. No assumptions are made about internal Token
structure.

### Coverage

Covers all operators listed in OPERATOR_GROUPS.

### Scope Limit

This test intentionally avoids testing the Token class itself
(subtype, line, col). Those aspects are to be tested separately.


---

## test_lexer_strings.py

### Purpose

To ensure the lexer correctly identifies and extracts string literals,
enclosed in single or double quotes.

### Method

Various quoted string inputs are lexed and compared to expected values.
Escape sequences are treated as literal characters for now.

### Coverage

Single-quoted and double-quoted strings, escaped quote inside string.

### Scope Limit

Does not validate full escape sequence rules (e.g. \n, \xFF)


---

## test_lexer_symbols.py

### Purpose

To ensure the lexer correctly identifies all Solidity structural symbols
and punctuators.

### Method

Each symbol is tested individually. The lexer should return a single token of
type "SYMBOL"
and the correct value.

### Coverage

Tests every character defined in `symbols.py`. No duplicates or subsets
should be skipped.

### Scope Limit

This test does not validate position tracking (line/col) or Token class
internals.


---

## test_parser_call_statements.py

### Purpose

To test parsing of expression-based statements such as `require(...)`
or other function calls that are used as standalone statements.

### Scope

Focuses on function call expressions inside function bodies, specifically
those wrapped in a StatementNode of type "expression".


---

## test_parser_contract.py

### Purpose

To test if the parser can correctly extract contract and function structures.


---

## test_parser_function_body.py

### Purpose

To test parsing of basic function body statements, e.g. assignments.


---

## test_parser_function_signature.py

### Purpose

To test parsing of function parameters and return types
in Solidity functions.


---

## test_parser_return.py

### Purpose

To test parsing of return statements with and without values.

### Method

Validates that return statements inside a function body are parsed into
ReturnNode, with or without a value (e.g. `return;` vs. `return x;`).


---

## test_parser_variables.py

### Purpose

To test parsing of contract-level variable declarations.

### Method

Various declarations with types and optional visibility are parsed and their
resulting AST nodes are validated.


---

## test_statement_rule.py

### Purpose

This suite verifies that StatementRule correctly parses all supported
Solidity statements.

### Scope

Includes return, assignment, expressions, require, revert, assert, emit,
control flow (if, while, for), and loop modifiers (break, continue).


---

## test_token.py

### Purpose

To ensure the Token class behaves correctly as a data structure for
lexical tokens.
This includes construction, default values, and string representation.

### Method

Tokens are manually instantiated and checked for correct field assignment
and __repr__ output.

### Coverage

Covers all public fields: type, value, line, col, subtype

### Scope Limit

This test does not depend on lexer logic or actual tokenization behavior.


---

## test_variable_rule.py

### Purpose

To verify that top-level variable declarations are parsed correctly
by VariableRule.

### Scope

This includes type, optional visibility, and name extraction.


---

