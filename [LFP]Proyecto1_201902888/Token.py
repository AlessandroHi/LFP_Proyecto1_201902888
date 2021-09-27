class Token:
    def __init__(self, lexema, tipo,  linea, columna):
        self.lexema = lexema
        self.tipo = tipo
        self.columna = columna 
        self.linea = linea 

    def impToken(self):
        print("Lexema: "+ self.lexema, "  Tipo: ",self.tipo,"  Linea: ",self.linea,"  Columna: ", self.columna)