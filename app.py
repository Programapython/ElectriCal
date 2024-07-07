from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QPushButton, QToolBar,QFileDialog, QMenu, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
import sys

import webbrowser
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class Aplicacion_Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        
        #Características de la ventana
        #self.title = 'Calculadora de consumo eléctrico'
        self.title = 'ElectriCal'
        self.left = 100
        self.top = 100
        self.width = 600
        self.height = 500

        #DEFINICION DE VARIABLES
        self.meses=[]
        self.consumo=[]

        self.n_informe=0
        self.direc="Ningun archivo seleccionado"
        self.n_dat="0"
        self.n_dat_eleg="0"
        self.ecu="---"

        self.inicializar_gui()

    def inicializar_gui(self):
               
        #SE DEFINE LAS PROPIEDADES PRINCIPALES DE LA VENTANA
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icono.ico'))
        self.setGeometry(self.left, self.top, self.width, self.height)

        #SE AGREGA UN MENU DE OPCIONES
        menu = self.menuBar()
        self.menuArchivo = menu.addMenu('Archivo')
        self.menuHerra = menu.addMenu('Herramientas')
        self.menuApar = menu.addMenu('Apariencia')
        self.menuAcerca = menu.addMenu('Acerca de')
        
        #SE AGREGAN LAS OPCIONES DE CDAD SECCION DEL MENU
        op1 = QAction('Abrir archivo', self)
        op1.triggered.connect(self.cambiar_direc)
        self.menuArchivo.addAction(op1)
        op2 = QAction('Personalizar', self)
        op2.triggered.connect(self.cambiar_direc)
        self.menuHerra.addAction(op2)
        op3 = QAction('Detalles', self)
        op3.triggered.connect(self.cambiar_direc)
        self.menuHerra.addAction(op3)
        op4 = QAction('Imprimir', self)
        op4.triggered.connect(self.gen_informe)
        self.menuHerra.addAction(op4)
        op5 = QAction('Acerca de ...', self)
        op5.triggered.connect(self.ir_pag)
        self.menuAcerca.addAction(op5)

        #SE DEFINE EL CONTENEDOR PRINCIPAL
        self.frame = QWidget()
        self.contPrincipal = QVBoxLayout()
        #SE DEFINE LOS CONTENEDORES
        self.contArch = QGroupBox('SELECCIONAR LA FUENTE DE DATOS')
        self.contArch.setFixedHeight(70)
        self.contGraf = QGroupBox('GRÁFICA DEL CONSUMO ELÉCTRICO')
        #self.contGraf.setFixedHeight(300)
        self.contResult = QGroupBox('RESULTADOS')
        self.contResult.setFixedHeight(130)

        #COLOCAR LAS ETIQUETAS
        #############################################################
        #############################################################
        self.label1 = QLabel("Fuente de datos(.xlsx):", self.contArch)
        self.label1.move(10,20)
        self.lDirec = QLabel(self.direc, self.contArch)
        self.lDirec.setFixedWidth(200)
        self.lDirec.move(130,20)
        self.boton1 = QPushButton("Cambiar la dirección",self.contArch)
        self.boton1.clicked.connect(self.cambiar_direc)
        self.boton1.setFixedWidth(150)
        self.boton1.move(350,15)
        self.label1 = QLabel("N° total de datos:", self.contArch)
        self.label1.move(10,45)
        self.nDat1 = QLabel(self.n_dat, self.contArch)
        self.nDat1.setFixedWidth(200)
        self.nDat1.move(100,45)
        self.label2 = QLabel("N° datos considerados:", self.contArch)
        self.label2.move(130,45)
        self.nDatEleg = QLabel(self.n_dat_eleg, self.contArch)
        self.nDatEleg.setFixedWidth(200)
        self.nDatEleg.move(245,45)
        self.boton2 = QPushButton("Personalizar",self.contArch)
        self.boton2.clicked.connect(self.cambiar_direc)
        self.boton2.setFixedWidth(150)
        self.boton2.move(350,40)
        

        self.label1 = QLabel("N° total de datos:", self.contResult)
        self.label1.move(10,20)
        self.nDat2 = QLabel(self.n_dat, self.contResult)
        self.nDat2.setFixedWidth(200)
        self.nDat2.move(105,20)
        self.label2 = QLabel("N° datos considerados:", self.contResult)
        self.label2.move(10,40)
        self.nDatEleg = QLabel(self.n_dat_eleg, self.contResult)
        self.nDatEleg.setFixedWidth(200)
        self.nDatEleg.move(128,40)
        self.label1 = QLabel("Ecuación obtenida por regresión:", self.contResult)
        self.label1.move(10,65)
        self.lEcu = QLabel(self.ecu, self.contResult)
        self.lEcu.setFixedWidth(400)
        self.lEcu.move(175,65)
        self.boton1 = QPushButton("Ver más detalles", self.contResult)
        self.boton1.clicked.connect(self.cambiar_direc)
        self.boton1.move(10,90)
        #############################################################
        #############################################################


        self.contPrincipal.addWidget(self.contArch)
        self.contPrincipal.addWidget(self.contGraf)
        self.contPrincipal.addWidget(self.contResult)

        self.frame.setLayout(self.contPrincipal)
        self.setCentralWidget(self.frame)

        self.show()

    def grafica(self,x1,y1,x2,y2):
        #Se define la caja que va contner a las figuras
        self.figuras = QHBoxLayout()

        #Se crean las figuras y se colocan en el interior de un contenedor

        #GRAFICA CON PREDICCIÓN
        self.fig1 = Figure(figsize=(1.5,2))
        self.canva1 = FigureCanvasQTAgg(self.fig1)
        #GRAFICA VERDADERA
        self.fig2 = Figure(figsize=(1.5,2))
        self.canva2 = FigureCanvasQTAgg(self.fig2)

        #Se grafica en ambas gráficas

        ax1 = self.fig1.add_subplot(111)
        ax1.plot(x1,y1)
        self.canva1.draw()

        ax2 = self.fig2.add_subplot(111)
        ax2.plot(x2,y2)
        self.canva2.draw()


        self.figuras.addWidget(self.canva1)
        self.figuras.addWidget(self.canva2)

        self.contGraf.setLayout(self.figuras)

    def calculos(self):
        self.val_real=['a','b','c']
        self.val_pred=['1','2','3']

    def gen_informe(self):
        self.n_informe += 1
        self.informe = canvas.Canvas(f'Informe {self.n_informe}.pdf')
        self.informe.drawString(70,750, f'INFORME {self.n_informe}')
        self.informe.drawString(70,730, f'Dirección de la fuente de datos: {self.direc}')
        self.informe.drawString(70,710, f'N° datos: {self.n_dat}')
        self.informe.drawString(70,690, f'N° datos considerados para la creación de la ecuación: {self.n_dat_eleg}')
        self.informe.drawString(70,670, f'Ecuación obtenida por regresión: {self.ecu}')
        self.informe.drawString(70,650, 'Tabla de errores:')

        # Definir los datos de la tabla

        data = self.calculos(['1','2','3'],['a','b','c'])

        # Crear la tabla
        table = Table(data)

        # Establecer el estilo de la tabla
        style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)])

        table.setStyle(style)

        # Dibujar la tabla en el PDF
        table.wrapOn(self.informe, 0, 0)
        table.drawOn(self.informe, 200, 500)

        self.informe.save()

    def cambiar_direc(self):
        self.direc,a=QFileDialog.getOpenFileName(self, 'Abrir Archivo', '', 'Archivos (*.xlsx)')
        print(a)
        if self.direc != "":
            self.lDirec.setText(self.direc)
            print(self.lDirec.text())
            self.doc = pd.read_excel(self.direc)
            fila,columna = self.doc.shape
            self.n_dat = fila
            self.nDat1.setText(str(self.n_dat))
            self.nDat2.setText(str(self.n_dat))

            for i in range(fila):
                self.meses.append(self.doc.iloc[i,0][:3])
                self.consumo.append(int(self.doc.iloc[i,1]))
            self.grafica(self.meses,self.consumo,self.meses,self.consumo)



    def ir_pag(self):
        webbrowser.open_new_tab("https://programapython.github.io/ElectriCal/")



class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.gui = Aplicacion_Gui()

if __name__=='__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())


'''
#CODIGO ANTERIOR:

app=QApplication(sys.argv)
window=QWidget()
window.setWindowTitle("Calculadora de consumo eléctrico")

flag1=QLabel("Ingrese la dirección del archivo que contiene los datos:", window)
flag1.move(0,0)
flag1.adjustSize()
flag1.setStyleSheet("background-color:blue")

btn_import=QPushButton("Seleccionar archivo",window)
btn_import.move(0,20)


flag2=QLabel("GRÁFICA OBTENIDA", window)
flag2.move(200,200)
flag2.adjustSize()
flag2.setStyleSheet("background-color:red")

window.show()
app.exec()
'''
