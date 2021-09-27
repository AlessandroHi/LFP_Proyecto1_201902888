from Celdas import Celdas

class Imagen(object):
    def __init__(self,titulo,ancho,alto,filas,columnas,celdas,filtros):
        self.titulo = titulo
        self.ancho = ancho
        self.alto = alto
        self.filas = filas
        self.columnas = columnas
        self.celdas = celdas
        self.filtros = filtros
    
    def buscarCelda(self,x,y):#VERIFICACION DE CELDAS
        existe = []
        for i in self.celdas:
            if i.x == x and i.y == y:
                existe.append(i.x)
                existe.append(i.y)
                existe.append(i.estado)
                existe.append(i.codigo)
                return existe
        return None

