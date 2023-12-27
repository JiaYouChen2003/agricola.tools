from PySide2.QtCore import *

import const_agricolatools
import search

class InquiryMachine():
    def inquiryByUrl(self, url, game_type = const_agricolatools.GAME_TYPE_LIST[0], username = '', password = ''):
        machine_search = search.SearchMachine()
        
        card_info_arr = machine_search.getCardInfoArr(url, game_type=game_type, username=username, password=password)
        
        # may get a fake card that has some message
        card_draftphase_name = const_agricolatools.ConstMessage().draftphase
        if card_info_arr[0][0] == card_draftphase_name:
            return [[card_draftphase_name]]
        
        return card_info_arr
    
    def inquiryByCardName(self, card_name, game_type = const_agricolatools.GAME_TYPE_LIST[0]):
        machine_search = search.SearchMachine()
        
        card_rank = machine_search.getCardRank(card_name=card_name, game_type=game_type)
        card_diff = machine_search.getCardDiff(card_name=card_name)
        card_info = [[card_name, card_rank, card_diff]]
        
        return card_info