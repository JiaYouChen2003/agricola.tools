from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import *

import sys
import time
import os.path
import json

from raw_asset.python_files import const_agricolatools
from raw_asset.python_files import inquiry
from raw_asset.python_files import analyze
from raw_asset.python_files import login


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
        
        self.machine_inquiry = inquiry.InquiryMachine()
        self.machine_analyze = analyze.AnalyzeMachine()
        
        self.start_thread_refresh = False
        self.need_auto_refresh = False
        
        self.setWindowTitle('agricola.tools')
        self.setWindowIcon(QIcon(const_agricolatools.ConstPath().window_icon_path))
        
        self.stacked_widget = QStackedWidget()
        self.login_page = QWidget()
        self.main_page = QWidget()
        
        # login page
        self.label_username = QLabel(const_agricolatools.QLABEL_USERNAME)
        self.label_password = QLabel(const_agricolatools.QLABEL_PASSWORD)
        self.label_auto_refresh = QLabel(const_agricolatools.QLABEL_AUTO_REFRESH)
        
        self.line_edit_URL = QLineEdit('')
        
        if os.path.isfile(const_agricolatools.ConstJsonFile().name_login_info):
            self.line_edit_username = QLineEdit(self.__getJsonFileValueByKey(const_agricolatools.ConstJsonFile().name_login_info,
                                                                            const_agricolatools.ConstJsonFile().key_login_info_username))
            self.line_edit_password = QLineEdit(self.__getJsonFileValueByKey(const_agricolatools.ConstJsonFile().name_login_info,
                                                                            const_agricolatools.ConstJsonFile().key_login_info_password))
        else:
            self.line_edit_username = QLineEdit('')
            self.line_edit_password = QLineEdit('')
        self.line_edit_password.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton()
        self.login_button.setText(const_agricolatools.TEXT_LOGIN_BUTTON)
        self.login_button.clicked.connect(self.__openMainPage)
        
        self.login_page_layout = QGridLayout()
        self.label_image = QLabel()
        self.label_image.setPixmap(QPixmap(const_agricolatools.ConstPath().login_page_img_path).scaled(600, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.login_page_layout.setSpacing(10)
        self.login_page_layout.addWidget(self.label_image, 0, 0, 1, 3)
        self.login_page_layout.addWidget(self.label_username, 1, 1, 1, 1)
        self.login_page_layout.addWidget(self.line_edit_username, 2, 1, 1, 1)
        self.login_page_layout.addWidget(self.label_password, 3, 1, 1, 1)
        self.login_page_layout.addWidget(self.line_edit_password, 4, 1, 1, 1)
        self.login_page_layout.addWidget(self.login_button, 5, 2, 1, 1)
        self.login_page.setLayout(self.login_page_layout)
        
        # main page
        self.label_URL_1 = QLabel(const_agricolatools.QLABEL_URL_1)
        self.label_URL_2 = QLabel(const_agricolatools.QLABEL_URL_2)
        self.label_result = QLabel(const_agricolatools.QLABEL_RESULT)
        self.label_print = QLabel('')
        
        self.table = QTableWidget()
        
        self.search_button = QPushButton()
        self.search_button.setText(const_agricolatools.TEXT_SEARCH_BUTTON)
        self.search_button.clicked.connect(self.startInquiry)
        
        self.cmb1 = QComboBox()
        self.cmb1.setStyle(QStyleFactory.create('Fusion'))
        self.game_type_list = const_agricolatools.GAME_TYPE_LIST
        self.cmb1.addItem(self.game_type_list[0])
        self.cmb1.addItem(self.game_type_list[1])
        self.cmb1.addItem(self.game_type_list[2])
        self.cmb1.addItem(self.game_type_list[3])
        self.cmb2 = QComboBox()
        self.cmb2.setStyle(QStyleFactory.create('Fusion'))
        self.auto_refresh_type_list = const_agricolatools.AUTO_REFRESH_LIST
        self.cmb2.addItem(self.auto_refresh_type_list[0])
        self.cmb2.addItem(self.auto_refresh_type_list[1])
        
        self.main_page_layout = QGridLayout()
        self.main_page_layout.setSpacing(10)
        self.main_page_layout.addWidget(self.label_URL_1, 1, 0)
        self.main_page_layout.addWidget(self.label_URL_2, 1, 0, 3, 0)
        self.main_page_layout.addWidget(self.label_result, 5, 0)
        
        self.main_page_layout.addWidget(self.line_edit_URL, 1, 3, 3, 33)
        self.main_page_layout.addWidget(self.table, 4, 1, 30, 35)
        
        self.main_page_layout.addWidget(self.search_button, 1, 36, 3, 2)
        self.main_page_layout.addWidget(self.label_print, 5, 36)
        self.main_page_layout.addWidget(self.cmb1, 30, 36)
        self.main_page_layout.addWidget(self.label_auto_refresh, 31, 36)
        self.main_page_layout.addWidget(self.cmb2, 32, 36)
        self.main_page.setLayout(self.main_page_layout)
        
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.main_page)
        
        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.stacked_widget)
        self.setLayout(self.main_layout)
    
    def __openMainPage(self):
        username = self.line_edit_username.text()
        password = self.line_edit_password.text()
        can_login = login.LoginMachine().checkCanLoginOrNot(driver=None, username=username, password=password)
        if can_login:
            self.stacked_widget.setCurrentIndex(1)
            self.resize(640, 810)
        else:
            self.label_image.setPixmap(QPixmap(const_agricolatools.ConstPath().login_page_cannot_login_img_path).scaled(600, 300, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
    
    def __getJsonFileValueByKey(self, json_file_name, key):
        with open(json_file_name, 'r') as json_file:
            json_dict = json.load(json_file)
            return json_dict[key]
    
    def __getGameType(self):
        # 4player_default
        game_type = self.game_type_list[self.cmb1.currentIndex()]
        return game_type
    
    def __getNeedAutoRefresh(self):
        # bool
        need_auto_refresh = self.cmb2.currentIndex()
        return need_auto_refresh
    
    def __setTableByArr(self, arr, arr_label, first_set=True, have_card_player=False):
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
        
        mean_list = []
        for i in range(card_info_arr[-1][3] + 1):
            mean_list.append(self.machine_analyze.getCardRankMean(card_info_arr=card_info_arr, player_num=i))
        
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
        self.label_print.setText(const_agricolatools.TEXT_END_AUTO_REFRESH)
        self.start_thread_refresh = False
    
    def __interruptThreadRefresh(self):
        self.label_print.setText(const_agricolatools.TEXT_INTERRUPT_AUTO_REFRESH)
        self.thread_refresh.requestInterruption()
        self.start_thread_refresh = False
    
    def __isLoginFailed(self, card_info_arr):
        # if login fail show cannot login
        card_cannot_login_name = const_agricolatools.ConstMessage().cannot_login
        
        if card_info_arr[0][0] == card_cannot_login_name:
            self.label_print.setText(const_agricolatools.MESSAGE_CANNOT_LOGIN)
            return True
        
        return False
    
    def __isDraftPhaseAndNotLogin(self, card_info_arr):
        # if still in draft phase and not login don't show info for all played cards(no card played)
        card_draftphase_name = const_agricolatools.ConstMessage().draftphase
        card_info_label = const_agricolatools.CARD_INFO_LABEL
        
        if card_info_arr[0][0] == card_draftphase_name:
            self.label_print.setText(const_agricolatools.MESSAGE_DRAFTPHASE)
            self.__setTableByArr(card_info_arr, card_info_label, first_set=(not self.start_thread_refresh))
            return True
        
        return False
    
    def startInquiry(self):
        if self.line_edit_URL.text()[0:5] == 'https':
            self.label_print.setText(const_agricolatools.TEXT_SEARCHING_WEBSITE)
            # use thread so that label print can be shown, not required
            # when thread end, start inquiry
            self.__startThreadToWaitThenInquiryByUrl()
        else:
            self.label_print.setText(const_agricolatools.TEXT_SEARCHING_CARD)
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
        
        # inquiry and get info for all played cards
        card_info_arr = self.machine_inquiry.inquiryByUrl(url, game_type=game_type, username=username, password=password, save_login_info=True)
        
        if self.__isLoginFailed(card_info_arr):
            return
        
        card_info_arr = sorted(card_info_arr, key=lambda x: int(x[1]))
        
        # if auto refresh is on but refresh thread did not start, start thread
        if self.need_auto_refresh and not self.start_thread_refresh:
            self.__startThreadRefresh()
        
        # show card info
        self.showCardInfoByArr(card_info_arr)
    
    def showCardInfoByArr(self, card_info_arr):
        # show search done
        self.label_print.setText(const_agricolatools.TEXT_SEARCHING_DONE)
        
        # title to show
        card_info_label = const_agricolatools.CARD_INFO_LABEL
        
        if self.__isDraftPhaseAndNotLogin(card_info_arr):
            return
        
        # analyze all played cards
        card_info_arr = self.__getAnalyzeOfCardInfoArr(card_info_arr)
        
        # show info for all played cards
        self.__setTableByArr(card_info_arr, card_info_label, first_set=(not self.start_thread_refresh), have_card_player=True)
    
    def startInquiryByCardName(self, card_name):
        # things need for inquiry
        game_type = self.__getGameType()
        
        # inquiry and get info for the card
        card_info = self.machine_inquiry.inquiryByCardName(card_name=card_name, game_type=game_type)
        
        # show the card exist or not
        if card_info[0][1] is None:
            self.label_print.setText(const_agricolatools.TEXT_CARD_CANNOT_FIND)
        else:
            self.label_print.setText(const_agricolatools.TEXT_CARD_SEARCHED)
        
        # title to show
        card_info_label = const_agricolatools.CARD_INFO_LABEL
        
        # show info for the card
        self.__setTableByArr(card_info, card_info_label)


if __name__ == '__main__':
    print('Do not close this terminal!!!')
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
