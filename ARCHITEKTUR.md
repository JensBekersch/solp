# Architekturübersicht (generiert aus Code-Kommentaren)

## 5.2 Lexer Internal Structure

The Lexer operates linearly over the input source code, character by
character. Each recognized unit (identifier, keyword, number, operator, etc.)
is converted into a Token object.

---

## 5.2.12 Symbols

Symbols such as `{`, `;`, and `(` are matched directly by checking if the
current character exists in the predefined SYMBOLS list. Each match results
in a single SYMBOL token.

---

## 5.3 Token Object

Each Token includes:
- type (e.g. KEYWORD, IDENTIFIER, OPERATOR)
- value (string representation)
- position (line, column)
- subtype (optional: e.g. operator group)

---

## 5.3.1 Token Stream

The TokenStream wraps a flat list of tokens and provides controlled,
lookahead-based navigation for parser rules. It ensures safe access to
tokens using a cursor-based API.

Responsibilities:
- Provide peekable access to the current and upcoming tokens
- Offer utility functions for advancing and consuming tokens
- Centralize matching and error reporting for expected patterns
- Prevent out-of-bounds access by returning None safely

---

## 5.3.1 Main Parser

The Parser coordinates the parsing process using a recursive descent
strategy. It serves as the central entry point to initiate parsing from a
list of tokens.

Responsibilities:
- Convert raw tokens into a navigable token stream
- Instantiate and coordinate the RuleDispatcher
- Delegate parsing to the top-level ContractRule

This parser does not implement parsing logic itself.
All grammar rules are modularized in dedicated rule classes
(ContractRule, FunctionRule, etc.)

---

## 5.3.2 Rule Dispatcher

The RuleDispatcher acts as a central registry and delegation hub for
all parser rules.Each rule (function, contract, variable, statements)
is encapsulated in its own class. The dispatcher maps rule names to their
respective parser classes and ensures correct instantiation and dependency
injection (e.g., passing the token stream and dispatcher itself).

Benefits:
- Centralized control over parsing behavior
- Loose coupling between parser components
- Easy extensibility: new rules can be added in one place
- Enables unit testing of each rule in isolation

---

## 5.3.2.1 Rule Name Constants

These constants define all supported parser rules to avoid magic strings.

---

## 5.3.6 Contract Rule

This rule parses Solidity contract declarations. It handles:
- the contract keyword and name (header)
- the opening and closing braces
- delegation of contract members (e.g. functions, variables) to other rules
The contract body is iterated token by token and parsed modularly via
the dispatcher.

---

## 5.3.7 Function Rule

This rule parses Solidity function declarations.
Responsibilities:
- Parse the function header (keyword and name)
- Parse the parameter list
- Parse optional function modifiers (visibility, payable)
- Parse optional return types (via 'returns')
- Parse the function body using the delegated 'statements' rule
Output: A fully constructed FunctionNode in the AST

---

## 5.3.8 Variable Rule

This rule parses top-level state variable declarations in Solidity contracts.
A variable can include:
- a type (e.g., uint, address)
- an optional visibility modifier (public/private/internal/external)
- a name (identifier)
- a semicolon to terminate the declaration

---

## 5.3.9 Statement Rule

The StatementRule handles parsing of statements within function bodies.

Supported:
- return statements (`return;`, `return expr;`)
- assignment statements (e.g. `x = 1;`, `y += 2;`)
- expression statements (e.g. `require(x > 0);`)


---

## 5.3.10 Constructor Rule

Handles parsing of Solidity constructors.
Constructors:
- use the keyword `constructor`
- may include parameters and visibility
- have no name or return type
- contain a standard statement block
Results in a ConstructorNode for use in ContractNode.members

---

## 5.4 AST Nodes

These represent the tree structure of Solidity source code after parsing.

---

