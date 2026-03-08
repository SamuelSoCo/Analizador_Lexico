import re

# 1. Definición de los patrones de Tokens usando Regex
# El orden importa: primero las más específicas (reales) antes que las generales (enteros)
TOKEN_PATTERNS = [
    ('RESERVADA', r'\b(int|float|if|else|while)\b'),
    ('REAL',      r'\d+\.\d+'),
    ('ENTERO',    r'\d+'),
    ('IDENT',     r'[a-zA-Z][a-zA-Z0-9]*'),
    ('OPERADOR',  r'[+\-*/=><]'),
    ('DELIM',     r'[;(){}]'),
    ('ESPACIO',   r'[ \t]+'),
    ('NUEVA_LINEA', r'\n'),
    ('ERROR',     r'.'), # Cualquier otro carácter es un error
]

# Unimos todos los patrones en una sola expresión regular "maestra"
regex_maestra = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_PATTERNS)

def lexer(codigo_fuente):
    tokens_encontrados = []
    tabla_simbolos = {} # Diccionario para evitar duplicados
    linea_actual = 1
    
    # re.finditer recorre el texto buscando coincidencias con nuestra regex maestra
    for match in re.finditer(regex_maestra, codigo_fuente):
        tipo = match.lastgroup
        lexema = match.group(tipo)
        
        if tipo == 'ESPACIO':
            continue
        elif tipo == 'NUEVA_LINEA':
            linea_actual += 1
            continue
        elif tipo == 'ERROR':
            print(f">>> ERROR LÉXICO: Carácter '{lexema}' no válido en línea {linea_actual}")
            continue
            
        # Validación especial para el caso "3x" (Número pegado a Letra)
        if tipo in ['ENTERO', 'REAL']:
            # Verificamos si lo que sigue inmediatamente es una letra
            pos_final = match.end()
            if pos_final < len(codigo_fuente) and codigo_fuente[pos_final].isalpha():
                print(f">>> ERROR LÉXICO: Formato de número inválido '{lexema}{codigo_fuente[pos_final]}' en línea {linea_actual}")
                continue

        # Guardar en la lista de tokens (Salida 1)
        tokens_encontrados.append((lexema, tipo, linea_actual))
        
        # Guardar en la Tabla de Símbolos (Salida 2) - Solo si es Identificador
        if tipo == 'IDENT':
            if lexema not in tabla_simbolos:
                tabla_simbolos[lexema] = {"token": "IDENT", "linea": linea_actual}

    return tokens_encontrados, tabla_simbolos

# --- PRUEBA OBLIGATORIA ---
codigo = """int suma = 10;
float promedio = suma / 2;
if (promedio > 5) {
    resultado = promedio + 3x;
}"""

lista_tokens, tabla = lexer(codigo)

# Mostrar resultados
print("\n--- LISTA DE TOKENS ---")
print(f"{'Lexema':<15} | {'Token':<12} | {'Línea'}")
for l, t, n in lista_tokens:
    print(f"{l:<15} | {t:<12} | {n}")

print("\n--- TABLA DE SÍMBOLOS ---")
print(f"{'Lexema':<15} | {'Token':<12} | {'Línea'}")
for lex, info in tabla.items():
    print(f"{lex:<15} | {info['token']:<12} | {info['linea']}")