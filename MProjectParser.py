'''
Grammar:

    query: forclauses returnclause

    forclauses: forclause | forclauses forclause

    forclause: FOR exprs

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


def p_query(p):
    'query : forclauses returnclause'
    p[0] = [p[1], p[2]]


def p_forclauses_1(p):
    'forclauses : forclauses forclause'
    p[0] = [p[1]]+p[2]


def p_forclauses_2(p):
    'forclauses : forclause'
    p[0] = p[1]


def p_forclause(p):
    'forclause : FOR exprs'
    p[0] = ['for', p[2]]


def p_exprs_1(p):
    'exprs : exprs COMMA expr'
    p[0] = p[1] + [p[3]]


def p_exprs_2(p):
    'exprs : expr'
    p[0] = [p[1]]


def p_expr_1(p):
    'expr : VARIABLE IN JSONLINES LPAREN INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN DOT pathexpr'
    p[0] = ['expr', [p[1], p[6], p[10]]]  # record the computable values


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

# while True:
#     try:
#         # Use raw_input on Python 2
#         res = parser.parse(inputdata)
#         print('RES: ', res)
#         break
#     except EOFError:
#         break