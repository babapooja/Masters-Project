import ply.lex as lex
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


# Tokens

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


def t_STRING(t):
    r'"(?:\\.|[^"\\])*"'
    t.value = t.value.strip('"')
    return t


def t_JSONLINES(t):
    r'json-lines'
    t.value = 'json-lines'
    return t


def t_FOR(t):
    r'[fF][oO][rR]'
    t.value = 'for'
    return t


def t_IN(t):
    r'[iI][nN]'
    t.value = 'in'
    return t


def t_WHERE(t):
    r'[wW][hH][eE][rR][eE]'
    t.value = 'where'
    return t

def t_AND(t):
    r'[aA][nN][dD]'
    t.value = 'and'
    return t


def t_RETURN(t):
    r'[rR][eE][tT][uU][rR][nN]'
    t.value = 'return'
    return t


def t_EQUAL(t):
    r'[eE][qQ]'
    t.value = 'eq'
    return t


def t_NOTEQUAL(t):
    r'[nN][eE]'
    t.value = 'ne'
    return t


def t_GREATEREQUAL(t):
    r'[gG][eE]'
    t.value = 'ge'
    return t


def t_GREATERTHAN(t):
    r'[gG][tT]'
    t.value = 'gt'
    return t


def t_LESSEQUAL(t):
    r'[lL][eE]'
    t.value = 'le'
    return t


def t_LESSTHAN(t):
    r'[lL][tT]'
    t.value = 'lt'
    return t


def t_CONTAINS(t):
    r'[cC][oO][nN][tT][aA][iI][nN][sS]'
    t.value = 'contains'
    return t


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


t_ignore = " \r\n\t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
