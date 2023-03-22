'''
Grammar:

    query: forclauses returnclause

    query: forclauses whereclauses returnclause

    forclauses: forclause | forclauses forclause

    forclause: FOR exprs

    whereclauses: whereclause | whereclauses whereclause

    whereclause: WHERE  wexprs 
    
    wexprs: wexprs COMMA wexpr | wexpr
    
    wexpr: VARIABLE DOT pathexpr EQUAL VARIABLE DOT pathexpr 
            | WHERE VARIABLE DOT pathexpr EQUAL STRING 
            | WHERE VARIABLE DOT pathexpr EQUAL NUMBER
            | WHERE VARIABLE DOT pathexpr NOTEQUAL VARIABLE DOT pathexpr 
            | WHERE VARIABLE DOT pathexpr NOTEQUAL STRING 
            | WHERE VARIABLE DOT pathexpr NOTEQUAL NUMBER
            | WHERE VARIABLE DOT pathexpr GREATERTHANEQUAL VARIABLE DOT pathexpr 
            | WHERE VARIABLE DOT pathexpr GREATERTHANEQUAL STRING 
            | WHERE VARIABLE DOT pathexpr GREATERTHANEQUAL NUMBER
            | WHERE VARIABLE DOT pathexpr GREATERTHAN VARIABLE DOT pathexpr 
            | WHERE VARIABLE DOT pathexpr GREATERTHAN STRING 
            | WHERE VARIABLE DOT pathexpr GREATERTHAN NUMBER
            | WHERE VARIABLE DOT pathexpr LESSTHANEQUAL VARIABLE DOT pathexpr 
            | WHERE VARIABLE DOT pathexpr LESSTHANEQUAL STRING 
            | WHERE VARIABLE DOT pathexpr LESSTHANEQUAL NUMBER
            | WHERE VARIABLE DOT pathexpr LESSTHAN VARIABLE DOT pathexpr 
            | WHERE VARIABLE DOT pathexpr LESSTHAN STRING 
            | WHERE VARIABLE DOT pathexpr LESSTHAN NUMBER

    exprs: exprs COMMA expr | expr

    expr: VARIABLE IN JSONLINES LPARENT INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN DOT pathexpr | rexpr

    pathexpr: pathexpr DOT step | step

    step: NAME LBRACKET selector RBRACKET | NAME

    selector:  | NUMBER

    returnclause: RETURN rexpr

    rexpr: VARIABLE DOT pathexpr | VARIABLE | LCBRACKET jsoncontents RCBRACKET

    jsoncontents : jsoncontents COMMA jsoncontent | jsoncontent

    jsoncontent : STRING COLON rexpr

Examples:
1. for  $question in json-lines("collection-faq.json").faqs[0],
        $answer in json-lines("collection-answers.json").answers[1] 
    return $x.owner

2. for $x in json-lines("collection_name.json").answers[0] return $x.owner.display_name

3. for $x in json-lines("collection_name.json").answers[0].abc return {"name":$x.owner[].display_name, "address":$x.owner[].display_name}

'''

import ply.yacc as yacc
from MProjectLexer import tokens

# start of the query


def p_query_1(p):
    'query : forclauses whereclauses returnclause'
    p[0] = [p[1], p[2], p[3]]

def p_query_2(p):
    'query : forclauses returnclause'
    p[0] = [p[1], p[2]]


# for clauses definitions
def p_forclauses_1(p):
    'forclauses : forclauses forclause'
    p[0] = [p[1]]+p[2]


def p_forclauses_2(p):
    'forclauses : forclause'
    p[0] = p[1]


def p_forclause(p):
    'forclause : FOR exprs'
    p[0] = ['for', p[2]]

# whereclauses definitions


def p_whereclauses_1(p):
    'whereclauses : whereclauses whereclause'
    p[0] = [p[1]]+p[2]


def p_whereclauses_2(p):
    'whereclauses : whereclause'
    p[0] = p[1]


def p_whereclause(p):
    'whereclause : WHERE wexprs'
    p[0] = ['where', p[2]]

########################################### whereclause : wexprs


def p_wexprs_1(p):
    'wexprs : wexprs COMMA wexpr'
    p[0] = p[1] + [p[3]]


def p_wexprs_2(p):
    'wexprs : wexpr'
    p[0] = [p[1]]

