from sys import path_importer_cache
from Token import Token
from Error import Error
import re


class AnalizadorLexico:
    def __init__(self):
        self.listaTokens = []
        self.listaErrores = []

    def analizar(self, codigo_fuente):
        self.listaTokens = []
        self.listaErrores = []
        
        #inicializar atributos
        linea = 1
        columna = 1
        buffer = ''
        centinela = '$'
        estado = 0
        codigo_fuente += centinela

        #automata
        i = 0
        while i< len(codigo_fuente):
            c = codigo_fuente[i]
            
            if estado == 0:
                if re.search(r'[a-zA-Z]', c): #ENTRADA DE LETRAS AL ESTADO 3
                    buffer += c
                    columna += 1
                    estado = 3
                elif re.search('\d', c): #ENTRADA DE DIGITOS AL ESTADO 2
                    buffer += c 
                    columna += 1
                    estado = 2
                elif re.search('#', c): #ENTRADA DE DIGITOS DE CODIGO HEXA. AL ESTADO 4
                    buffer += c 
                    columna += 1
                    estado = 4
                elif c == '@': #ENTRADA DE DIGITOS DE CODIGO HEXA. AL ESTADO 4
                    buffer += c 
                    columna += 1
                    estado = 5
                elif c == '=': 
                    buffer += c
                    self.listaTokens.append(Token(buffer, ' caracter signo igual', linea, columna))
                    buffer = ''
                    columna += 1
                elif c == ';': 
                    buffer += c
                    self.listaTokens.append(Token(buffer, 'caracter punto y coma', linea, columna))
                    buffer = ''
                    columna += 1
                elif c == '{': 
                    buffer += c
                    self.listaTokens.append(Token(buffer, 'Llave de abertura', linea, columna))
                    buffer = ''
                    columna += 1
                elif c == '}': 
                    buffer += c
                    self.listaTokens.append(Token(buffer, 'Llave de cierrre', linea, columna))
                    buffer = ''
                    columna += 1
                elif c == '[': 
                    buffer += c
                    self.listaTokens.append(Token(buffer, 'Corchete de abertura', linea, columna))
                    buffer = ''
                    columna += 1
                elif c == ']': 
                    buffer += c
                    self.listaTokens.append(Token(buffer, 'Corchete de cierrre', linea, columna))
                    buffer = ''
                    columna += 1
                elif c == ',': 
                    buffer += c
                    self.listaTokens.append(Token(buffer, 'caracter coma', linea, columna))
                    buffer = ''
                    columna += 1
                elif c == '\'' or c == '"':
                    buffer += c
                    columna += 1
                    estado = 1
                elif c == '\n':
                    linea += 1
                    columna = 1
                elif c == '\t':
                    columna += 1
                elif c == ' ':
                    columna += 1    
                elif c == '\r':
                    pass
                elif c == centinela:
                    print('Se aceptó la cadena!')
                    break
                else:
                    buffer += c
                    self.listaErrores.append(Error('Caracter ' + buffer + ' no reconocido en el lenguaje.', 'Léxico', linea, columna))
                    buffer = ''
                    columna += 1
            elif estado == 1: # ESTADO 1 ACEPTACION DE CADENAS
                if c == '\'' or c == '"':
                    buffer += c
                    self.listaTokens.append(Token(buffer, 'cadena', linea, columna))
                    buffer = ''
                    columna += 1
                    estado = 0
                elif c == '\n':
                    buffer += c
                    linea += 1
                    columna = 1
                elif c == '\r':
                    buffer += c
                else:
                    buffer += c
                    columna += 1
            elif estado == 2: # ESTADO 2 DE ACEPTACION DE DIGITOS
                if re.search('\d', c):
                    buffer += c
                    columna += 1
                else:
                    columna -= 1
                    self.listaTokens.append(Token(buffer, 'entero', linea, columna))
                    columna += 1
                    buffer = ''
                    i -= 1
                    estado = 0
            elif estado == 3: # ESTADO 3 DE ACEPTACION DE PALABRAS
                if re.search(r'[a-zA-Z]', c):
                    buffer += c
                    columna += 1
                else:
                    if buffer == 'TITULO':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda TITULO', linea, columna))
                        columna +=1
                    elif buffer == 'ANCHO':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda ANCHO', linea, columna))
                        columna +=1
                    elif buffer == 'ALTO':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda ALTO', linea, columna))
                        columna +=1
                    elif buffer == 'FILAS':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda FILAS', linea, columna))
                        columna +=1
                    elif buffer == 'COLUMNAS':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda COLUMNAS', linea, columna))
                        columna +=1
                    elif buffer == 'CELDAS':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda CELDAS', linea, columna)) 
                        columna +=1  
                    elif buffer == 'FILTROS':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda FILTROS', linea, columna))
                        columna +=1
                    elif buffer == 'MIRRORX':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda MIRRORX', linea, columna))
                        columna +=1
                    elif buffer == 'MIRRORY':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda MIRRORY', linea, columna))
                        columna +=1
                    elif buffer == 'DOUBLEMIRROR':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra reservarda DOUBLEMIRROR', linea, columna))
                        columna +=1
                    elif buffer == 'TRUE':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra booleana TRUE', linea, columna))
                        columna +=1
                    elif buffer == 'FALSE':
                        columna -=1
                        self.listaTokens.append(Token(buffer, 'palabra booleana FALSE', linea, columna))
                        columna +=1
                    else:
                        buffer += c
                        columna -=1
                        self.listaErrores.append(Error('Caracter ' + buffer + ' no reconocido en el lenguaje.', 'Léxico', linea, columna))
                        buffer = ''
                        columna += 1
                    buffer = ''
                    i -= 1
                    estado = 0
            elif estado == 4: # ESTADO 4 DE ACEPTACION DE CODIGO HEXA.
                if re.search(r'[a-zA-Z0-9]', c):
                    buffer += c
                    columna += 1
                else:
                    columna -= 1
                    self.listaTokens.append(Token(buffer, 'codigo hexagesimal', linea, columna))
                    columna += 1
                    buffer = ''
                    i -= 1
                    estado = 0
            elif estado == 5:
                if c == '@': 
                    buffer += c 
                    columna += 1
                    estado = 6
            elif estado == 6:
                if c == '@': 
                    buffer += c 
                    columna += 1
                    estado = 7
            elif estado == 7:
                if c == '@': 
                    buffer += c 
                    columna += 1
                else:
                    columna -= 1
                    self.listaTokens.append(Token(buffer, 'separacion', linea, columna))
                    columna += 1
                    buffer = ''
                    i -= 1
                    estado = 0    


            i += 1
        

    def impTokens(self):
        for t in self.listaTokens:
            t.impToken()

    def impErrores(self):
        if len(self.listaErrores) == 0:
            print('No hubo errores')
        else:
            for e in self.listaErrores:
                e.impError()

    def ReporteToken(self):
     inicio = """ 
       <!doctype html>
       <html lang="en">
       <head>
       <meta charset="utf-8">
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
       <title>Reportes</title>
        </head>
        <body style="background-color:#FFEBDB;">
         <center>
            <h1 style="border: ridge #d3d3eb 5px; background-color:#25425C; color:#FFEBDB ;">REPORTES</h1>
            <p>
                <span style="border-image: initial; border: 2px solid #FB770D;background-color:#FFA45B;color:#FFFF;font-size: 25px;">LISTA DE TOKENS</span> 
            </p>
            
            <table class="table" style="width: 800px;">
                <thead class="table-dark">
                    <tr>
                        
                        <th scope="col" with="30px">TOKEN</th>
                        <th scope="col" with="30px">LEXEMA</th>
                        <th scope="col" with="30px">LINEA</th>
                        <th scope="col" with="30px">COUMNA</th>
                    </tr>
                </thead>"""

     for x in self.listaTokens:
         inicio+= """ <tbody>
                <tr>
                    
                    <td style="width:30px;">"""+str(x.lexema)+"""</td>
                    <td style="width:50px;">"""+str(x.tipo)+"""</td>
                    <td style="width:50px;">"""+str(x.linea)+"""</td>
                    <td style="width:50px;">"""+str(x.columna)+"""</td>
                </tr>
            </tbody>"""
           
     fin = """</table>
       </center>
      </body>
      </html>"""

     inicio += fin
     CrearArchivo("Reportes.html",inicio)
     
    def ReporteErrores(self):
     inicio = """ 
       <!doctype html>
       <html lang="en">
       <head>
       <meta charset="utf-8">
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
       <title>Reportes</title>
        </head>
        <body style="background-color:#FFEBDB;">
         <center>
            <h1 style="border: ridge #d3d3eb 5px; background-color:#25425C; color:#FFEBDB ;">REPORTES</h1>
            <p>
                <span style="border-image: initial; border: 2px solid #FB770D;background-color:#FFA45B;color:#FFFF;font-size: 25px;">LISTA DE ERRORES</span> 
            </p>
            
            <table class="table" style="width: 800px;">
                <thead class="table-dark">
                    <tr>
                        <th scope="col" with="30px">ERRORES</th>
                        <th scope="col" with="30px">TIPO</th>
                        <th scope="col" with="30px">LINEA</th>
                        <th scope="col" with="30px">COUMNA</th>
                    </tr>
                </thead>"""

     for x in self.listaErrores:
         inicio+= """ <tbody>
                <tr>
                    
                    <td style="width:30px;">"""+str(x.descripcion)+"""</td>
                    <td style="width:50px;">LEXICO</td>
                    <td style="width:50px;">"""+str(x.linea)+"""</td>
                    <td style="width:50px;">"""+str(x.columna)+"""</td>
                </tr>
            </tbody>"""
           
     fin = """</table>
       </center>
      </body>
      </html>"""

     inicio += fin
     CrearArchivo("ReportesErrores.html",inicio)


def CrearArchivo(ruta, contenido):#ESCRITURA DE ARCHIVO PARA REPORTES
    archivo = open(ruta, 'w')
    archivo.write(contenido)
    archivo.close
