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
    'POTENCIA',
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
    'STRING_DOBLE',
    'PARENTESIS_A',
    'PARENTESIS_B',
    'LLAVE_A',
    'LLAVE_B',
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
    'float',
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

#palabras reservadas que faltaron incluir
reservadas={
    
    'else':'else',
    'while':'while',
    'int':'int',
    'float':'float',
    'print':'print',
    'import':'import'
    
}

#modificamos la lista de tpkens para incluir las palabras resercvadas
tokens=tokens+list(reservadas.values())


t_ignore=' \t'

def t_COMENTARIO(t):
    r'//.*'
    pass  # No genera token, lo ignora completamente


# Expresiones regulares

t_SUMA=r'\+'
t_ASIGNACION=r'='
t_RESTA=r'\-'
t_DIVISION=r'/'
t_POTENCIA = r'\*\*'
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
t_LLAVE_B=r'\}'
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

#Para cadenas de texto con doble comillas

def t_STRING_DOBLE(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1] # Esto quita las comillas del valor final
    return t




# token para IF
def t_IF(t):
    r'IF'
    return t

# Identificadores o palabras reservadas 

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
    elif t.value == 'float':
        t.type = 'float'
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


def t_FMASMAS(t):
    r'i+'
    return t


# Función para atrapar el error 3x 
def t_ERROR_3X(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
    global errores_Desc
    errores_Desc.append(f"Error Léxico: Identificador inválido '{t.value}' en la línea {t.lexer.lineno}")
    #dejamos que el t_error se encargue o saltamos al siguiente espacio
    print(f"Modo panico:Saltando identificador invalido '{t.value}'")
    t.lexer.skip(len(t.value))#saltamos solo el inicio para que el modo panico busque el ';'

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
#Funcion de manejo de errores modicicando para que permita el modo panico
# Función de manejo de errores modificada (Modo Pánico Simple)
def t_error(t):
    # Reportamos el carácter que originó el fallo
    lexema_error = t.value[0]
    lista_errores_lexicos.append(f"Carácter ilegal '{lexema_error}' en línea {t.lineno}")
    print(f"Error Léxico: '{lexema_error}' en línea {t.lineno}. Sincronizando...")

    # Buscamos el siguiente punto de estabilidad
    delimitadores = [' ', '\t', '\n', ';', '{', '}', '(', ')']
    
    distancia = 0
    for char in t.value:
        if char in delimitadores:
            break
        distancia += 1
    
    # Si distancia es 0, significa que el error es el delimitador mismo (raro)
    # o que el error está pegado a uno. Saltamos al menos 1.
    salto = distancia if distancia > 0 else 1
    t.lexer.skip(salto)

# constructor del lexer

lexer=lex.lex()

def analisis(cadena):
    lexer.input(cadena)
    lista_tokens = []
    tabla_simbolos = {} # Diccionario para la tabla de símbolos
    lexer.lineno = 1
    
    for tok in lexer:
        # Calcular columna
        columna = tok.lexpos - cadena.rfind('\n', 0, tok.lexpos)
        
        # 1. Guardar en la lista de todos los tokens
        lista_tokens.append((tok.value, tok.type, tok.lineno, columna))
        
        # 2. Construir Tabla de Símbolos (Solo para Identificadores)
        # Según tu rúbrica: Lexema, Token (IDENT) y Línea de aparición.
        if tok.type == 'ID':
            # Solo se agrega si no existe para no repetir entradas
            if tok.value not in tabla_simbolos:
                tabla_simbolos[tok.value] = {
                    'Token': 'IDENT',
                    'Linea': tok.lineno
                }
        
    return lista_tokens, tabla_simbolos

# ejemplo de uso
""""""
if __name__=='__main__':
    codigo="""
    import math
    radio=5
    area=math.pi*radio**2
    print("El area del circulo es:",area)
    """
    codigo1 = """int suma = 10;
    float promedio// = suma / 2;
    if (promedio > 5) {
    resultado = promedio + 3x;
    }
    """

    

    # Análisis del primer código
    res_tokens, res_tabla = analisis(codigo)
    print("--- TOKENS CODIGO 0 ---")
    print(res_tokens)
    print("\n--- TABLA DE SIMBOLOS 0 ---")
    print(res_tabla)

    print("\n" + "="*50 + "\n")

    # Análisis del segundo código 
    res_tokens1, res_tabla1 = analisis(codigo1)
    print("--- TOKENS CODIGO 1 ---")
    for token in res_tokens1:
        print(token)
    
    print("\n--- TABLA DE SIMBOLOS 1---")
    print(res_tabla1)

    print("\n--- ERRORES 1 ---")
    print(errores_Desc)
