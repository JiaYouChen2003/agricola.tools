from PySide2.QtWidgets import *
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
		self.table = QTableWidget()
		self.button = QPushButton()
		self.button.setText('scrape')
		self.cmb = QComboBox()
		self.cmb.setStyle(QStyleFactory.create('Fusion'))
		self.game_type_list = ['4player_default', '4player_withAAS', '4player_banlist_500+', '4player_banlist_300-']
		self.cmb.addItem(self.game_type_list[0])
		self.cmb.addItem(self.game_type_list[1])
		self.cmb.addItem(self.game_type_list[2])
		self.cmb.addItem(self.game_type_list[3])
		self.grid = QGridLayout()
		self.grid.setSpacing(12)
		self.grid.addWidget(self.label1, 1, 0, 2, 0)
		self.grid.addWidget(self.line_edit, 1, 1, 2, 35)
		self.grid.addWidget(self.button, 1, 36)
		self.grid.addWidget(self.label2, 3, 0)
		self.grid.addWidget(self.table, 3, 1, 3, 35)
		self.grid.addWidget(self.cmb, 2, 36)
		self.setLayout(self.grid)
		self.resize(300, 800)
		self.button.clicked.connect(self.inquiry)
		
	def inquiry(self):
		machine_search = search.SearchMachine()

		url = self.line_edit.text()
		game_type = self.getGameType()
		card_info_arr = machine_search.getCardInfoArr(url, game_type)

		self.table.setRowCount(len(card_info_arr))
		self.table.setColumnCount(len(card_info_arr[0]))
		self.table.setHorizontalHeaderLabels(["Card Name", "Card Rank", "Card Diff"])

		for i, [card_name, card_rank, card_diff] in enumerate(card_info_arr):
			self.setTableItem(card_name, i, 0)
			self.setTableItem(card_rank, i, 1)
			self.setTableItem(card_diff, i, 2)
		header = self.table.horizontalHeader()
		header.setSectionResizeMode(0, QHeaderView.Stretch)
		header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
		header.setSectionResizeMode(2, QHeaderView.ResizeToContents)

	def getGameType(self):
		# 4player_default
		game_type = self.game_type_list[self.cmb.currentIndex()]
		return game_type
	
	def setTableItem(self, item, row, column):
		item = QTableWidgetItem(item)
		self.table.setItem(row, column, item)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	gui = GUI()
	gui.show()
	sys.exit(app.exec_())