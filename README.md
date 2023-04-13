#J2M Converter

This open source project provides an implmentation of parsing JSONiq query entered by user, generating MongoDB query return the result after querying the MongoDB.

## Context-Free Grammer

Grammar generated for `for clause`, `where clause` and `return clause` in the `FLWOR` expression.

```
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
```

# User Manual

## MongoDB, Python
This project requires Python installed on your system. MongoDB can or cannot be installed on your system. MongoDB contains all the databases and collections requried. The configuration for MongoDB connection can be done in the `.jsoniq.cfg`. The configuration includes - `DATABASE_NAME`, `HOSTNAME`, `PORT`, `USERNAME`, `PASSWORD`

## How to invokde interpreter
Once the project is on the system and the database connection is configured, you can open the terminal in the project directory and execute the following command to run the python code - 
<p align="center">`python main.py`</p>
The program will start executing and provide area to type your JSONiq query. End your JSONiq query with a `;` to mark the end of the JSONiq query. After executing the JSONiq query, you will be prompted to continue with querying or exit the code. To exit the interpreter, you can either type, 'n', 'N', 'No', 'no' or 'NO'.

Below is a snippet of the above explanation -  

![cmd snippet](/Documents/cmd.png "Code run on CMD")
