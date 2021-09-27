from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from AnalizadorLexico import AnalizadorLexico
from Celdas import Celdas
from Imagen import Imagen
from html2image import Html2Image
import re
import sys
import webbrowser
from PIL import ImageTk, Image


def Buscar_archivo():  # FUNCION QUE REALIZAR LA SELLECION DEL ARCHIVO A LEER Y RETORNA EL CONTENIDO
    global codigo_fuente
    Tk().withdraw()
    archivo = filedialog.askopenfile(
        title="Seleccionar un archivo",
        initialdir="./",
        filetypes=(
            ("Archivos pxla", "*.pxla"),
        )
    )
    if archivo is None:
        print('No se seleccionó ningun archivo\n')
        return None
    else:
        texto = archivo.read()
        archivo.close()
        print('Lectura exitosa\n')
        codigo_fuente = texto

def analizar():
    global scanner
    scanner = AnalizadorLexico()
    scanner.analizar(codigo_fuente)
    #scanner.impTokens()
    #
    scanner.impErrores()

def splitImg():  # FUNCION QUE ANALIZA EL CONTENIDO DEL ARCHIVO SEPARACION DE IMAGENES
  listaIma = splitear(codigo_fuente,"@")
  listaatri = [] #ALACENARA CADA ATRITU DE IMAGEN
  i = 0
  while i< len(listaIma):
      listaatri = splitear2(listaIma[i],";")
      valIma(listaatri)
      listaatri = []
      i += 1
  
def valIma(listaA):
    global listaIMAGEN
    CELDAS = []
    FILTROS = []
    bandera = "N"
    auxiliar = ''
    posicion = 1
    i = 0
    titulo = ""
    ancho = 0
    alto = 0
    filas = 0
    columnas = 0
    listaCeldas = []
    celdas = ""
    filtros = ""
    
    while i< len(listaA):
      if i == 0:
          cadena = listaA[i]
          auxiliar = ''
          posicion = 1
          for leido in cadena:
           if leido == '=':
            posicion +=1
            continue
           if leido == "\"":
            titulo = auxiliar.strip()
            auxiliar= ''
           else:
            auxiliar += leido
            posicion +=1
      if i == 1:
          cadena = listaA[i]
          centinela = "$"
          cadena+=centinela
          auxiliar = ''
          posicion = 1
          for leido in cadena:
           if re.search(r'[a-zA-Z]', leido):
                posicion +=1
                continue
           if leido == "=":
            posicion +=1
            continue
           if leido == '$':
            ancho = int(auxiliar)
            auxiliar= ''
           else:
            auxiliar += leido
            posicion +=1
      if i == 2:
          cadena = listaA[i]
          centinela = "$"
          cadena+=centinela
          auxiliar = ''
          posicion = 1
          for leido in cadena:
           if re.search(r'[a-zA-Z]', leido):
                posicion +=1
                continue
           if leido == "=":
            posicion +=1
            continue
           if leido == '$':
            alto = int(auxiliar)
            auxiliar= ''
           else:
            auxiliar += leido
            posicion +=1
      if i == 3:
          cadena = listaA[i]
          centinela = "$"
          cadena+=centinela
          auxiliar = ''
          posicion = 1
          for leido in cadena:
           if re.search(r'[a-zA-Z]', leido):
                posicion +=1
                continue
           if leido == "=":
            posicion +=1
            continue
           if leido == '$':
            filas = int(auxiliar)
            auxiliar= ''
           else:
            auxiliar += leido
            posicion +=1 
      if i == 4:
          cadena = listaA[i]
          centinela = "$"
          cadena+=centinela
          auxiliar = ''
          posicion = 1
          for leido in cadena:
           if re.search(r'[a-zA-Z]', leido):
                posicion +=1
                continue
           if leido == "=":
            posicion +=1
            continue
           if leido == '$':
            columnas = int(auxiliar)
            auxiliar= ''
           else:
            auxiliar += leido
            posicion +=1 
      if i == 5:
          cadena = listaA[i]
          auxiliar = ''
          posicion = 1
          for leido in cadena:
           if bandera =='N':
            if leido == '=' or leido ==' ':
                bandera='A'
                auxiliar =''
            else:
             auxiliar += leido
             posicion +=1
           elif bandera =='A':

            if leido == '=':
                posicion +=1
                continue
            if leido == '[':
                posicion+=1
                continue
            if leido == ']':
                posicion +=1
                continue
            if leido == '"':
                posicion +=1
                continue
            if leido == ' ':
                posicion +=1
                continue
            if leido == '{' :
                posicion +=1
                continue
            if leido == '}':
                celdas = auxiliar.strip()
                listaCeldas = splitear2(celdas,"\n")
                bandera = 'N'
                auxiliar= ''
            else:
              auxiliar += leido
              posicion +=1
           else:
            return None
      if i == 6:
          cadena = listaA[i]
          centinela = "$"
          cadena +=centinela
          auxiliar = ''
          posicion = 1
          for leido in cadena:
           if bandera =='N':
            if leido == '=' or leido ==' ':
                bandera='A'
                auxiliar =''
            else:
             auxiliar += leido
             posicion +=1
           elif bandera =='A':
            if leido == '=':
                posicion +=1
                continue
            if leido == '$':
                filtros = auxiliar.strip()
                FILTROS = splitear2(filtros,",")
                auxiliar= ''
            else:
              auxiliar += leido
              posicion +=1
           else:
            return None
      else:
            pass
      
      i += 1

    for linea in listaCeldas:
        datos = splitear2(linea, ',')
        x = int(datos[0])
        y = int(datos[1])
        estado = datos[2]
        codigo = datos[3]
        CELDAS.append(Celdas(x, y,estado,codigo))
        
    listaIMAGEN.append(Imagen(titulo,ancho,alto,filas,columnas,CELDAS,FILTROS))
 
