# Importamos las funciones y clases de los 3 archivos anteriores
from Analizador_Lexico1_2 import generar_lista_tokens
from Tabla_ll1 import GeneradorTablas
from Parser import ParserLL1

"""Integracion de las 3 etapas del compilador
Actua como el punto centralizado importando los tres componentes principales: el Analizador Léxico, el Generador de Tablas LL(1) y el Parser Sintáctico
1. El Analizador Léxico procesa el código fuente y produce una lista de tokens.
2. El Generador de Tablas LL(1) construye la tabla de predicción    basada en la gramática definida.
3. El Parser Sintáctico utiliza la lista de tokens y la tabla para validar la estructura"""




def ejecutar_compilador(codigo_fuente, nombre_prueba):
    print(f"\n{'='*20} PROBANDO: {nombre_prueba} {'='*20}")
    
    # PASO 1: Análisis Léxico
    # El Texto plano es procesado por el  Lexer convierte el texto en una lista de diccionarios (objetos token)
    print("\n[PASO 1] Ejecutando Analizador Léxico\n")
    tokens = generar_lista_tokens(codigo_fuente)
    for t in tokens:
        print(f"  {t}")

    # PASO 2: Generación de Tabla LL(1)
    # El generador calcula Primero/Siguiente y crea la matriz de decisiones 
    print("\n[PASO 2] Generando Tabla LL(1)\n")
    gen = GeneradorTablas()
    gen.cargar_gramatica_proyecto()
    gen.calcular_conjuntos()
    tabla = gen.construir_tabla_ll1()
    gen.mostrar_tabla_formateada()

    # PASO 3: Análisis Sintáctico (Parser de Pila)
    # Usamos lo resultados de la etapa lexica y la tabla ,El Parser usa los tokens y la tabla para validar la estructura
    print("\n[PASO 3] Ejecutando Parser Sintáctico\n")
    parser = ParserLL1(tokens, tabla)
    resultado = parser.analizar()

    if resultado:
        print(f"\n[RESULTADO] {nombre_prueba}: EXITOSO (valido según la gramática).")
    else:
        print(f"\n[RESULTADO] {nombre_prueba}: FALLIDO )no válido según la gramática,hay que revisar los errores reportados).")

# --- BLOQUE DE PRUEBAS ---

# 1. Caso de Éxito,el codigo cumple con la gramatica definida, no tiene errores lexicos ni sintacticos, el parser logra procesarlo completamente y se reporta un analisis exitoso
codigo_exito = """
PROGRAM miPrograma;
VAR
    x: INT;
    y: FLOAT;
BEGIN
    x = 10;
    y = x + 5;
END
"""

# 2. Caso de error, con errores sintacticos,como punto y coma faltante, operador sin operando, el parser detecta el error, reporta un mensaje claro con la linea y el token problemático, y luego intenta recuperarse para seguir analizando el resto del codigo y encontrar mas errores si los hay
#asi como el error de suma huerfano sin un operando del lado derecho, activando el modo panico
codigo_error = """
PROGRAM errorPrograma; 
VAR 
x: INT 
BEGIN 
x = 5 + ;
END
"""

if __name__ == "__main__":
    
    print(f"Codigo de prueba 1:\n{codigo_exito}")
    # Ejecutamos la prueba exitosa
    ejecutar_compilador(codigo_exito, "CÓDIGO CORRECTO")
    
    print("\n" + "="*60 + "\n")
    print(f"Codigo de prueba 2:\n{codigo_error}")
    # Ejecutamos la prueba con error
    ejecutar_compilador(codigo_error, "CÓDIGO CON ERROR")