#J2M Converter

This open source project provides an implmentation of parsing JSONiq query entered by user, generating MongoDB query return the result after querying the MongoDB. This project requires MongoDB installed along with the collections created.

## Context-Free Grammer

`
query ::= forclauses whereclause returnclause | forclauses returnclause
forclauses ::= forclause | forclauses forclause
forclause ::= FOR exprs
whereclause ::= WHERE wexprs
wexprs ::= wexpr | wexprs AND wexpr
wexpr ::= VARIABLE DOT pathexpr condition VARIABLE DOT pathexpr
    | VARIABLE condition VARIABLE DOT pathexpr
    | VARIABLE condition VARIABLE
    | VARIABLE DOT pathexpr condition STRING
    | VARIABLE condition STRING
    | VARIABLE DOT pathexpr condition NUMBER
    | VARIABLE condition NUMBER
    | CONTAINS LPAREN VARIABLE DOT pathexpr COMMA STRING RPAREN
    | CONTAINS LPAREN VARIABLE COMMA STRING RPAREN
condition ::= EQUAL | NOTEQUAL | GREATEREQUAL | GREATERTHAN | LESSEQUAL | LESSTHAN
exprs ::= exprs COMMA expr | expr
expr ::= VARIABLE IN JSONLINES LPAREN INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN DOT pathexpr | rexpr
    | VARIABLE IN JSONLINES LPAREN INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN
    | rexpr
pathexpr ::= pathexpr DOT step | step
step ::= NAME LBRACKET selector RBRACKET | NAME
selector ::= | NUMBER
returnclause ::= RETURN rexpr
rexpr ::= VARIABLE DOT pathexpr | VARIABLE | LCBRACKET jsoncontents RCBRACKET
jsoncontents ::= jsoncontents COMMA jsoncontent | jsoncontent
jsoncontent ::= STRING COLON rexpr

`