def splitear2(cadena, caracter):#FUNCION QUE SEPARA CONTENIDO POR ATRIBUTO
    temporal = ""
    listaTemporal = []
    for i in cadena:
        if i == caracter:
            listaTemporal.append(temporal.strip())
            temporal = ""
        else:
            temporal += i
    if temporal.strip() != "":
        listaTemporal.append(temporal.strip())
    return listaTemporal

def splitear(cadena, caracter):#FUNCION QUE SEPARA CONTENIDO POR IMAGEN
    temporal = ""
    listaTemporal = []
    cont = 0
    for i in cadena:
        if i == caracter:
          cont +=1
          if cont == 4:
            listaTemporal.append(temporal.strip())
            temporal = ""
            cont = 0
          else:
           print()
        else:
            temporal += i
    if temporal.strip() != "":
        listaTemporal.append(temporal.strip())
    return listaTemporal
       
def changetitulos():#FUNCION PARA CARGAR AL COMBOBOX
   listaOp =  []
   for img in listaIMAGEN:
       listaOp.append(img.titulo)

   comboImg['values'] = listaOp

def changetDim():#FUNCION PARA CARGAR AL COMBOBOX
   figura = comboImg.get()
   dimension = "Dimension:"
   for img in listaIMAGEN:
       if figura == img.titulo:
           dimension += ''' '''+str(img.ancho)+'''x'''+str(img.alto)+''''''
       else:
           None

   label4['text'] = dimension
   
def labelestado1():
    label1['text'] = "Archivo cargado en memoria" 

def labelestado2():
    label1['text'] = "Archivo analizado" 


def salir():#BOTON SALIR 
  sys.exit()  

def CrearREPORTES(): #CREAR REPORTE
 scanner.ReporteToken()
 scanner.ReporteErrores()

def abrirReportes():#ABRIR REPORTE
    webbrowser.open_new("Reportes.html")
    webbrowser.open_new("ReportesErrores.html")
    webbrowser.open_new("Imagenes.html")

