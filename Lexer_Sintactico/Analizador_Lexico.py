#Analizador Lexico

"""Para el analizador lexico se usara la libreria PLY(Python Lex-Yacc) la cual es una biblioteca para los analizadores lexicos y sintacticos
PLY es una herramienta para analisis lexico y sintactico que se usan en lenguajes como C"""

import ply.lex as lex

lista_errores_lexicos=[]
errores_Desc=[]

#tokens que utilizaremos para el analizador lexico

tokens=[
    'ID',
    'NUMERO',
    'REAL',
    'SUMA',
    'ASIGNACION',
    'RESTA',
    'DIVISION',
    'MULTIPLICACION',
    'IGUAL',
    'DIFERENTE',
    'MAYORQUE',
    'MENORQUE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'PUNTO',
    'COMA',
    'DOSPUNTOS',
    'PUNTOCOMA',
    'COMILLASSIMPLES',
    'COMILLADOBLE',
    'PARENTESIS_A',
    'PARENTESIS_B',
    'LLAVE_A',
    'LLAVE_C',
    'CORCHETE_A',
    'CORCHETE_B',
    'MASMAS',
    'MENOSMENOS',
    'AND',
    'OR',
    'NOT',
    'CADENA',
    'BEGIN',
    'END',
    'True',
    'False',
    'IMPORT',
    'FUN',
    'FROM',
    'WHILE',
    'FOR',
    'IF',
    'ELSE',
    'RETURN',
    'DESTROY',
    'ONOFF',
    'SMS',
    'DSEN',
    'DLED',
    'GVS',
    'real',
    'int',
    'bool',
    'stg',
    'moveTo',
    'glassPosition',
    'gateOpen',
    'CO',
    'CA',
    'compuerta',
    'cons'
]

t_ignore=' \t'

# Expresiones regulares

t_SUMA=r'\+'
t_ASIGNACION=r'='
t_RESTA=r'\-'
t_DIVISION=r'/'
t_MULTIPLICACION=r'\*'
t_IGUAL=r'=='
t_DIFERENTE=r'!='
t_MAYORQUE=r'>'
t_MENORQUE=r'<'
t_MENORIGUAL=r'<='
t_MAYORIGUAL=r'>='
t_PUNTO=r'\.'
t_COMA=r'\,'
t_DOSPUNTOS=r'\:'
t_PUNTOCOMA=r'\;'
t_COMILLASSIMPLES=r'\''
t_COMILLADOBLE=r'\"'
t_PARENTESIS_A=r'\('
t_PARENTESIS_B=r'\)'
t_LLAVE_A=r'\{'
t_LLAVE_C=r'\}'
t_CORCHETE_A=r'\['
t_CORCHETE_B=r'\]'
t_MASMAS=r'\+\+'
t_MENOSMENOS=r'\-\-'
t_AND=r'\&\&'
t_OR=r'\|\|'
t_NOT=r'\!'

contador=0

def t_SALTOLINEA(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_CADENA(t):
    r'\#.*?\#'
    t.type='CADENA'
    return t

# token para IF
def t_IF(t):
    r'IF'
    return t

# Identificadores

def t_IDENTIFICADORES(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    if t.value=='BEGIN':
        t.type='BEGIN'
    elif t.value=='END':
        t.type='END'
    elif t.value=='FOR':
        t.type='FOR'
    elif t.value=='WHILE':
        t.type='WHILE'
    elif t.value=='ELSE':
        t.type='ELSE'
    elif t.value=='int':
        t.type='int'
    elif t.value=='real':
        t.type='real'
    elif t.value=='bool':
        t.type='bool'
    elif t.value=='stg':
        t.type='stg'
    elif t.value=='SMS':
        t.type='SMS'
    elif t.value=='FUN':
        t.type='FUN'
    elif t.value=='True':
        t.type='True'
    elif t.value=='False':
        t.type='False'
    elif t.value=='CO':
        t.type='CO'
    elif t.value=='CA':
        t.type='CA'
    elif t.value=='moveTo':
        t.type='moveTo'
    elif t.value=='glassPosition':
        t.type='glassPosition'
    elif t.value=='gateOpen':
        t.type='gateOpen'
    elif t.value=='compuerta':
        t.type='compuerta'
    elif t.value=='cons':
        t.type='cons'
    else:
        t.type='ID'
        
    return t

# Comentarios

def t_COMENTARIO(t):
    r'\/\/(.*?)\/\/'
    return t

def t_FMASMAS(t):
    r'i+'
    return t

# Numeros

def t_REAL(t):
    r'(\d+\.\d+|\.\d+)'
    t.value=float(t.value)
    return t

def t_NUMERO(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_TRUE(t):
    r'TRUE'
    return t

def t_FALSE(t):
    r'FALSE'
    return t

# Manejo de errores

def t_error(t):
    global errores_Desc
    errores_Desc.append(f"Simbolo no valido '{t.value[0]}' en la linea {t.lexer.lineno}")
    t.lexer.skip(1)

# constructor del lexer

lexer=lex.lex()

def analisis(cadena):
    lexer.input(cadena)
    tokens=[]
    lexer.lineno=1
    
    for tok in lexer:
        columna=tok.lexpos - cadena.rfind('\n',0,tok.lexpos)
        tokens.append((tok.value, tok.type, tok.lineno, columna))
        
    return tokens

# ejemplo de uso

if __name__=='__main__':
    codigo="""
    import math
    radio=5
    area=math.pi*radio**2
    print("El area del circulo es:",area)
    """
    #impresion de la lista de los tokens obtenidos del analisis lexico
    print(analisis(codigo))
    print("\n")
    #impresion de la lista por token
    for token in analisis(codigo):
        print(token)
    