# EQUAL
def p_wexpr_1(p):
    'wexpr : VARIABLE DOT pathexpr EQUAL VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], 'eq', [p[5], p[7]]]]

def p_wexpr_2(p):
    'wexpr : VARIABLE DOT pathexpr EQUAL STRING'
    p[0] = ['wexpr', [[p[1], p[3]], 'eq', p[5]]]

def p_wexpr_3(p):
    'wexpr : VARIABLE DOT pathexpr EQUAL NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], 'eq', p[5]]]

# NOTEQUAL
def p_wexpr_4(p):
    'wexpr : VARIABLE DOT pathexpr NOTEQUAL VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], 'ne', [p[5], p[7]]]]

def p_wexpr_5(p):
    'wexpr : VARIABLE DOT pathexpr NOTEQUAL STRING'
    p[0] = ['wexpr', [[p[1], p[3]], 'ne', p[5]]]

def p_wexpr_6(p):
    'wexpr : VARIABLE DOT pathexpr NOTEQUAL NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], 'ne', p[5]]]

# LESS-THAN-EQUAL
def p_wexpr_7(p):
    'wexpr : VARIABLE DOT pathexpr LESSTHANEQUAL VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], 'lte', [p[5], p[7]]]]

def p_wexpr_8(p):
    'wexpr : VARIABLE DOT pathexpr LESSTHANEQUAL STRING'
    p[0] = ['wexpr', [[p[1], p[3]], 'lte', p[5]]]

def p_wexpr_9(p):
    'wexpr : VARIABLE DOT pathexpr LESSTHANEQUAL NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], 'lte', p[5]]]

# LESS-THAN
def p_wexpr_10(p):
    'wexpr : VARIABLE DOT pathexpr LESSTHAN VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], 'lt', [p[5], p[7]]]]

def p_wexpr_11(p):
    'wexpr : VARIABLE DOT pathexpr LESSTHAN STRING'
    p[0] = ['wexpr', [[p[1], p[3]], 'lt', p[5]]]

def p_wexpr_12(p):
    'wexpr : VARIABLE DOT pathexpr LESSTHAN NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], 'lt', p[5]]]

# GREATER-THAN-EQUAL
def p_wexpr_13(p):
    'wexpr : VARIABLE DOT pathexpr GREATERTHANEQUAL VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], 'gte', [p[5], p[7]]]]

def p_wexpr_14(p):
    'wexpr : VARIABLE DOT pathexpr GREATERTHANEQUAL STRING'
    p[0] = ['wexpr', [[p[1], p[3]], 'gte', p[5]]]

def p_wexpr_15(p):
    'wexpr : VARIABLE DOT pathexpr GREATERTHANEQUAL NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], 'gte', p[5]]]

# GREATER-THAN
def p_wexpr_16(p):
    'wexpr : VARIABLE DOT pathexpr GREATERTHAN VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], 'gt', [p[5], p[7]]]]

def p_wexpr_17(p):
    'wexpr : VARIABLE DOT pathexpr GREATERTHAN STRING'
    p[0] = ['wexpr', [[p[1], p[3]], 'gt', p[5]]]

def p_wexpr_18(p):
    'wexpr : VARIABLE DOT pathexpr GREATERTHAN NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], 'gt', p[5]]]

########################################### forclause : exprs


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


def p_pathexpr_1(p):
    'pathexpr : pathexpr DOT step'
    p[0] = p[1] + [p[3]]


def p_pathexpr_2(p):
    'pathexpr : step'
    p[0] = [p[1]]


def p_step_1(p):
    'step : NAME LBRACKET selector RBRACKET'
    p[0] = [p[1], p[3]]


def p_step_2(p):
    'step : NAME'
    p[0] = p[1]

# recheck


def p_selector_2(p):
    'selector : '
    p[0] = ''


def p_selector_1(p):
    'selector : NUMBER'
    p[0] = p[1]


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
FOR $x in json-lines("collection-answers.json").answers[]
            return
                {
                    "answer_id" : $x.answer_id,
                    "q_id" : $x.question_id
                }
'''

# while True:
#     try:
#         # Use raw_input on Python 2
#         res = parser.parse(inputdata)
#         print('RES: ', res)
#         break
#     except EOFError:
#         break
