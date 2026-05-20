import collections

class AnalizadorGramatical:
    def __init__(self):
        self.gramatica = collections.OrderedDict()
        self.no_terminales = []
        self.terminales = set()
        self.primero = {}
        self.siguiente = {}
        self.simbolo_vacio = "e"  
        self.fin_cadena = "$"     

    def limpiar_datos(self):
        self.gramatica.clear()
        self.no_terminales.clear()
        self.terminales.clear()
        self.primero.clear()
        self.siguiente.clear()

    # --- EJEMPLOS PRECARGADOS ---
    def cargar_ejemplo_1(self):
        self.limpiar_datos()
        self.gramatica = {"A": [["id", "=", "E", ";"]], "E": [["id"], ["num"]]}
        self.no_terminales = ["A", "E"]
        print("\n[OK] Ejercicio 1: Asignación Simple cargado.")

    def cargar_ejemplo_2(self):
        self.limpiar_datos()
        self.gramatica = {
            "S": [["i", "c", "t", "S", "S'"], ["s"]],
            "S'": [["a", "S"], ["e"]] 
        }
        self.no_terminales = ["S", "S'"]
        print("\n[OK] Ejercicio 2: If-Then-Else cargado.")

    def cargar_ejemplo_3(self):
        self.limpiar_datos()
        self.gramatica = {
            "S": [["A", "B", "C"]],
            "A": [["pub"], ["put"], ["e"]],
            "B": [["static"], ["e"]],
            "C": [["final"]]
        }
        self.no_terminales = ["S", "A", "B", "C"]
        print("\n[OK] Ejercicio 3: Acumulación cargado.")

    def identificar_terminales(self):
        self.terminales.clear()
        for prods in self.gramatica.values():
            for p in prods:
                for token in p:
                    if token not in self.gramatica and token != self.simbolo_vacio:
                        self.terminales.add(token)

    def mostrar_resumen_gramatica(self):
        """Imprime la estructura de la gramática de forma organizada"""
        print("\n" + "="*50)
        print("      ESTRUCTURA DE LA GRAMÁTICA")
        print("="*50)
        print("\nReglas de Producción:")
        contador = 1
        for nt in self.no_terminales:
            for prod in self.gramatica[nt]:
                print(f"  {contador}. {nt} -> {' '.join(prod)}")
                contador += 1
        self.identificar_terminales()
        print(f"\nNo Terminales: {{ {', '.join(self.no_terminales)} }}")
        print(f"Terminales:    {{ {', '.join(sorted(list(self.terminales)))} }}")
        print(f"E. Inicial:    {self.no_terminales[0]}")
        print("-" * 50)

    def validar_gramatica(self):
        """Valida recursión izquierda y símbolos no definidos"""
        for nt, producciones in self.gramatica.items():
            for prod in producciones:
                # Validar recursión izquierda inmediata
                if prod[0] == nt:
                    print(f"\n[ERROR] Recursión izquierda detectada en: {nt}")
                    return False
                # Validar símbolos no definidos (Huérfanos)
                for token in prod:
                    if token[0].isupper() and token != self.simbolo_vacio:
                        if token not in self.gramatica:
                            print(f"\n[ERROR DE DEFINICIÓN] El No Terminal '{token}' no tiene producción.")
                            return False
        return True

    def calcular_conjuntos(self):
        """Bucle de estabilidad para obtener conjuntos Primero y Siguiente"""
        self.primero = {nt: set() for nt in self.no_terminales}
        self.siguiente = {nt: set() for nt in self.no_terminales}
        self.siguiente[self.no_terminales[0]].add(self.fin_cadena)

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

    def mostrar_tablas_finales(self):
        """Impresión con anchos corregidos para una visualización clara"""
        print("\n" + "-" * 85)
        print(f"{'No Terminal':<15} | {'Conjunto Primero':<30} | {'Conjunto Siguiente':<30}")
        print("-" * 85)
        
        t_prim, t_sig = set(), set()
        
        for nt in self.no_terminales:
            p = sorted(list(self.primero[nt]))
            s = sorted(list(self.siguiente[nt]))
            t_prim.update(p); t_sig.update(s)
            
            p_str = "{" + ", ".join(p) + "}"
            s_str = "{" + ", ".join(s) + "}"
            
            print(f"{nt:<15} | {p_str:<30} | {s_str:<30}")
        
        print("\n--- Conjuntos Totales (Unión de Todos los Conjuntos) ---")
        print(f"Total Primero:   {{ {', '.join(sorted(list(t_prim)))} }}")
        print(f"Total Siguiente: {{ {', '.join(sorted(list(t_sig)))} }}")

def menu():
    app = AnalizadorGramatical()
    while True:
        print("\nPRIMERO Y SIGUIENTE")
        print("======================")
        print("1. Ver Ejemplos Precargados")
        print("2. Entrada Manual")
        print("3. Salir")
        print("======================")
        print("\nNotas:")
        print("1.- Epsilon se representa exclusivamente con el símbolo 'e'.")
        print("2.- No se permite recursión por la izquierda (error crítico).")
        print("3.- Símbolos No Terminales sin producción propia serán marcados como error.")
        print("-" * 20)
        
        op = input("Selección: ")
        
        if op == "1":
            print("\n--- Seleccione Ejercicio ---")
            print("a. Asignación Simple (A -> id = E ;)")
            print("b. If-Then-Else (S -> i c t S S')")
            print("c. Acumulación (S -> A B C)")
            sub_op = input("Opción: ").lower()
            if sub_op == "a": app.cargar_ejemplo_1()
            elif sub_op == "b": app.cargar_ejemplo_2()
            elif sub_op == "c": app.cargar_ejemplo_3()
            else: continue
            
        elif op == "2":
            app.limpiar_datos()
            print("\nIngrese las reglas con el formato: NT -> prod1 prod2 | prod3")
            print("Para procesar y ver resultados, escriba 'FIN'.")
            while True:
                linea = input("> ")
                if linea.upper() == "FIN": break
                if "->" not in linea: continue
                
                izq, der = linea.split("->")
                nt = izq.strip()
                prods = [p.strip().split() for p in der.split("|")]
                
                if nt not in app.gramatica:
                    app.gramatica[nt] = []
                    app.no_terminales.append(nt)
                app.gramatica[nt].extend(prods)
                
        elif op == "3": 
            print("Saliendo del programa...")
            break
        else: 
            print("Opción no válida.")
            continue

        if app.validar_gramatica():
            app.mostrar_resumen_gramatica()
            app.calcular_conjuntos()
            app.mostrar_tablas_finales()

if __name__ == "__main__":
    menu()