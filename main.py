from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from PySide2.QtCore import *

import sys
import time

sys.path.append('./python_files')
import const_agricolatools
import inquiry
import analyze

class WorkerWaitToShowThings(QObject):
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
        
        self.setWindowTitle('agricola.tools')
        self.setWindowIcon(QIcon(const_agricolatools.WINDOW_ICON_PATH))
        
        self.label1_1 = QLabel('URL or')
        self.label1_2 = QLabel('Card Name:')
        self.label2 = QLabel('Results:')
        
        self.line_edit = QLineEdit()
        self.table = QTableWidget()
        self.button = QPushButton()
        
        self.button.setText('search')
        self.cmb1 = QComboBox()
        self.cmb1.setStyle(QStyleFactory.create('Fusion'))
        self.game_type_list = const_agricolatools.GAME_TYPE_LIST
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
        self.button.clicked.connect(self.startInquiry)
    
    def __getGameType(self):
        # 4player_default
        game_type = self.game_type_list[self.cmb1.currentIndex()]
        return game_type
    
    def __getNeedAutoRefresh(self):
        # bool
        need_auto_refresh = self.cmb2.currentIndex()
        return need_auto_refresh
    
    def __setTableByArr(self, arr, arr_label, first_set = True):
        self.table.setRowCount(len(arr))
        if first_set:
            self.table.setColumnCount(len(arr[0]))
            self.table.setHorizontalHeaderLabels(arr_label)
        
        for i, arr_row in enumerate(arr):
            for j, item in enumerate(arr_row):
                self.__setTableItem(item, i, j)
        
        if first_set:
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            
            for i in range(1, len(arr[0])):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
    
    def __setTableItem(self, item, row, column):
        item = QTableWidgetItem(item)
        self.table.setItem(row, column, item)
    
    def __getAnalyzeOfCardInfoArr(card_info_arr):
        machine_analyze = analyze.AnalyzeMachine
        
        mean = []
        for i in range(card_info_arr[-1][3]):
            mean.append(machine_analyze.getCardRankMean(card_info_arr=card_info_arr, player_num=i))
        
        player_num = 0
        for card_info in card_info_arr:
            if card_info[3] == (player_num + 1):
                card_info_arr.insert(['mean: ', mean[player_num], None, None])
                player_num += 1
            else:
                continue
        return card_info_arr
    
    def __startThreadToWaitThenInquiryByUrl(self):
        # initial thread and what to run while thread running
        self.thread_wait = QThread()
        self.worker_wait = WorkerWaitToShowThings()
        self.worker_wait.moveToThread(self.thread_wait)
        self.thread_wait.started.connect(self.worker_wait.run)
        
        # finish wait thread, start inquiry
        self.worker_wait.finished.connect(self.startInquiryByUrl())
        # delete thread
        self.worker_wait.finished.connect(self.thread_wait.quit)
        self.worker_wait.finished.connect(self.worker_wait.deleteLater)
        self.thread_wait.finished.connect(self.thread_wait.deleteLater)
        self.thread_wait.start()
    
    def __startThreadRefresh(self):
        self.label_print.setText('Start Auto Refresh')
        self.start_thread_refresh = True
        self.thread_refresh = QThread()
        self.worker_refresh = WorkerRefresh()
        self.worker_refresh.moveToThread(self.thread_refresh)
        
        self.thread_refresh.started.connect(self.worker_refresh.run)
        
        self.worker_refresh.refresh.connect(self.startInquiryByUrl)
        
        self.worker_refresh.finished.connect(self.__endThreadRefresh)
        self.worker_refresh.finished.connect(self.thread_refresh.quit)
        self.worker_refresh.finished.connect(self.worker_refresh.deleteLater)
        self.thread_refresh.finished.connect(self.thread_refresh.deleteLater)
        self.thread_refresh.start()
    
    def __endThreadRefresh(self):
        self.label_print.setText('End Auto Refresh')
        self.start_thread_refresh = False
    
    def __interruptThreadRefresh(self):
        self.label_print.setText('Interrupt Refresh!')
        self.thread_refresh.requestInterruption()
        self.start_thread_refresh = False
    
    def startInquiry(self):
        if self.line_edit.text()[0:5] == 'https':
            self.label_print.setText('Searching Website...')
            # use thread so that label print can be shown, not required
            # when thread end, start inquiry
            self.__startThreadToWaitThenInquiryByUrl()
        else:
            self.label_print.setText('Searching Card...')
            self.startInquiryByCardName(card_name=self.line_edit.text())
    
    def startInquiryByUrl(self):
        # if auto refresh is off but refresh thread is start, interrupt thread
        need_auto_refresh = self.__getNeedAutoRefresh()
        if not need_auto_refresh and self.start_thread_refresh:
            self.__interruptThreadRefresh()
            return
        
        # things need for inquiry
        url = self.line_edit.text()
        machine_inquiry = inquiry.InquiryMachine()
        game_type = self.__getGameType()
        
        # inquiry and get info for all played cards
        card_info_arr = machine_inquiry.inquiryByUrl(url=url, game_type=game_type)
        
        # title to show
        card_info_label = const_agricolatools.CARD_INFO_LABEL
        self.label_print.setText('Searching Done!')
        
        # if still in draft phase don't show info for all played cards(no card played)
        card_draftphase_name = const_agricolatools.ConstMessage().draftphase
        if card_info_arr[0][0] == card_draftphase_name:
            self.label_print.setText(card_draftphase_name)
            self.__setTableByArr(card_info_arr, card_info_label, first_set=(not self.start_thread_refresh))
            return
        
        # analyze all played cards
        card_info_arr = self.__getAnalyzeOfCardInfoArr(card_info_arr)
        
        # show info for all played cards
        self.__setTableByArr(card_info_arr, card_info_label, first_set=(not self.start_thread_refresh))
        
        # if auto refresh is on but refresh thread did not start, start thread
        if need_auto_refresh and not self.start_thread_refresh:
            self.__startThreadRefresh()
    
    def startInquiryByCardName(self, card_name):
        # things need for inquiry
        machine_inquiry = inquiry.InquiryMachine()
        game_type = self.__getGameType()
        
        # inquiry and get info for the card
        card_info = machine_inquiry.inquiryByCardName(card_name=card_name, game_type=game_type)
        
        # title to show
        card_info_label = const_agricolatools.CARD_INFO_LABEL
        if card_info[0][1] == None:
            self.label_print.setText('Cannot Found Card :(')
        else:
            self.label_print.setText('Card Searched!')
        
        # show info for the card
        self.__setTableByArr(card_info, card_info_label)

if __name__ == '__main__':
    print(const_agricolatools.CARD_INFO_LABEL)
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())