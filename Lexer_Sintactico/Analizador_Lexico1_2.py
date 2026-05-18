import ply.lex as lex

# 1. LISTA DE TOKENS EXTENDIDA
# Incluye los obligatorios para el Parser y los extras que solicitaste.
tokens = [
    'ID', 'NUM', 'SEMICOLON', 'COLON', 'ASSIGN', 
    'PLUS', 'MULT', 'LPAREN', 'RPAREN',
    'MINUS', 'DIV', 'IGUAL', 'DIFERENTE', 'PUNTO', 'COMA',
    'COMILLA_S', 'COMILLA_D', 'MAYOR', 'MENOR', 'CADENA'
]

# 2. PALABRAS RESERVADAS (Diccionario para búsqueda rápida)
reservadas = {
    'PROGRAM': 'PROGRAM',
    'VAR': 'VAR',
    'INT': 'INT',
    'FLOAT': 'FLOAT',
    'BEGIN': 'BEGIN',
    'END': 'END',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'true': 'TRUE',
    'false': 'FALSE',
    'import': 'IMPORT',
    'fun': 'FUN',
    'destroy': 'DESTROY'
}

# Unimos tokens con palabras reservadas
tokens = tokens + list(reservadas.values())

# 3. EXPRESIONES REGULARES SIMPLES
t_SEMICOLON = r'\;'
t_COLON     = r'\:'
t_ASSIGN    = r'='
t_PLUS      = r'\+'
t_MINUS     = r'\-'
t_MULT      = r'\*'
t_DIV       = r'\/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_PUNTO     = r'\.'
t_COMA      = r'\,'
t_COMILLA_S = r'\''
t_COMILLA_D = r'\"'
t_MAYOR     = r'>'
t_MENOR     = r'<'

t_ignore = ' \t'

# 4. FUNCIONES PARA TOKENS COMPLEJOS Y ERRORES

def t_COMENTARIO(t):
    r'//.*'
    pass # Ignora el comentario y no genera token, resolviendo tu duda de estabilidad.

def t_CADENA(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1] # Quita las comillas del valor
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Prioridad: Si el lexema está en reservadas, usa ese tipo; si no, es ID.
    t.type = reservadas.get(t.value, 'ID') 
    return t

def t_NUM(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# 5. MODO PÁNICO: Manejo de Errores Léxicos
def t_error(t):
    # Detecta el carácter ilegal y lo reporta.
    print(f"ERROR LÉXICO: Carácter '{t.value[0]}' ilegal en línea {t.lineno}")
    
    # Lógica de sincronización (Modo Pánico):
    # Salta hasta encontrar un delimitador para intentar seguir con el resto.
    delimitadores = [' ', '\t', '\n', ';', '{', '}', '(', ')']
    distancia = 0
    for char in t.value:
        if char in delimitadores:
            break
        distancia += 1
    
    salto = distancia if distancia > 0 else 1
    t.lexer.skip(salto)

# 6. CONSTRUCTOR Y GENERADOR DE OBJETOS
lexer = lex.lex()

def generar_lista_tokens(codigo):
    """
    Genera la lista de diccionarios que el Módulo Sintáctico requiere.
    """
    lexer.input(codigo)
    lista_tokens = []
    lexer.lineno = 1
    
    while True:
        tok = lexer.token()
        if not tok:
            break  
        
        # Estructura de objeto exigida por la rúbrica.
        lista_tokens.append({
            'tipo': tok.type,
            'valor': tok.value,
            'linea': tok.lineno
        })
    
    # Símbolo de fin de cadena para el algoritmo de la pila.
    lista_tokens.append({'tipo': '$', 'valor': '$', 'linea': lexer.lineno})
    return lista_tokens

# --- PRUEBA DEL LEXER ---
if __name__ == '__main__':
    codigo_sucio = """
    import miLibreria;
    PROGRAM test;
    VAR x: INT;
    BEGIN
        x = 10 @ + 5; // El @ debería ser ignorado por el modo pánico
        y = "Hola mundo";
    END
    """
    codigo_limpio = """
    import miLibreria;
    PROGRAM test;
    VAR x: INT;
    BEGIN
        x = 10  + 5; 
        y = "Hola mundo";
    END
    """
    
    tokens_finales = generar_lista_tokens(codigo_sucio)
    print("\n--- RESULTADO DEL ANÁLISIS LÉXICO ---")
    for t in tokens_finales:
        print(t)
        
    
    print("\n"+"-"*40)
    print("\n--- CÓDIGOS DE PRUEBA LIMPIO ---")
    tokens_finales1=generar_lista_tokens(codigo_limpio)
    print("\n--- RESULTADO DEL ANÁLISIS LÉXICO ---")
    for t in tokens_finales1:
        print(t)