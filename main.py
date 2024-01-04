from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon
from PySide2.QtCore import *

import sys
import time

sys.path.append('./raw_asset/python_files')
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
        self.need_auto_refresh = False
        
        self.setWindowTitle('agricola.tools')
        self.setWindowIcon(QIcon(const_agricolatools.WINDOW_ICON_PATH))
        
        self.label_URL_1 = QLabel(const_agricolatools.QLABEL_URL_1)
        self.label_URL_2 = QLabel(const_agricolatools.QLABEL_URL_2)
        self.label_result = QLabel(const_agricolatools.QLABEL_RESULT)
        self.label_print = QLabel('')
        self.label_username = QLabel(const_agricolatools.QLABEL_USERNAME)
        self.label_password = QLabel(const_agricolatools.QLABEL_PASSWORD)
        self.label_auto_refresh = QLabel(const_agricolatools.QLABEL_AUTO_REFRESH)
        
        self.line_edit_URL = QLineEdit()
        self.line_edit_username = QLineEdit()
        self.line_edit_password = QLineEdit()
        
        self.table = QTableWidget()
        
        self.button = QPushButton()
        self.button.setText(const_agricolatools.SEARCH_BUTTON_TEXT)
        
        self.cmb1 = QComboBox()
        self.cmb1.setStyle(QStyleFactory.create('Fusion'))
        self.game_type_list = const_agricolatools.GAME_TYPE_LIST
        self.cmb1.addItem(self.game_type_list[0])
        self.cmb1.addItem(self.game_type_list[1])
        self.cmb1.addItem(self.game_type_list[2])
        self.cmb1.addItem(self.game_type_list[3])
        self.cmb2 = QComboBox()
        self.cmb2.setStyle(QStyleFactory.create('Fusion'))
        self.auto_refresh_type_list = const_agricolatools.AUTO_REFRESH_TEXT
        self.cmb2.addItem(self.auto_refresh_type_list[0])
        self.cmb2.addItem(self.auto_refresh_type_list[1])
        
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.addWidget(self.label_URL_1, 1, 0)
        self.grid.addWidget(self.label_URL_2, 1, 0, 3, 0)
        self.grid.addWidget(self.label_result, 5, 0)
        
        self.grid.addWidget(self.line_edit_URL, 1, 3, 3, 33)
        self.grid.addWidget(self.table, 4, 1, 30, 35)
        
        self.grid.addWidget(self.button, 1, 36, 3, 1)
        self.grid.addWidget(self.label_print, 5, 36)
        self.grid.addWidget(self.label_username, 25, 36)
        self.grid.addWidget(self.line_edit_username, 26, 36)
        self.grid.addWidget(self.label_password, 27, 36)
        self.grid.addWidget(self.line_edit_password, 28, 36)
        self.grid.addWidget(self.cmb1, 30, 36)
        self.grid.addWidget(self.label_auto_refresh, 31, 36)
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
    
    def __setTableByArr(self, arr, arr_label, first_set = True, have_card_player = False):
        self.table.setRowCount(len(arr))
        if first_set:
            if have_card_player:
                self.table.setColumnCount(len(arr[0]) - 1)
            else:
                self.table.setColumnCount(len(arr[0]))
            self.table.setHorizontalHeaderLabels(arr_label)
        
        for i, arr_row in enumerate(arr):
            for j, item in enumerate(arr_row):
                self.__setTableItem(item, i, j)
        
        if first_set:
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Stretch)
            
            for i in range(1, self.table.columnCount()):
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
    
    def __setTableItem(self, item, row, column):
        item = QTableWidgetItem(item)
        self.table.setItem(row, column, item)
    
    def __getAnalyzeOfCardInfoArr(self, card_info_arr):
        machine_analyze = analyze.AnalyzeMachine()
        
        mean_list = []
        for i in range(card_info_arr[-1][3] + 1):
            mean_list.append(machine_analyze.getCardRankMean(card_info_arr=card_info_arr, player_num=i))
        
        card_info_arr.insert(0, [const_agricolatools.CARD_PLAYER_LABEL + const_agricolatools.CARD_PLAYER_LABEL_ALL, None, None, None])
        card_info_arr.insert(1, [const_agricolatools.CARD_MEAN_LABEL, str(mean_list[0]), None, None])
        player_num = 1
        for card_num, card_info in enumerate(card_info_arr):
            if card_info[3] == player_num:
                card_info_arr.insert(card_num + 1, [const_agricolatools.CARD_MEAN_LABEL, str(mean_list[player_num]), None, None])
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
        self.label_print.setText(const_agricolatools.END_AUTO_REFRESH_TEXT)
        self.start_thread_refresh = False
    
    def __interruptThreadRefresh(self):
        self.label_print.setText(const_agricolatools.INTERRUPT_AUTO_REFRESH_TEXT)
        self.thread_refresh.requestInterruption()
        self.start_thread_refresh = False
    
    def startInquiry(self):
        if self.line_edit_URL.text()[0:5] == 'https':
            self.label_print.setText(const_agricolatools.SEARCHING_WEBSITE_TEXT)
            # use thread so that label print can be shown, not required
            # when thread end, start inquiry
            self.__startThreadToWaitThenInquiryByUrl()
        else:
            self.label_print.setText(const_agricolatools.SEARCHING_CARD_TEXT)
            self.startInquiryByCardName(card_name=self.line_edit_URL.text())
    
    def startInquiryByUrl(self):
        # if auto refresh is off but refresh thread is start, interrupt thread
        self.need_auto_refresh = self.__getNeedAutoRefresh()
        if not self.need_auto_refresh and self.start_thread_refresh:
            self.__interruptThreadRefresh()
            return
        
        # things need for inquiry
        url = self.line_edit_URL.text()
        game_type = self.__getGameType()
        username = self.line_edit_username.text()
        password = self.line_edit_password.text()
        machine_inquiry = inquiry.InquiryMachine()
        
        # inquiry and get info for all played cards
        card_info_arr = machine_inquiry.inquiryByUrl(url, game_type=game_type, username=username, password=password)
        
        # if login fail show cannot login
        card_cannot_login_name = const_agricolatools.ConstMessage().cannot_login
        if card_info_arr[0][0] == card_cannot_login_name:
            self.label_print.setText(const_agricolatools.MESSAGE_CANNOT_LOGIN)
            return
        
        # if auto refresh is on but refresh thread did not start, start thread
        if self.need_auto_refresh and not self.start_thread_refresh:
            self.__startThreadRefresh()
        
        # show card info
        self.showCardInfoByArr(card_info_arr)
    
    def showCardInfoByArr(self, card_info_arr):
        # title to show
        card_info_label = const_agricolatools.CARD_INFO_LABEL
        self.label_print.setText(const_agricolatools.SEARCHING_DONE_TEXT)
        
        # if still in draft phase and not login don't show info for all played cards(no card played)
        card_draftphase_name = const_agricolatools.ConstMessage().draftphase
        if card_info_arr[0][0] == card_draftphase_name:
            self.label_print.setText(const_agricolatools.MESSAGE_DRAFTPHASE)
            self.__setTableByArr(card_info_arr, card_info_label, first_set=(not self.start_thread_refresh))
            return
        
        # analyze all played cards
        card_info_arr = self.__getAnalyzeOfCardInfoArr(card_info_arr)
        
        # show info for all played cards
        self.__setTableByArr(card_info_arr, card_info_label, first_set=(not self.start_thread_refresh), have_card_player=card_info_arr[-1][3])
    
    def startInquiryByCardName(self, card_name):
        # things need for inquiry
        machine_inquiry = inquiry.InquiryMachine()
        game_type = self.__getGameType()
        
        # inquiry and get info for the card
        card_info = machine_inquiry.inquiryByCardName(card_name=card_name, game_type=game_type)
        
        # title to show
        card_info_label = const_agricolatools.CARD_INFO_LABEL
        if card_info[0][1] == None:
            self.label_print.setText(const_agricolatools.CARD_CANNOT_FIND_TEXT)
        else:
            self.label_print.setText(const_agricolatools.CARD_SEARCHED_TEXT)
        
        # show info for the card
        self.__setTableByArr(card_info, card_info_label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())