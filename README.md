# J2M Converter

This is my Master's project. The details of my advisor for this project are - 

Dr. Raj Sunderraman

_Professor and Associate Chair

Department of Computer Science

Georgia State University

P.O. Box 5060

Atlanta, GA 30302-5060

Website: http://tinman.cs.gsu.edu/~raj_

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

# I. User Manual

## MongoDB, Python
This project requires Python installed on your system. MongoDB can or cannot be installed on your system. MongoDB contains all the databases and collections requried. The configuration for MongoDB connection can be done in the `.jsoniq.cfg`. The configuration includes - `DATABASE_NAME`, `HOSTNAME`, `PORT`, `USERNAME`, `PASSWORD`

## How to invokse interpreter
Once the project is on the system and the database connection is configured, you can open the terminal in the project directory and execute the following command to run the python code - 
<p align="center">python main.py</p>
The program will start executing and provide area to type your JSONiq query. End your JSONiq query with a `;` to mark the end of the JSONiq query. After executing the JSONiq query, you will be prompted to continue with querying or exit the code. To exit the interpreter, you can either type, 'n', 'N', 'No', 'no' or 'NO'.

Below is a snippet of the above explanation -  

![cmd snippet](/Documents/cmd.png "Code run on CMD")

# II. Implementation

Following is the overall flowchart for the implementation of the project
![flowchart](/Documents/FlowChart-J2M.jpeg "FlowChart")

## Phase 1 (Lexical analysis and parsing)

### Lexical analysis
We have used [PLY](https://www.dabeaz.com/ply/) to implement the lexical analysis. Once the input is received, we have tokenized it to fetch the relevant information from the input query. Following is an example of the lexical analysis - 
```
<!-- defining the tokens -->
reserved = {
    'for': 'FOR',
    'in': 'IN',
    'where': 'WHERE',
    'return': 'RETURN',
    'eq': 'EQUAL',
    'ne': 'NOTEQUAL',
    'gt': 'GREATERTHAN',
    'gte': 'GREATEREQUAL',
    'lt': 'LESSTHAN',
    'lte': 'LESSEQUAL',
    'and': 'AND',
    'contains': 'CONTAINS'
}
tokens = [
    'NAME', 'DOT', 'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'STRING',
    'NUMBER', 'COMMA', 'JSONLINES', 'VARIABLE',  'FILENAME', "INVERTEDCOMMA",
    "LCBRACKET", "RCBRACKET", "COLON"
] + list(reserved.values())

<!-- regular expressions for token matching -->
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'  # eg: john
t_INVERTEDCOMMA = r'["\']'
t_FILENAME = r"[a-zA-Z_][a-zA-Z0-9-_]*.json"  # eg: 'abc.json'
t_VARIABLE = r'\$[a-zA-Z_][a-zA-Z0-9_]*'
t_DOT = r'\.'
t_COLON = r'\:'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCBRACKET = r'\{'
t_RCBRACKET = r'\}'
t_COMMA = r'\,'
t_ignore_COMMENT = r'\#.*'
```

### Parsing
We have used [PLY](https://www.dabeaz.com/ply/) to implement the parser. Once the tokens are received, we define grammar to generate rules for the query language. Then the token are structured together in list so as to form an Abstract Syntax Tree. Following is an example of the parser -

```
<!-- start of the query -->
def p_query_1(p):
    'query : forclauses whereclause returnclause'
    p[0] = [p[1], p[2], p[3]]
def p_query_2(p):
    'query : forclauses returnclause'
    p[0] = [p[1], p[2]]


<!-- for clauses definitions -->
def p_forclauses_1(p):
    'forclauses : forclauses forclause'
    p[0] = [p[1]]+p[2]
def p_forclauses_2(p):
    'forclauses : forclause'
    p[0] = p[1]
def p_forclause(p):
    'forclause : FOR exprs'
    p[0] = ['for', p[2]]

<!-- wherelcauses definition -->
def p_whereclause_1(p):
    'whereclause : WHERE wexprs'
    p[0] = ['where', p[2]]
def p_wexprs_1(p):
    'wexprs : wexprs AND wexpr'
    p[0] = p[1] + [p[3]]
def p_wexprs_2(p):
    'wexprs : wexpr'
    p[0] = [p[1]]
....
```

### Data Structures
We have made use to the array data structure for this implementation. Let us take a look at the example below - 
[['for', [['expr', ['$x', 'collection-faq.json', [['faqs', '']]]]]], ['return', ['$x', [['tags', 1]]]]]

For the above example, the AST and the Expression Tree generated will look something like the one in the below snippet - 

![astet](/Documents/AST-ET.jpg "AST-ET.jpg")

## Phase 2 (Semantic Checks)

In this phase, we check for the variables if they have been defined previous to their use. If in case they fail to satisfy the condition, we raise an error and stop the execution of the code.

## Phase 3 (Query translation and Execution)

Once the semantic checks have been performed and there are no errors, we proceed with the execution of the query entered by the user. We segrgate the `for clause`, `return clause` and `where clause`(if any) statements. Once they are segregated a connection is established to the MongoDB database based on the connection details provided in the `.jsoniq.cfg` configuration file.

Later all the statements are stiched together based on the JSONiq query and the MongoDB query is formed. The MongoDB query is then executed with the help of `pymongo` and `MongoClient`. 

Once the results are fetched, we run through the `return clause` from the JSONiq query to understand what exact details are asked. THe output data is then formed conforming to the JSONiq query and returned to the command prompt, the interpreter. 

If there is any error while executing the query, there will be an error message displayed in the console in red color. If the data is fetched successfully and the result data is formed, a success message is displayed on the interpreter in green color and the results are displayed on the console.
_
Note: MongoDB does not give an error if a database or collection is not found. Infact it creates one instance as blank and works on it. 
If such an anamoly happens in the execution of this project and no data is found to operate on, an error message will be displayed on the console to recheck the query._

