import ply.yacc as yacc
from LexYacc.MProjectLexer import tokens

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
    'expr : VARIABLE IN JSONLINES LPAREN INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN'
    p[0] = ['expr', [p[1], p[6]]]


def p_expr_3(p):
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

