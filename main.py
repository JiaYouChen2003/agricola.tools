from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QStyleFactory, QGridLayout, QMessageBox, QApplication
from PySide2.QtGui import QIcon

import sys
import search

class GUI(QWidget):
	def __init__(self, parent=None):
		super().__init__()
		self.setWindowTitle('agricola.tools')
		self.setWindowIcon(QIcon('raw_asset/agricola-en.jpg'))
		self.label1 = QLabel('URL:')
		self.line_edit = QLineEdit()
		self.label2 = QLabel('Results:')
		self.text = QTextEdit()
		self.button = QPushButton()
		self.button.setText('scrape')
		self.cmb = QComboBox()
		self.cmb.setStyle(QStyleFactory.create('Fusion'))
		self.cmb.addItem('4player_default')
		self.cmb.addItem('Default2')
		self.cmb.addItem('Default3')
		self.cmb.addItem('Default4')
		self.grid = QGridLayout()
		self.grid.setSpacing(12)
		self.grid.addWidget(self.label1, 1, 0)
		self.grid.addWidget(self.line_edit, 1, 1, 1, 38)
		self.grid.addWidget(self.button, 1, 39)
		self.grid.addWidget(self.label2, 2, 0)
		self.grid.addWidget(self.text, 2, 1, 1, 40)
		self.grid.addWidget(self.cmb, 1, 40)
		self.setLayout(self.grid)
		self.resize(600, 400)
		self.button.clicked.connect(self.inquiry)
		
	def inquiry(self):
		machine_search = search.SearchMachine()

		url = self.line_edit.text()
		game_type = self.getGameType()
		cards_info_arr = machine_search.getCardInfoList(url, game_type)
		self.text.setText('')
		for cards_info in cards_info_arr:
			self.text.append(cards_info[0].rjust(20) + ' ' +  ' '.join(cards_info[1:].rjust(5)))


	def getGameType(self):
		if self.cmb.currentIndex() == 0:
			return '4player_default'
		elif self.cmb.currentIndex() == 1:
			return '2'
		elif self.cmb.currentIndex() == 2:
			return '3'
		elif self.cmb.currentIndex() == 3:
			return '4'

if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = GUI()
	gui.show()
	sys.exit(app.exec_())