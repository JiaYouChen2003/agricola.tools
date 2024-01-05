from PySide2.QtCore import *

import const_agricolatools
import search

class InquiryMachine():
    def __init__(self):
        self.machine_search = search.SearchMachine()
    
    def inquiryByUrl(self, url, game_type = const_agricolatools.GAME_TYPE_LIST[0], username = '', password = ''):
        '''
        card_info = [card_name, card_rank, card_diff, card_player_num]
        '''
        
        card_info_arr = self.machine_search.getCardInfoArr(url, game_type=game_type, username=username, password=password)
        
        # may get a fake card that has some message
        possible_message_card_name_list = const_agricolatools.ConstMessage().all_message
        for possible_message_card_name in possible_message_card_name_list:
            if card_info_arr[0][0] == possible_message_card_name:
                return [[possible_message_card_name]]
        
        return card_info_arr
    
    def inquiryByCardName(self, card_name, game_type = const_agricolatools.GAME_TYPE_LIST[0]):
        card_rank = self.machine_search.getCardRank(card_name=card_name, game_type=game_type)
        card_diff = self.machine_search.getCardDiff(card_name=card_name)
        card_info = [[card_name, card_rank, card_diff]]
        
        return card_info