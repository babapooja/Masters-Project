'''

link: https://polybox.ethz.ch/index.php/s/Qr2eo7nolAxP95d (slide 163-165) - chapter 13

Grammar:

    query: forclauses returnclause

    query: forclauses whereclause returnclause

    forclauses: forclause | forclauses forclause

    forclause: FOR exprs

    whereclause: WHERE  wexpr
                | WHERE quantifier VARIABLE DOT pathexpr IN VARIABLE dot pathexpr SATISFIES wexpr
                | WHERE quantifier VARIABLE DOT pathexpr IN expr SATISFIES wexpr

    quantifier: SOME | EVERY

    wexpr: VARIABLE DOT pathexpr condition VARIABLE DOT pathexpr 
            | VARIABLE DOT pathexpr condition STRING 
            | VARIABLE DOT pathexpr condition NUMBER
            | CONTAINS LPAREN VARIABLE DOT pathexpr COMMA STRING RPAREN

    condition: EQUAL | NOTEQUAL | GREATERTHANEQUAL | GREATERTHAN | LESSTHANEQUAL | LESSTHAN 

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
    'whereclause : WHERE wexpr'
    p[0] = ['where', p[2]]

def p_whereclause_2(p):
    'whereclause : WHERE quantifier VARIABLE DOT pathexpr IN VARIABLE DOT pathexpr SATISFIES wexpr'
    p[0] = ['where', [
                p[2], [[p[3], p[5]]], 
                [p[7], p[9]], 
                p[11]
            ]
        ]

def p_whereclause_3(p):
    'whereclause : WHERE quantifier VARIABLE IN VARIABLE DOT pathexpr SATISFIES wexpr'
    p[0] = ['where', [
                p[2], p[3], 
                [p[5], p[7]], 
                p[9]
            ]
        ]

def p_whereclause_4(p):
    'whereclause : WHERE quantifier VARIABLE DOT pathexpr IN JSONLINES LPAREN INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN DOT pathexpr SATISFIES wexpr'
    p[0] = ['where', [
                p[2], [[p[3], p[5]]],
                ['expr', p[10], p[14]],
                p[16]
               ]
        ]

def p_whereclause_5(p):
    'whereclause : WHERE quantifier VARIABLE IN JSONLINES LPAREN INVERTEDCOMMA FILENAME INVERTEDCOMMA RPAREN DOT pathexpr SATISFIES wexpr'
    p[0] = ['where', [
                p[2], p[3], 
                [p[7], p[9]], 
                p[11]
            ]
        ]

########################################### quantifiers: SOME, EVERY
def p_quantifier_1(p):
    'quantifier : SOME'
    p[0] = p[1]

def p_quantifier_2(p):
    'quantifier : EVERY'
    p[0] = p[1]


########################################### where clause expressions
def p_wexpr_1(p):
    'wexpr : VARIABLE DOT pathexpr condition VARIABLE DOT pathexpr'
    p[0] = ['wexpr', [[p[1], p[3]], p[4], [p[5], p[7]]]]

def p_wexpr_2(p):
    'wexpr : VARIABLE DOT pathexpr condition STRING'
    p[0] = ['wexpr', [[p[1], p[3]], p[4], p[5]]]

def p_wexpr_5(p):
    'wexpr : VARIABLE condition STRING'
    p[0] = ['wexpr', [p[1], p[2], p[3]]]

def p_wexpr_3(p):
    'wexpr : VARIABLE DOT pathexpr condition NUMBER'
    p[0] = ['wexpr', [[p[1], p[3]], p[4], p[5]]]

def p_wexpr_4(p):
    'wexpr : CONTAINS LPAREN VARIABLE DOT pathexpr COMMA STRING RPAREN'
    p[0] = ['wexpr', [p[1], [p[3], p[5]], p[7]]]

########################################### conditions : EQUAL, NOTEQUAL, LESSTHANEQUAL, LESSTHAN, GREATERTHANEQUAL, GREATERTHAN
def p_condition_1(p):
    'condition : EQUAL'
    p[0] = p[1]
    
def p_condition_2(p):
    'condition : NOTEQUAL'
    p[0] = p[1]

def p_condition_3(p):
    'condition : GREATERTHANEQUAL'
    p[0] = p[1]

def p_condition_4(p):
    'condition : GREATERTHAN'
    p[0] = p[1]

def p_condition_5(p):
    'condition : LESSTHANEQUAL'
    p[0] = p[1]

def p_condition_6(p):
    'condition : LESSTHAN'
    p[0] = p[1]

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
for $question in json-lines("collection-faq.json").faqs[],
            $answer in json-lines("collection-answers.json").answers[]
        where contains($question.title, "MySQL")
        return
        {
            "question":$question.title,
            "answer_score":$answer.score
        };
        
'''

while True:
    try:
        # Use raw_input on Python 2
        res = parser.parse(inputdata)
        print('RES: ', res)
        break
    except EOFError:
        break
