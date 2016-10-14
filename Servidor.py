from PyQt4 import QtCore, QtGui, uic
import sys
from random import randint

class Snake():

	def __init__(self, color):
		self.color = color
		self.cuerpo = [[0,0],[1,0],[2,0]]
		self.tamaño = len(self.cuerpo)
		self.direccion = 'abajo'
		self.score = 0

class Servidor_Uso(QtGui.QMainWindow):
	
	def __init__(self):
		super(Servidor_Uso, self).__init__()
		uic.loadUi('Servidor.ui',self)
		self.resize(800,500)
		self.cuadricula()
		self.kfc = []
		self.serpientes = []
		self.empezo = False
		self.pausa = False
		self.timer_1 = None
		self.timer_2 = None
		self.timer_3 = None
		self.colorea_tabla()
		self.tableWidget.setSelectionMode(QtGui.QTableWidget.NoSelection)	
		self.spinBox.valueChanged.connect(self.set_timer)
		self.spinBox_3.valueChanged.connect(self.set_columnas_renglones)
		self.spinBox_2.valueChanged.connect(self.set_columnas_renglones)
		self.pushButton_2.clicked.connect(self.juego_comenzado)
		self.pushButton_3.clicked.connect(self.juego_terminado)
		self.pushButton_3.hide()
		self.show()

	def juego_comenzado(self):
		if not self.empezo:
			self.pushButton_3.show()
			parse = Snake([254,000,000])
			self.serpientes.append(parse)
			self.pushButton_2.setText("Pause")
			self.colorea_serpientes()
			self.timer_1 = QtCore.QTimer(self)
			self.timer_2 = QtCore.QTimer(self)
			self.timer_3 = QtCore.QTimer(self)
			self.timer_1.timeout.connect(self.avanza)
			self.timer_1.start(150) 
			self.timer_2.timeout.connect(self.comer)
			self.timer_2.start(150)	
			self.timer_3.timeout.connect(self.crea_kfc) 
			self.timer_3.start(3000) 
			self.tableWidget.installEventFilter(self)
			self.empezo = True 
		elif self.empezo and not self.pausa:
			self.timer_1.stop() 
			self.timer_1.stop()
			self.timer_2.stop()
			self.pausa = True
			self.pushButton_2.setText("Reanudar")
		elif self.pausa:
			self.timer_1.start()
			self.timer_2.start()
			self.timer_3.start()
			self.pausa = False 
			self.pushButton_2.setText("Pause")

	def juego_terminado(self):
		self.serpientes = [] 
		self.kfc = []
		self.timer_1.stop()
		self.timer_2.stop()
		self.timer_3.stop()
		self.empezo = False 
		self.pushButton_3.hide()
		self.pushButton_2.setText("Inicia Juego")
		self.colorea_tabla()

	def cuadricula(self):
		self.tableWidget.horizontalHeader().setResizeMode(QtGui.QHeaderView.Stretch)
		self.tableWidget.verticalHeader().setResizeMode(QtGui.QHeaderView.Stretch)

	def set_timer(self):
		self.timer.setInterval(self.spinBox.value())

	def eventFilter(self, source, event):
		if (event.type() == QtCore.QEvent.KeyPress and source is self.tableWidget):
			if (event.key() == QtCore.Qt.Key_Up and source is self.tableWidget):
				for serpiente in self.serpientes:
					if serpiente.direccion is not "abajo":
						serpiente.direccion = "arriba"
			elif (event.key() == QtCore.Qt.Key_Down and source is self.tableWidget):
				for serpiente in self.serpientes:
					if serpiente.direccion is not "arriba":
						serpiente.direccion = "abajo"
			elif (event.key() == QtCore.Qt.Key_Right and source is self.tableWidget):	
				for serpiente in self.serpientes:
					if serpiente.direccion is not "izquierda":
						serpiente.direccion = "derecha"
			elif (event.key() == QtCore.Qt.Key_Left and source is self.tableWidget):
				for serpiente in self.serpientes:
					if serpiente.direccion is not "derecha":
						serpiente.direccion = "izquierda"
		return QtGui.QMainWindow.eventFilter(self, source, event)

	def avanza(self):
		for serpiente in self.serpientes:
			if self.crash(serpiente):
				self.serpientes.remove(serpiente)
			self.tableWidget.item(serpiente.cuerpo[0][0],serpiente.cuerpo[0][1]).setBackground(QtGui.QColor(0,0,0))
			i = 0
			for cuadrito in serpiente.cuerpo[:-1]:
				i += 1
				cuadrito[0] = serpiente.cuerpo[i][0]
				cuadrito[1] = serpiente.cuerpo[i][1]
			if serpiente.direccion is "abajo":
				if serpiente.cuerpo[-1][0] + 1 < self.tableWidget.rowCount():
					serpiente.cuerpo[-1][0] += 1
				else:
					serpiente.cuerpo[-1][0] = 0
			if serpiente.direccion is "derecha":
				if serpiente.cuerpo[-1][1] + 1 < self.tableWidget.columnCount():
					serpiente.cuerpo[-1][1] += 1
				else:
					serpiente.cuerpo[-1][1] = 0
			if serpiente.direccion is "arriba":
				if serpiente.cuerpo[-1][0] != 0:
					serpiente.cuerpo[-1][0] -= 1
				else:
					serpiente.cuerpo[-1][0] = self.tableWidget.rowCount()-1
			if serpiente.direccion is "izquierda":
				if serpiente.cuerpo[-1][1] != 0:
					serpiente.cuerpo[-1][1] -= 1
				else:
					serpiente.cuerpo[-1][1] = self.tableWidget.columnCount()-1
		self.colorea_serpientes()
	
	def set_columnas_renglones(self):
		self.tableWidget.setRowCount(self.spinBox_3.value())
		self.tableWidget.setColumnCount(self.spinBox_2.value())
		self.colorea_tabla()

	def crea_kfc(self):
		optimo = False
		while not optimo: 
			i = randint(0, self.tableWidget.rowCount()-1) 
			j = randint(0, self.tableWidget.columnCount()-1)
			for serpiente in self.serpientes:
				if [i,j] in serpiente.cuerpo: 
					break
			optimo = True 
			self.kfc.append([i,j]) 
			self.tableWidget.item(i,j).setBackground(QtGui.QColor(255,255,255))

	def colorea_tabla(self):
		for i in range(self.tableWidget.rowCount()):
			for j in range(self.tableWidget.columnCount()):
				self.tableWidget.setItem(i,j, QtGui.QTableWidgetItem())
				self.tableWidget.item(i,j).setBackground(QtGui.QColor(0,0,0))
	
	def colorea_serpientes(self):
		for serpiente in self.serpientes:
			for c in serpiente.cuerpo:
				self.tableWidget.item(c[0], c[1]).setBackground(QtGui.QColor(serpiente.color[0], serpiente.color[1], serpiente.color[2]))
    

	def comer(self):
		for serpiente in self.serpientes:
			for pierna in self.kfc:
				if serpiente.cuerpo[-1][0] == pierna[0] and serpiente.cuerpo[-1][1] == pierna[1]:
					serpiente.score += 1
					serpiente.cuerpo.append([pierna[0],pierna[1]])
					self.kfc.remove(pierna)
					self.colorea_serpientes()
					return True	
		return False

	def crash(self, serpiente):
		for cuadrito in serpiente.cuerpo[0:len(serpiente.cuerpo)-2]:
			if serpiente.cuerpo[-1][0] == cuadrito[0] and serpiente.cuerpo[-1][1] == cuadrito[1]:
				return True
		return False

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	c = Servidor_Uso()
	sys.exit(app.exec_())