def crearImagen():#FUNCION QUE GENERA IMAGENES
  global listaIMAGEN
  HtmlGeneral = ""
  HTMLImgagen =""
  titulo = ""
  ancho = 0
  alto = 0
  filasY = 0
  columnasX = 0
  filtros = "" 
  yfila = 0
  xcolumna = 0
  confirmacion = []
  altoCelda = 0 
  anchoCelda =  0
  HtmlGeneral += '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
        <title>Reportes Img</title>
        </head>
        <body style="background-color:#FFEBDB">
        <center>
        <h1 style="border: ridge #d3d3eb 5px; background-color:#25425C; color:#FFEBDB ;">REPORTES</h1>
        </center>'''

  for img in listaIMAGEN:
    titulo = img.titulo
    ancho = img.ancho
    alto = img.alto
    filasY = img.filas
    columnasX = img.columnas
    filtros = img.filtros
    altoCelda = int(alto)/int(filasY)
    anchoCelda =  int(ancho)/int(columnasX)
    imgORIGINAL = ''''''
    imgMIRRORX = ""
    imgMIRRORY = ""
    imgDOUBLEMIRROR = "" 
    
    HtmlGeneral += '''
          <style>
        table{
            width: '''+str(ancho)+'''px;
            height: '''+str(alto)+'''px;
            border: 1px solid black;
            border-collapse: collapse;
        }
        td{
            border: 0.1px solid black;
            width: '''+str(anchoCelda)+'''px;
            height: '''+str(altoCelda)+'''px;
        }
        </style>
        <center>'''

    HTMLImgagen +='''
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
        <title>Imagen</title>
        <style>
        table{
            width: '''+str(ancho)+'''px;
            height: '''+str(alto)+'''px;
            border: 1px solid black;
            border-collapse: collapse;
        }
        td{
            border: 0.1px solid black;
            width: '''+str(anchoCelda)+'''px;
            height: '''+str(altoCelda)+'''px;
        }
        </style>
            '''

    imgORIGINAL += HTMLImgagen 
    imgMIRRORX += HTMLImgagen
    imgMIRRORY += HTMLImgagen
    imgDOUBLEMIRROR += HTMLImgagen
    HtmlGeneral += "<h3>Imagen Original</h3>\n"
    HtmlGeneral += "<h4>Titulo: "+titulo+" Dimension: "+str(ancho)+"x"+str(alto)+"</h4>\n"
    HtmlGeneral += "<table>\n"
    imgORIGINAL += "<table>\n" 
    for yfila in range(int(filasY)): 
      HtmlGeneral += "<tr>\n"
      imgORIGINAL += "<tr>\n"
      for xcolumna in range(int(columnasX)):
       confirmacion = img.buscarCelda(xcolumna,yfila)    
       if confirmacion is not None:       
        if confirmacion[2] == "FALSE":
          HtmlGeneral += "<td style=\"background-color: #FFFFFF;\" ></td>\n"
          imgORIGINAL += "<td style=\"background-color: #FFFFFF;\" ></td>\n" 
        else:       
          HtmlGeneral += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"
          imgORIGINAL += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"       
       else:  
         HtmlGeneral += "<td style=\"background-color: #FFFFFF;\"></td>\n"
         imgORIGINAL += "<td style=\"background-color: #FFFFFF;\"></td>\n" 
         confirmacion = []       
      HtmlGeneral += "</tr>\n"
      imgORIGINAL += "</tr>\n" 

    HtmlGeneral += "</table>\n"
    imgORIGINAL += "</table>\n" 
    imgORIGINAL += "</body></html>"

    hti = Html2Image()
    hti.screenshot(html_str=imgORIGINAL, save_as=''+titulo+'Orignal.png', size=(int(ancho), int(alto)))
    imgORIGINAL = """ """

    if "MIRRORY" in filtros:
            HtmlGeneral += "<h3>Imagen Filtro MirrorY</h3>\n"
            HtmlGeneral += "<table>\n"
            imgMIRRORY += "<table>\n"
            for yfila in range(int(filasY)-1,-1,-1):
                HtmlGeneral += "<tr>\n"
                imgMIRRORY  += "<tr>\n"
                for xcolumna in range(int(columnasX)):
                    confirmacion = img.buscarCelda(xcolumna,yfila)
                    if confirmacion is not None:
                        if confirmacion[2] == "FALSE":
                            HtmlGeneral += "<td style=\"background-color: #FFFFFF;\" ></td>\n"
                            imgMIRRORY += "<td style=\"background-color: #FFFFFF;\" ></td>\n"
                        else:
                            HtmlGeneral += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"
                            imgMIRRORY += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"
                    else:
                        HtmlGeneral += "<td style=\"background-color: #FFFFFF;\"></td>\n"
                        imgMIRRORY += "<td style=\"background-color: #FFFFFF;\"></td>\n"
                        confirmacion = []
                        
                HtmlGeneral += "</tr>\n"
                imgMIRRORY += "</tr>\n"
            HtmlGeneral += "</table>\n" 
            imgMIRRORY += "</table>\n" 
            imgMIRRORY += "</body></html>"   

            hti = Html2Image()
            hti.screenshot(html_str=imgMIRRORY, save_as=''+titulo+'MirrorY.png', size=(int(ancho), int(alto)))
            imgMIRRORY = """ """

    if "MIRRORX" in filtros:
            HtmlGeneral += "<h3>Imagen Filtro MirrorX</h3>\n"
            HtmlGeneral += "<table>\n"
            imgMIRRORX += "<table>\n"
            for yfila in range(int(filasY)):
                HtmlGeneral += "<tr>\n"
                imgMIRRORX += "<tr>\n"
                for xcolumna in range(int(columnasX)-1,-1,-1):
                    confirmacion = img.buscarCelda(xcolumna,yfila)
                    if confirmacion is not None:
                        if confirmacion[2] == "FALSE":
                            HtmlGeneral += "<td style=\"background-color: #FFFFFF;\" ></td>\n"
                            imgMIRRORX += "<td style=\"background-color: #FFFFFF;\" ></td>\n"
                        else:
                            HtmlGeneral += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"
                            imgMIRRORX += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"
                    else:
                       
                        HtmlGeneral += "<td style=\"background-color: #FFFFFF;\"></td>\n"
                        imgMIRRORX += "<td style=\"background-color: #FFFFFF;\"></td>\n"
                        confirmacion = []
                       
                HtmlGeneral += "</tr>\n"
                imgMIRRORX += "</tr>\n"
            HtmlGeneral += "</table>\n"
            imgMIRRORX+= "</table>\n"

            hti = Html2Image()
            hti.screenshot(html_str=imgMIRRORX, save_as=''+titulo+'MirrorX.png', size=(int(ancho), int(alto)))
            imgMIRRORX = """ """
    if "DOUBLEMIRROR" in filtros:
            HtmlGeneral += "<h3>Imagen FILTRO DOUBLEMIRROR</h3>\n"
            HtmlGeneral += "<table>\n"
            imgDOUBLEMIRROR += "<table>\n"
            for yfila in range(int(filasY)-1,-1,-1):
                HtmlGeneral += "<tr>\n"
                imgDOUBLEMIRROR += "<tr>\n"
                for xcolumna in range(int(columnasX)-1,-1,-1):
                    confirmacion = img.buscarCelda(xcolumna,yfila)
                    if confirmacion is not None:
                        if confirmacion[2] == "FALSE":
                            HtmlGeneral += "<td style=\"background-color: #FFFFFF;\" ></td>\n"
                            imgDOUBLEMIRROR += "<td style=\"background-color: #FFFFFF;\" ></td>\n"
                        else:
                            HtmlGeneral += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"
                            imgDOUBLEMIRROR += "<td style=\"background-color: "+confirmacion[3]+";\"></td>\n"
                    else:
                        HtmlGeneral += "<td style=\"background-color: #FFFFFF;\"></td>\n"
                        imgDOUBLEMIRROR += "<td style=\"background-color: #FFFFFF;\"></td>\n"
                        
                HtmlGeneral += "</tr>\n"
                imgDOUBLEMIRROR += "</tr>\n"
            HtmlGeneral += "</table>\n" 
            imgDOUBLEMIRROR += "</table>\n" 
            hti = Html2Image()
            hti.screenshot(html_str=imgDOUBLEMIRROR, save_as=''+titulo+'DoubleMirror.png', size=(int(ancho), int(alto)))
            imgDOUBLEMIRROR = """ """

    HtmlGeneral += '''
             </center>
            </body>
        </html>'''


  CrearArchivo("Imagenes.html", HtmlGeneral)

def CrearArchivo(ruta, contenido):#ESCRITURA DE ARCHIVO PARA REPORTES
    archivo = open(ruta, 'w')
    archivo.write(contenido)
    archivo.close

def MostrarImagenOriginal():
  nombre = comboImg.get()
  img = Image.open(''+nombre+'Orignal.png')
  new_img = img.resize((300,300))
  render = ImageTk.PhotoImage(new_img)
  img1 = Label(ventana, image=render)
  img1.image = render
  img1.place(x=280, y = 80)


def MostrarImagenX():
  nombre = comboImg.get()
  img = Image.open(''+nombre+'MirrorX.png')
  new_img = img.resize((300,300))
  render = ImageTk.PhotoImage(new_img)
  img1 = Label(ventana, image=render)
  img1.image = render
  img1.place(x=280, y = 80)

def MostrarImagenY():
  nombre = comboImg.get()
  img = Image.open(''+nombre+'MirrorY.png')
  new_img = img.resize((300,300))
  render = ImageTk.PhotoImage(new_img)
  img1 = Label(ventana, image=render)
  img1.image = render
  img1.place(x=280, y = 80)

def MostrarImagenD():
  nombre = comboImg.get()
  img = Image.open(''+nombre+'DoubleMirror.png')
  new_img = img.resize((300,300))
  render = ImageTk.PhotoImage(new_img)
  img1 = Label(ventana, image=render)
  img1.image = render
  img1.place(x=280, y = 80)
 

if __name__ == '__main__':
    global listaIMAGEN
    listaIMAGEN = []
    global codigo_fuente
    codigo_fuente = ""  # CODIGO FUENTE SIN ANALIZAR

    ventana = Tk()
    ventana.title("Bitxelart")
    
    btnCargar = Button(ventana, text="Cargar", width=7,height=1, command=lambda: [Buscar_archivo(),labelestado1()])
    btnCargar.grid(column=1, row=0)

    btnAnalizar = Button(ventana, text="Analizar", width=8, height=1, command=lambda: [analizar(), splitImg(),crearImagen(),labelestado2()])
    btnAnalizar.grid(column=2, row=0)

    btnReportes = Button(ventana, text="Reportes", width=8, height=1, command=lambda: [CrearREPORTES(), abrirReportes()])
    btnReportes.grid(column=3, row=0)

    btnSalir = Button(ventana, text="Salir", width=7, height=1,command=salir)
    btnSalir.grid(column=4, row=0)

    btnOriginal = Button(ventana, text="Original", width=15, height=2, command=lambda: [MostrarImagenOriginal(), changetDim()])
    btnOriginal.place(x = 30,y = 140)

    btnMirrorX = Button(ventana, text="MirrorX",width=15, height=2,command= lambda: [MostrarImagenX(), changetDim()] )
    btnMirrorX.place(x = 30,y = 190)

    btnMirrorY = Button(ventana, text="MirrorY", width=15, height=2,command=  lambda: [MostrarImagenY(), changetDim()])
    btnMirrorY.place(x = 30,y = 240)

    btnDOUBLEMIRROR = Button(ventana, text="DoubleMirror", width=15, height=2,command=  lambda: [MostrarImagenD(), changetDim()])
    btnDOUBLEMIRROR.place(x = 30,y = 290)
    
    label = Label(ventana,text="LISTA DE IMAGENES")
    label.place(x = 30,y = 50)

    label2 = Label(ventana,text="Estado:")
    label2.place(x = 305,y = 5)
    
    label1 = Label(ventana,text="Ningun archivo en memoria")
    label1.place(x = 350,y = 5)

    label4 = Label(ventana,text="")
    label4.place(x = 350,y = 40)
   
    opciones =[]
    comboImg = ttk.Combobox(ventana, height=1, width=20, values=['Aun no hay imagenes'], postcommand= changetitulos, state="readonly")
    comboImg.current(0)
    comboImg.place(x = 30,y = 70)
    

    ventana.geometry('650x400+200+100')
    ventana.mainloop()
   