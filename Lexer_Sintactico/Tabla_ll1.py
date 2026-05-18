import collections

class GeneradorTablas:
    def __init__(self):
        self.gramatica = collections.OrderedDict()
        self.no_terminales = []
        self.terminales = set()
        self.primero = {}
        self.siguiente = {}
        self.tabla_ll1 = {}
        self.simbolo_vacio = "e"
        self.fin_cadena = "$"

    def cargar_gramatica_proyecto(self):
        """Carga la gramática oficial con los tokens del Lexer"""
        self.gramatica = {
            "P": [["PROGRAM", "ID", "SEMICOLON", "D", "B"]],
            "D": [["VAR", "L"], ["e"]],
            "L": [["ID", "COLON", "T", "SEMICOLON", "L'"]],
            "L'": [["L"], ["e"]],
            "T": [["INT"], ["FLOAT"]],
            "B": [["BEGIN", "S", "END"]],
            "S": [["ID", "ASSIGN", "E", "SEMICOLON", "S'"]],
            "S'": [["S"], ["e"]],
            "E": [["F", "E'"]],
            "E'": [["PLUS", "F", "E'"], ["e"]],
            "F": [["ID"], ["NUM"]]
        }
        self.no_terminales = list(self.gramatica.keys())
        self.identificar_terminales()

    def identificar_terminales(self):
        self.terminales = set()
        for producciones in self.gramatica.values():
            for prod in producciones:
                for simbolo in prod:
                    if simbolo not in self.gramatica and simbolo != self.simbolo_vacio:
                        self.terminales.add(simbolo)

    def calcular_conjuntos(self):
        """Aquí insertamos tu lógica de estabilidad"""
        self.primero = {nt: set() for nt in self.no_terminales}
        self.siguiente = {nt: set() for nt in self.no_terminales}
        self.siguiente[self.no_terminales[0]].add(self.fin_cadena)

        # --- TU LÓGICA DE ESTABILIDAD ---
        while True:
            antes = str(self.primero) + str(self.siguiente)
            for nt in self.no_terminales:
                for produccion in self.gramatica[nt]:
                    # --- LÓGICA DE PRIMERO ---
                    for i, token in enumerate(produccion):
                        if token not in self.gramatica or token == self.simbolo_vacio:
                            self.primero[nt].add(token)
                            break
                        else:
                            self.primero[nt].update(self.primero[token] - {self.simbolo_vacio})
                            if self.simbolo_vacio not in self.primero[token]:
                                break
                            if i == len(produccion) - 1:
                                self.primero[nt].add(self.simbolo_vacio)
                    
                    # --- LÓGICA DE SIGUIENTE ---
                    for i, token in enumerate(produccion):
                        if token in self.gramatica:
                            limite = False
                            for j in range(i + 1, len(produccion)):
                                sig_token = produccion[j]
                                if sig_token not in self.gramatica:
                                    self.siguiente[token].add(sig_token)
                                    limite = True
                                    break
                                else:
                                    self.siguiente[token].update(self.primero[sig_token] - {self.simbolo_vacio})
                                    if self.simbolo_vacio not in self.primero[sig_token]:
                                        limite = True
                                        break
                            if not limite:
                                self.siguiente[token].update(self.siguiente[nt])
            
            if antes == (str(self.primero) + str(self.siguiente)):
                break

    def obtener_primero_produccion(self, produccion):
        """Calcula el Primero de una regla específica"""
        res = set()
        for simbolo in produccion:
            if simbolo == self.simbolo_vacio:
                res.add(self.simbolo_vacio)
                break
            if simbolo not in self.gramatica:
                res.add(simbolo)
                break
            else:
                res.update(self.primero[simbolo] - {self.simbolo_vacio})
                if self.simbolo_vacio not in self.primero[simbolo]:
                    break
        else:
            res.add(self.simbolo_vacio)
        return res

    def construir_tabla_ll1(self):
        """Crea el manual de decisiones para el Parser"""
        self.tabla_ll1 = {nt: {} for nt in self.no_terminales}
        
        for nt in self.no_terminales:
            for produccion in self.gramatica[nt]:
                prim_prod = self.obtener_primero_produccion(produccion)
                
                # Regla 1: Por cada terminal en Primero de la regla
                for token in prim_prod:
                    if token != self.simbolo_vacio:
                        self.tabla_ll1[nt][token] = produccion
                
                # Regla 2: Si la regla produce épsilon, mirar Siguiente
                if self.simbolo_vacio in prim_prod:
                    for token_sig in self.siguiente[nt]:
                        self.tabla_ll1[nt][token_sig] = produccion
        return self.tabla_ll1

    def mostrar_tabla_formateada(self):
        """Muestra la tabla para verificar que esté lista para el Parser"""
        print("\n--- TABLA DE PREDICCIÓN LL(1) ---")
        for nt, reglas in self.tabla_ll1.items():
            for token, prod in reglas.items():
                print(f"M[{nt}, {token}] = {prod}")

# --- FLUJO DE EJECUCIÓN ---
if __name__ == "__main__":
    generador = GeneradorTablas()
    generador.cargar_gramatica_proyecto()
    generador.calcular_conjuntos()
    generador.construir_tabla_ll1()
    generador.mostrar_tabla_formateada()