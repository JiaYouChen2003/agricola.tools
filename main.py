from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon

import sys
import search

class GUI(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('agricola.tools')
        self.setWindowIcon(QIcon('raw_asset/agricola-en.jpg'))
        self.label1_1 = QLabel('URL or')
        self.label1_2 = QLabel('Card Name:')
        self.line_edit = QLineEdit()
        self.label2 = QLabel('Results:')
        self.table = QTableWidget()
        self.button = QPushButton()
        self.button.setText('search')
        self.cmb = QComboBox()
        self.cmb.setStyle(QStyleFactory.create('Fusion'))
        self.game_type_list = ['4player_default', '4player_withAAS', '4player_banlist_500+', '4player_banlist_300-']
        self.cmb.addItem(self.game_type_list[0])
        self.cmb.addItem(self.game_type_list[1])
        self.cmb.addItem(self.game_type_list[2])
        self.cmb.addItem(self.game_type_list[3])
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label1_1, 1, 0)
        self.grid.addWidget(self.label1_2, 2, 0)
        self.grid.addWidget(self.line_edit, 1, 1, 2, 35)
        self.grid.addWidget(self.button, 1, 36)
        self.grid.addWidget(self.label2, 3, 0)
        self.grid.addWidget(self.table, 3, 1, 3, 35)
        self.grid.addWidget(self.cmb, 2, 36)
        self.setLayout(self.grid)
        self.resize(640, 810)
        self.button.clicked.connect(self.inquiry)

    def inquiry(self):
        if self.line_edit.text()[0:5] == 'https':
            self.inquiryUrl()
        else:
            self.inquiryCardName()

    def inquiryUrl(self):
        card_info_label = ["Card Name", "Card Rank", "Card Diff"]
        machine_search = search.SearchMachine()
        url = self.line_edit.text()
        game_type = self.getGameType()
        
        card_info_arr = machine_search.getCardInfoArr(url, game_type)
        self.setTableByArr(card_info_arr, card_info_label)

    def inquiryCardName(self):
        card_info_label = ["Card Name", "Card Rank", "Card Diff"]
        machine_search = search.SearchMachine()
        card_name = str(self.line_edit.text())
        
        card_rank = machine_search.getCardRank(card_name=card_name)
        card_diff = machine_search.getCardDiff(card_name=card_name)
        card_info = [[card_name, card_rank, card_diff]]
        self.setTableByArr(card_info, card_info_label)

    def getGameType(self):
        # 4player_default
        game_type = self.game_type_list[self.cmb.currentIndex()]
        return game_type

    def setTableByArr(self, arr, arr_label):
        self.table.setRowCount(len(arr))
        self.table.setColumnCount(len(arr[0]))
        self.table.setHorizontalHeaderLabels(arr_label)
        
        for i, arr_row in enumerate(arr):
            for j, item in enumerate(arr_row):
                self.setTableItem(item, i, j)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        
        for i in range(1, len(arr[0])):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def setTableItem(self, item, row, column):
        item = QTableWidgetItem(item)
        self.table.setItem(row, column, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())