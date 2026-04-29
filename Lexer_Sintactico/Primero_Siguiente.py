import collections

# Estructura para almacenar la gramática y los conjuntos
class AnalizadorGramatical:
    def __init__(self):
        self.gramatica = collections.OrderedDict()
        self.no_terminales = []
        self.terminales = set()
        self.primero = {}
        self.siguiente = {}
        self.simbolo_vacio = "e"  # Representa epsilon (EPS)
        self.fin_cadena = "$"     # Representa el final de la cadena

    def limpiar_datos(self):
        self.gramatica.clear()
        self.no_terminales.clear()
        self.terminales.clear()
        self.primero.clear()
        self.siguiente.clear()

    def cargar_ejemplo_asignacion(self):
        """Carga el ejemplo: A -> id = E ; | E -> id | E -> num"""
        self.limpiar_datos()
        # Formato: Lista de listas para manejar tokens como 'id' o '='
        self.gramatica = {
            "A": [["id", "=", "E", ";"]],
            "E": [["id"], ["num"]]
        }
        self.no_terminales = ["A", "E"]
        print("\n--> Ejemplo 'Asignación Simple' cargado con éxito.")

    def es_terminal(self, token):
        """Regla: Es terminal si empieza con minúscula o es símbolo, 
        y no es un No Terminal definido."""
        return not (token[0].isupper()) or token == self.simbolo_vacio

    def validar_recursion_izquierda(self):
        """REGLA: Si A -> A ..., el programa no debe continuar."""
        for nt, producciones in self.gramatica.items():
            for prod in producciones:
                if prod[0] == nt:
                    print(f"\n[ERROR CRÍTICO] Recursión izquierda detectada: {nt} -> {' '.join(prod)}")
                    return False
        return True

    def validar_huerfanos(self):
        """REGLA: Si un No Terminal aparece a la derecha pero no tiene producción."""
        for prods in self.gramatica.values():
            for p in prods:
                for token in p:
                    if token[0].isupper() and token != self.simbolo_vacio:
                        if token not in self.gramatica:
                            print(f"\n[ERROR] Símbolo No Terminal '{token}' no definido en la gramática.")
                            return False
        return True

    def calcular_conjuntos(self):
        """Bucle de Estabilidad para Primero y Siguiente."""
        # Inicialización de mapas de conjuntos vacíos
        self.primero = {nt: set() for nt in self.no_terminales}
        self.siguiente = {nt: set() for nt in self.no_terminales}
        
        # Regla 1 de Siguiente: El símbolo inicial siempre lleva $
        self.siguiente[self.no_terminales[0]].add(self.fin_cadena)

        estabilizado = False
        while not estabilizado:
            estabilizado = True
            
            # Guardamos estado actual para comparar cambios (Estabilidad)
            estado_anterior = str(self.primero) + str(self.siguiente)

            for nt in self.no_terminales:
                for produccion in self.gramatica[nt]:
                    
                    # --- LÓGICA DE PRIMERO ---
                    # Revisamos la producción de izquierda a derecha (Acumulación)
                    for i, token in enumerate(produccion):
                        if self.es_terminal(token):
                            self.primero[nt].add(token)
                            break # Si es terminal, aquí termina el Primero de esta regla
                        else:
                            # Si es No Terminal, heredamos sus Primeros (excepto epsilon)
                            self.primero[nt].update(self.primero[token] - {self.simbolo_vacio})
                            # Solo si el No Terminal tiene epsilon, pasamos al siguiente token
                            if self.simbolo_vacio not in self.primero[token]:
                                break
                            # Si llegamos al final y todos tuvieron epsilon, el padre tiene epsilon
                            if i == len(produccion) - 1:
                                self.primero[nt].add(self.simbolo_vacio)

                    # --- LÓGICA DE SIGUIENTE ---
                    # Buscamos a cada No Terminal dentro de la producción
                    for i, token in enumerate(produccion):
                        if token in self.gramatica: # Si es un No Terminal (llave)
                            
                            # Mirar a la derecha para ver quién lo sigue
                            encontrado_limite = False
                            for j in range(i + 1, len(produccion)):
                                siguiente_token = produccion[j]
                                
                                if self.es_terminal(siguiente_token):
                                    if siguiente_token != self.simbolo_vacio:
                                        self.siguiente[token].add(siguiente_token)
                                        encontrado_limite = True
                                        break
                                else:
                                    # Si lo que sigue es No Terminal, le robamos su PRIMERO
                                    self.siguiente[token].update(self.primero[siguiente_token] - {self.simbolo_vacio})
                                    if self.simbolo_vacio not in self.primero[siguiente_token]:
                                        encontrado_limite = True
                                        break
                            
                            # Regla de Herencia: Si está al final o lo que sigue es epsilon
                            if not encontrado_limite:
                                # El hijo hereda el SIGUIENTE de su padre (nt)
                                self.siguiente[token].update(self.siguiente[nt])

            # Verificación de Estabilidad
            if estado_anterior != (str(self.primero) + str(self.siguiente)):
                estabilizado = False

    def imprimir_tabla(self):
        print(f"\n{'No Terminal':<15} | {'Conjunto Primero':<30} | {'Conjunto Siguiente':<30}")
        print("-" * 80)
        for nt in self.no_terminales:
            p = "{" + ", ".join(sorted(self.primero[nt])) + "}"
            s = "{" + ", ".join(sorted(self.siguiente[nt])) + "}"
            print(f"{nt:<15} | {p:<30} | {s:<30}")

def menu():
    analizador = AnalizadorGramatical()
    
    while True:
        print("\n========================================")
        print("   GENERADOR DE PRIMERO Y SIGUIENTE")
        print("========================================")
        print("1. Cargar ejemplo precargado (Asignación)")
        print("2. Ingresar gramática manualmente")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            analizador.cargar_ejemplo_asignacion()
        elif opcion == "2":
            analizador.limpiar_datos()
            print("Ingrese reglas (Var -> Prod1 | Prod2). Escriba 'FIN' al terminar.")
            while True:
                linea = input("> ")
                if linea.upper() == "FIN": break
                if "->" not in linea: continue
                
                izq, der = linea.split("->")
                nt = izq.strip()
                # Separar por | y luego por espacios para tokens multicarácter
                prods = [p.strip().split() for p in der.split("|")]
                
                if nt not in analizador.gramatica:
                    analizador.gramatica[nt] = []
                    analizador.no_terminales.append(nt)
                analizador.gramatica[nt].extend(prods)
        elif opcion == "3":
            break
        else: continue

        # Validaciones de seguridad[cite: 1]
        if not analizador.validar_recursion_izquierda(): continue
        if not analizador.validar_huerfanos(): continue
        
        # Procesamiento
        analizador.calcular_conjuntos()
        analizador.imprimir_tabla()

if __name__ == "__main__":
    menu()