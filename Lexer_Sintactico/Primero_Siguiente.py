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

    def cargar_ejemplo_asignacion(self):
        """Carga: A -> id = E ; | E -> id | E -> num"""
        self.limpiar_datos()
        self.gramatica = {
            "A": [["id", "=", "E", ";"]],
            "E": [["id"], ["num"]]
        }
        self.no_terminales = ["A", "E"]
        print("\n--> Ejemplo 'Asignación Simple' cargado.")

    def identificar_terminales(self):
        self.terminales.clear()
        for prods in self.gramatica.values():
            for p in prods:
                for token in p:
                    if token not in self.gramatica and token != self.simbolo_vacio:
                        self.terminales.add(token)

    def mostrar_resumen_gramatica(self):
        """Imprime la estructura de la gramática como en la diapositiva[cite: 2]"""
        print("\n" + "="*40)
        print("      ESTRUCTURA DE LA GRAMÁTICA")
        print("="*40)
        
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
        print("-" * 40)

    def validar_gramatica(self):
        """Validación de recursión izquierda y símbolos huérfanos[cite: 1]"""
        for nt, producciones in self.gramatica.items():
            for prod in producciones:
                if prod[0] == nt:
                    print(f"\n[ERROR] Recursión izquierda detectada en: {nt}")
                    return False
                for token in prod:
                    if token[0].isupper() and token != self.simbolo_vacio and token not in self.gramatica:
                        print(f"\n[ERROR] No Terminal '{token}' no definido.")
                        return False
        return True

    def calcular_conjuntos(self):
        """Algoritmo de estabilidad para Primero y Siguiente[cite: 1, 3]"""
        self.primero = {nt: set() for nt in self.no_terminales}
        self.siguiente = {nt: set() for nt in self.no_terminales}
        self.siguiente[self.no_terminales[0]].add(self.fin_cadena)

        while True:
            antes = str(self.primero) + str(self.siguiente)
            for nt in self.no_terminales:
                for produccion in self.gramatica[nt]:
                    # --- CÁLCULO DE PRIMERO ---
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
                    
                    # --- CÁLCULO DE SIGUIENTE ---
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
        """Impresión corregida con columnas alineadas"""
        print("\n" + "-" * 75)
        # Ajustamos el espaciado para que no se pierdan las columnas
        print(f"{'No Terminal':<15} | {'Conjunto Primero':<25} | {'Conjunto Siguiente':<25}")
        print("-" * 75)
        
        t_prim = set()
        t_sig = set()
        
        for nt in self.no_terminales:
            p = sorted(list(self.primero[nt]))
            s = sorted(list(self.siguiente[nt]))
            t_prim.update(p)
            t_sig.update(s)
            
            p_str = "{" + ", ".join(p) + "}"
            s_str = "{" + ", ".join(s) + "}"
            # Usamos anchos fijos para que todo quede en su columna
            print(f"{nt:<15} | {p_str:<25} | {s_str:<25}")
        
        print("\n--- Conjuntos Totales (Unión de todos los símbolos) ---")
        print(f"Total Primero:   {{ {', '.join(sorted(list(t_prim)))} }}")
        print(f"Total Siguiente: {{ {', '.join(sorted(list(t_sig)))} }}")

def menu():
    app = AnalizadorGramatical()
    while True:
        print("========================\n1. Ejemplo Precargado (Asignación) \n2. Entrada Manual \n3. Salir\n========================")
        op = input("Selección: \n>")
        if op == "1": app.cargar_ejemplo_asignacion()
        elif op == "2":
            app.limpiar_datos()
            print("Formato: NT -> prod1 prod2 | prod3. Escribe 'FIN' para procesar.")
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
        elif op == "3": break
        else: continue

        if app.validar_gramatica():
            app.mostrar_resumen_gramatica()
            app.calcular_conjuntos()
            app.mostrar_tablas_finales()

if __name__ == "__main__":
    menu()