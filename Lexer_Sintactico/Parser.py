import pandas as pd

class ParserLL1:
    def __init__(self, lista_tokens, tabla_ll1):
        self.tokens = lista_tokens  # Lista de diccionarios del Lexer
        self.tabla = tabla_ll1      # Matriz generada por el Módulo de Gramática
        self.pila = ["$", "P"]      # Pila: $ (fondo) y P (Símbolo inicial)
        self.posicion = 0           # Índice del token actual
        self.tabla_simbolos = {}    # Diccionario persistente de variables
        self.traza = []             # Registro para traza_analisis.txt
        self.hubo_error = False     # Bandera para el estado final

    def obtener_token_actual(self):
        if self.posicion < len(self.tokens):
            return self.tokens[self.posicion]
        # Si nos pasamos, devolvemos el símbolo de fin de cadena por seguridad
        return {'tipo': '$', 'valor': '$', 'linea': self.tokens[-1]['linea']}

    def modo_panico(self, esperado):
        self.hubo_error = True
        token_actual = self.obtener_token_actual()
        
        msg = f"Error Sintáctico en línea {token_actual['linea']}: Se esperaba {esperado}, se recibió {token_actual['tipo']} ({token_actual['valor']})\n"
        print(msg)
        self.traza.append(msg)

        # Símbolos de sincronización
        sincronizadores = ["SEMICOLON", "BEGIN", "END", "VAR", "PROGRAM"]
        
        # 1. Intentar saltar tokens hasta encontrar uno "seguro"
        encontrado = False
        while self.posicion < len(self.tokens):
            if self.tokens[self.posicion]['tipo'] in sincronizadores:
                # Si es un punto y coma, lo consumimos para intentar la siguiente instrucción
                if self.tokens[self.posicion]['tipo'] == "SEMICOLON":
                    self.posicion += 1
                encontrado = True
                break
            self.posicion += 1
        
        # 2. SI NO ENCONTRAMOS NADA, forzamos el avance para romper el bucle infinito
        if not encontrado or self.posicion >= len(self.tokens):
            self.posicion += 1 

        # 3. Limpiar la pila hasta encontrar un No Terminal de control
        # Quitamos elementos hasta que el tope sea algo que pueda reiniciar el análisis
        while len(self.pila) > 1:
            tope = self.pila[-1]
            if tope in ["S", "D", "B", "P", "$"]:
                break
            self.pila.pop()

    def validar_semantica(self, token):
        """
        Requisito: Cada ID debe guardarse en un diccionario.
        Si es declaración (VAR), verifica que no exista previamente.
        """
        nombre = token['valor']
        linea = token['linea']
        
        # Detectamos si estamos en la sección de declaraciones (Reglas D o L en la pila)
        es_declaracion = any(x in self.pila for x in ['L', "L'", 'D'])

        if es_declaracion:
            if nombre in self.tabla_simbolos:
                msg = f"Error Semántico en línea {linea}: La variable '{nombre}' ya fue declarada previamente.\n"
                print(msg)
                self.traza.append(msg)
                self.hubo_error = True
            else:
                # Guardar en la tabla de símbolos persistente
                self.tabla_simbolos[nombre] = {'tipo': 'IDENT', 'linea': linea, 'valor_inicial': None}
        else:
            # Validación extra: Uso de variable no declarada
            if nombre not in self.tabla_simbolos:
                msg = f"Error Semántico en línea {linea}: La variable '{nombre}' no ha sido declarada.\n"
                print(msg)
                self.traza.append(msg)
                self.hubo_error = True

    def analizar(self):
        print("\n--- INICIANDO ANÁLISIS SINTÁCTICO ---")
        
        while len(self.pila) > 0:
            tope = self.pila[-1]
            token_actual = self.obtener_token_actual()
            tipo_token = token_actual['tipo']
            
            # Registrar el paso actual en la traza
            self.traza.append(f"Pila: {self.pila} | Token Actual: {tipo_token}\n")

            # CASO 1: MATCH (Terminal en tope == Token en entrada)
            if tope == tipo_token:
                if tipo_token == "ID":
                    self.validar_semantica(token_actual)

                self.pila.pop()
                self.posicion += 1
                
                # Si llegamos al fin de cadena correctamente
                if tipo_token == "$":
                    if not self.hubo_error:
                        self.finalizar_exito()
                    else:
                        print("\n[AVISO] Análisis finalizado. Se encontraron errores en el código.")
                        self.guardar_traza()
                    return not self.hubo_error

            # CASO 2: NO TERMINAL (Buscar en la Tabla LL1)
            elif tope in self.tabla:
                if tipo_token in self.tabla[tope]:
                    produccion = self.tabla[tope][tipo_token]
                    self.pila.pop()
                    
                    # Si la producción no es épsilon ('e'), meter a la pila al revés
                    if produccion != ["e"]:
                        for simbolo in reversed(produccion):
                            self.pila.append(simbolo)
                else:
                    # No hay regla en la tabla: Modo Pánico
                    self.modo_panico(esperado=tope)
            
            # CASO 3: ERROR (El tope es un terminal que no coincide o símbolo inválido)
            # --- CASO 3: ERROR CRÍTICO ---
            else:
                self.modo_panico(esperado=tope)
                # SEGURIDAD: Si llegamos al fondo de la pila o de los tokens, terminamos
                if len(self.pila) <= 1 or self.posicion >= len(self.tokens):
                    break
            

        self.guardar_traza()
        return not self.hubo_error

    def finalizar_exito(self):
        print("Análisis sintáctico exitoso.")
        self.guardar_traza()

    def guardar_traza(self):
        with open("traza_analisis.txt", "w", encoding="utf-8") as f:
            f.writelines(self.traza)
        print("Archivo 'traza_analisis.txt' generado correctamente.")

# --- EXPLICACIÓN DEL FUNCIONAMIENTO ---
"""
1. ENTRADA: Recibe la lista de tokens del Lexer [{'tipo': 'PROGRAM', ...}] 
y la tabla M[NoTerminal, Terminal].

2. PROCESO DE LA PILA:
- Si el tope es un No Terminal (como P, D, B), busca en la TABLA LL(1).
- Sustituye el No Terminal por su producción en orden INVERSO.
- Si el tope es un Terminal (como ID, SEMICOLON), compara con el token del Lexer.

3. TRAZA: Cada movimiento de la pila se guarda en una lista que al final 
se escribe en un archivo .txt, como pide tu rúbrica.

4. TABLA DE SÍMBOLOS: Cada vez que hay un MATCH con un ID, se registra en 
un diccionario para uso posterior.
"""