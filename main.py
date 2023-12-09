from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from PySide2.QtCore import *

import sys
import time

import search

CARD_INFO_LABEL = ["Card Name", "Card Rank", "Card Diff"]

class WorkerInquiryUrl(QObject):
    finished = Signal()
    
    def run(self):
        time.sleep(0.1)
        self.finished.emit()

class WorkerRefresh(QObject):
    finished = Signal()
    refresh = Signal()
    
    def run(self):
        for i in range(120):
            time.sleep(30)
            if (QThread.currentThread().isInterruptionRequested()):
                return
            self.refresh.emit()
        self.finished.emit()

class GUI(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.start_thread_refresh = False
        self.url = ''
        
        self.setWindowTitle('agricola.tools')
        self.setWindowIcon(QIcon('raw_asset/agricola-en.jpg'))
        
        self.label1_1 = QLabel('URL or')
        self.label1_2 = QLabel('Card Name:')
        self.label2 = QLabel('Results:')
        
        self.line_edit = QLineEdit()
        self.table = QTableWidget()
        self.button = QPushButton()
        
        self.button.setText('search')
        self.cmb1 = QComboBox()
        self.cmb1.setStyle(QStyleFactory.create('Fusion'))
        self.game_type_list = ['4player_default', '4player_withAAS', '4player_banlist_500+', '4player_banlist_300-']
        self.cmb1.addItem(self.game_type_list[0])
        self.cmb1.addItem(self.game_type_list[1])
        self.cmb1.addItem(self.game_type_list[2])
        self.cmb1.addItem(self.game_type_list[3])
        self.label_print = QLabel('')
        self.label3 = QLabel('Auto Refresh:')
        self.cmb2 = QComboBox()
        self.cmb2.setStyle(QStyleFactory.create('Fusion'))
        self.autorefresh_type_list = ['off', 'on']
        self.cmb2.addItem(self.autorefresh_type_list[0])
        self.cmb2.addItem(self.autorefresh_type_list[1])
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label1_1, 1, 0)
        self.grid.addWidget(self.label1_2, 1, 0, 3, 0)
        self.grid.addWidget(self.label2, 5, 0)
        
        self.grid.addWidget(self.line_edit, 1, 3, 3, 33)
        self.grid.addWidget(self.table, 4, 1, 30, 35)
        
        self.grid.addWidget(self.button, 1, 36, 3, 1)
        self.grid.addWidget(self.cmb1, 30, 36)
        self.grid.addWidget(self.label_print, 5, 36)
        self.grid.addWidget(self.label3, 31, 36)
        self.grid.addWidget(self.cmb2, 32, 36)
        self.setLayout(self.grid)
        self.resize(640, 810)
        self.button.clicked.connect(self.inquiry)

    def inquiry(self):
        if self.line_edit.text()[0:5] == 'https':
            self.label_print.setText('Searching Website...')
            # use thread so that label print can be shown, not required
            self.startThreadInquiryUrl()
        else:
            self.label_print.setText('Searching Card...')
            self.inquiryCardName()

    def startThreadInquiryUrl(self):
        self.thread_inquiry_url = QThread()
        self.worker = WorkerInquiryUrl()
        self.worker.moveToThread(self.thread_inquiry_url)
        
        self.thread_inquiry_url.started.connect(self.worker.run)
        
        self.worker.finished.connect(self.inquiryUrl)
        self.worker.finished.connect(self.thread_inquiry_url.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread_inquiry_url.finished.connect(self.thread_inquiry_url.deleteLater)
        self.thread_inquiry_url.start()

    def inquiryUrl(self):
        card_info_label = CARD_INFO_LABEL
        machine_search = search.SearchMachine()
        if self.url == '':
            self.url = self.line_edit.text()
        game_type = self.getGameType()
        need_auto_refresh = self.getNeedAutoRefresh()
        
        if not need_auto_refresh and self.start_thread_refresh:
            self.interruptThreadRefresh()
            return
        
        card_info_arr = machine_search.getCardInfoArr(self.url, game_type)
        if card_info_arr[0][0] == 'Still in Draft Phase':
            self.label_print.setText('Still in Draft Phase')
            return
        
        self.label_print.setText('Searching Done!')
        self.setTableByArr(card_info_arr, card_info_label, first_set=(not self.start_thread_refresh))
        
        if need_auto_refresh and not self.start_thread_refresh:
            self.startThreadRefresh()

    def startThreadRefresh(self):
        self.start_thread_refresh = True
        self.thread_refresh = QThread()
        self.worker = WorkerRefresh()
        self.worker.moveToThread(self.thread_refresh)
        
        self.thread_refresh.started.connect(self.worker.run)
        
        self.worker.refresh.connect(self.inquiryUrl)
        
        self.worker.finished.connect(self.endThreadRefresh)
        self.worker.finished.connect(self.thread_refresh.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread_refresh.finished.connect(self.thread_refresh.deleteLater)
        self.thread_refresh.start()
        self.label_print.setText('AutoRefreshStart')

    def endThreadRefresh(self):
        self.start_thread_refresh = False
        self.label_print.setText('AutoRefreshEnd')

    def interruptThreadRefresh(self):
        self.thread_refresh.requestInterruption()
        self.label_print.setText('AutoRefreshInterrupted')

    def inquiryCardName(self):
        card_info_label = CARD_INFO_LABEL
        machine_search = search.SearchMachine()
        card_name = str(self.line_edit.text())
        
        card_rank = machine_search.getCardRank(card_name=card_name)
        card_diff = machine_search.getCardDiff(card_name=card_name)
        card_info = [[card_name, card_rank, card_diff]]
        self.setTableByArr(card_info, card_info_label)
        if card_rank == None:
            self.label_print.setText('Cannot Found Card :(')        
        else:
            self.label_print.setText('Card Searched!')

    def getGameType(self):
        # 4player_default
        game_type = self.game_type_list[self.cmb1.currentIndex()]
        return game_type

    def getNeedAutoRefresh(self):
        # bool
        need_auto_refresh = self.cmb2.currentIndex()
        return need_auto_refresh

    def setTableByArr(self, arr, arr_label, first_set = True):
        self.table.setRowCount(len(arr))
        if first_set:
            self.table.setColumnCount(len(arr[0]))
            self.table.setHorizontalHeaderLabels(arr_label)
        
        for i, arr_row in enumerate(arr):
            for j, item in enumerate(arr_row):
                self.setTableItem(item, i, j)
        
        if first_set:
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