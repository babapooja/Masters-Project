'''

link: https://polybox.ethz.ch/index.php/s/Qr2eo7nolAxP95d (slide 163-165) - chapter 13

Grammar:

    query: forclauses returnclause

    query: forclauses whereclause returnclause

    forclauses: forclause | forclauses forclause

    forclause: FOR exprs

    whereclause: WHERE  wexprs

    wexprs: wexpr | wexprs AND wexpr

    wexpr: VARIABLE DOT pathexpr condition VARIABLE DOT pathexpr
            | VARIABLE condition VARIABLE DOT pathexpr
            | VARIABLE condition VARIABLE
            | VARIABLE DOT pathexpr condition STRING 
            | VARIABLE condition STRING 
            | VARIABLE DOT pathexpr condition NUMBER
            | VARIABLE condition NUMBER
            | CONTAINS LPAREN VARIABLE DOT pathexpr COMMA STRING RPAREN
            | CONTAINS LPAREN VARIABLE COMMA STRING RPAREN

    condition: EQUAL | NOTEQUAL | GREATEREQUAL | GREATERTHAN | LESSEQUAL | LESSTHAN 

    exprs: exprs COMMA expr | expr

    expr: VARIABLE IN JSONLINES LPARENT INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN DOT pathexpr | rexpr

    pathexpr: pathexpr DOT step | step

    step: NAME LBRACKET selector RBRACKET | NAME

    selector:  | NUMBER

    returnclause: RETURN rexpr

    rexpr: VARIABLE DOT pathexpr | VARIABLE | LCBRACKET jsoncontents RCBRACKET

    jsoncontents : jsoncontents COMMA jsoncontent | jsoncontent

    jsoncontent : STRING COLON rexpr

'''

import ply.yacc as yacc
from MProjectLexer import tokens

# start of the query
def p_query_1(p):
    'query : forclauses whereclause returnclause'
    p[0] = [p[1], p[2], p[3]]

def p_query_2(p):
    'query : forclauses returnclause'
    p[0] = [p[1], p[2]]


########################################## for clauses definitions
def p_forclauses_1(p):
    'forclauses : forclauses forclause'
    p[0] = [p[1]]+p[2]

def p_forclauses_2(p):
    'forclauses : forclause'
    p[0] = p[1]

def p_forclause(p):
    'forclause : FOR exprs'
    p[0] = ['for', p[2]]

########################################### wherelcause
def p_whereclause_1(p):
    'whereclause : WHERE wexprs'
    p[0] = ['where', p[2]]

def p_wexprs_1(p):
    'wexprs : wexprs AND wexpr'
    p[0] = p[1] + [p[3]]

def p_wexprs_2(p):
    'wexprs : wexpr'
    p[0] = [p[1]]

########################################### where clause expressions
def p_wexpr_1(p):
    'wexpr : VARIABLE DOT pathexpr condition VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], p[4], [p[5], p[7]]]]

def p_wexpr_2(p):
    'wexpr : VARIABLE condition VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [p[1], p[2], [p[3], p[5]]]]

def p_wexpr_3(p):
    'wexpr : VARIABLE condition VARIABLE'
    p[0] = ['wexpr', [p[1], p[2], p[3]]]

def p_wexpr_4(p):
    'wexpr : VARIABLE DOT pathexpr condition STRING'
    p[0] = ['wexpr', [[p[1], p[3]], p[4], p[5]]]

def p_wexpr_5(p):
    'wexpr : VARIABLE condition STRING'
    p[0] = ['wexpr', [p[1], p[2], p[3]]]

def p_wexpr_6(p):
    'wexpr : VARIABLE DOT pathexpr condition NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], p[4], p[5]]]

def p_wexpr_7(p):
    'wexpr : VARIABLE condition NUMBER'
    p[0] = ['wexpr', [p[1], p[2], p[3]]]

def p_wexpr_8(p):
    'wexpr : CONTAINS LPAREN VARIABLE DOT pathexpr COMMA STRING RPAREN'
    p[0] = ['contains', [[p[3], p[5]], p[7]]]

def p_wexpr_9(p):
    'wexpr : CONTAINS LPAREN VARIABLE COMMA STRING RPAREN'
    p[0] = ['contains', [p[3], p[5]]]

########################################### conditions : EQUAL, NOTEQUAL, LESSEQUAL, LESSTHAN, GREATEREQUAL, GREATERTHAN
def p_condition_1(p):
    'condition : EQUAL'
    p[0] = '$eq'
    
def p_condition_2(p):
    'condition : NOTEQUAL'
    p[0] = '$ne'

def p_condition_3(p):
    'condition : GREATEREQUAL'
    p[0] = '$gte'

def p_condition_4(p):
    'condition : GREATERTHAN'
    p[0] = '$gt'

def p_condition_5(p):
    'condition : LESSEQUAL'
    p[0] = '$lte'

def p_condition_6(p):
    'condition : LESSTHAN'
    p[0] = '$lt'

########################################### for clause expressions

def p_exprs_1(p):
    'exprs : exprs COMMA expr'
    p[0] = p[1] + [p[3]]


def p_exprs_2(p):
    'exprs : expr'
    p[0] = [p[1]]


def p_expr_1(p):
    'expr : VARIABLE IN JSONLINES LPAREN INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN DOT pathexpr'
    p[0] = ['expr', [p[1], p[6], p[10]]]


def p_expr_2(p):
    'expr : rexpr'
    p[0] = p[1]


################################################ pathexpressions
def p_pathexpr_1(p):
    'pathexpr : pathexpr DOT step'
    p[0] = p[1] + [p[3]]


def p_pathexpr_2(p):
    'pathexpr : step'
    p[0] = [p[1]]

################################################ step
def p_step_1(p):
    'step : NAME LBRACKET selector RBRACKET'
    p[0] = [p[1], p[3]]


def p_step_2(p):
    'step : NAME'
    p[0] = p[1]


################################################## selectors
def p_selector_2(p):
    'selector : '
    p[0] = ''


def p_selector_1(p):
    'selector : NUMBER'
    p[0] = p[1]


###################################################### return clauses and return expressions
def p_returnclause_1(p):
    'returnclause : RETURN rexpr'
    p[0] = [p[1], p[2]]


def p_rexpr_1(p):
    'rexpr : VARIABLE DOT pathexpr'
    p[0] = [p[1], p[3]]


def p_rexpr_2(p):
    'rexpr : VARIABLE'
    p[0] = p[1]


def p_rexpr_3(p):
    'rexpr : LCBRACKET jsoncontents RCBRACKET'
    p[0] = ['{', p[2], '}']


def p_jsoncontents_1(p):
    'jsoncontents : jsoncontents COMMA jsoncontent'
    p[0] = p[1]+[p[3]]


def p_jsoncontents_2(p):
    'jsoncontents : jsoncontent'
    p[0] = [p[1]]


def p_jsoncontent(p):
    'jsoncontent : STRING COLON rexpr'
    p[0] = [p[1], p[3]]


def p_error(p):
    print("Syntax error at '%s'" % p.value)


parser = yacc.yacc()


inputdata = '''
for $faq in json-lines('collection-faq.json').faqs[]
            where $faq.title eq "Next-gen Databases"
            return $faq.tags  
'''

while True:
    try:
        # Use raw_input on Python 2
        res = parser.parse(inputdata)
        print('RES: ', res)
        break
    except EOFError:
        break
