class Error:
    def __init__(self, descripcion, tipo, linea, columna):
        self.descripcion = descripcion
        self.tipo = tipo
        self.linea = linea
        self.columna = columna

    def impError(self):
        print(self.descripcion, self.tipo, self.linea, self.columna)