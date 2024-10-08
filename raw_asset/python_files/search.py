import openpyxl

from raw_asset.python_files import const_agricolatools
from raw_asset.python_files import scrape
from raw_asset.python_files import save


class SearchMachine():
    def __init__(self):
        self.machine_scrape = None
        
        self.xlsx_name = const_agricolatools.ConstPath().xlsx_path
        self.workbook_list = openpyxl.load_workbook(self.xlsx_name)
        
        self.player_num = 0
    
    def __getCardNameAndPlayerNum(self, card):
        card_name = card.text
        
        if card.size['height'] < 30:
            self.player_num += 1
            card_name = const_agricolatools.CARD_PLAYER_LABEL + str(self.player_num)
        card_player_num = self.player_num
        
        return card_name, card_player_num
    
    def __getValuesFromSheet(self, sheet):
        arr = []
        for row in sheet:
            list = []
            for column in row:
                list.append(str(column.value).strip())
            arr.append(list)
        return arr
    
    def __getItemIndexByNameFromArray(self, itemName, arr, column4name, column4index, wantcasefold=False):
        for row in arr:
            if wantcasefold:
                if row[column4name].casefold() == itemName.casefold():
                    return row[column4index]
            else:
                if row[column4name] == itemName:
                    return row[column4index]
    
    # Functions that can be called
    def getCardInfoArr(self, url, game_type=const_agricolatools.GAME_TYPE_LIST[0], username='', password='', save_login_info=True):
        '''
        card_info = [card_name, card_rank, card_diff, card_player_num]
        '''
        if self.machine_scrape is None:
            self.machine_scrape = scrape.ScrapeMachine()
        
        # may get a fake card that has some message
        card_list = self.machine_scrape.getCardListFromBGA(url=url, username=username, password=password, save_login_info=save_login_info)
        
        if card_list[0] == const_agricolatools.ConstMessage().draftphase and len(card_list) == 3:
            _, card_list, hand_list = card_list
            card_info_arr = self.getCardInfoArrFromCardNameList(card_list=card_list, game_type=game_type)
            hand_info_arr = self.getCardInfoArrFromCardNameList(card_list=hand_list, game_type=game_type)
            card_info_arr.append([const_agricolatools.CARD_HAND_LABEL, None, None, 0])
            if len(hand_info_arr) != 0:
                card_info_arr.extend(hand_info_arr)
            return card_info_arr
        
        return self.getCardInfoArrFromCardNameList(card_list=card_list, game_type=game_type)
    
    def getCardInfoArrFromCardNameList(self, card_list, game_type=const_agricolatools.GAME_TYPE_LIST[0]):
        '''
        card_info = [card_name, card_rank, card_diff, card_player_num]
        '''
        card_info_arr = []
        self.player_num = 0
        
        # get card rank, diff and card player
        for card in card_list:
            card_name, card_player_num = self.__getCardNameAndPlayerNum(card=card)
            card_rank = self.getCardRank(card_name=card_name, game_type=game_type)
            card_diff = self.getCardDiff(card_name=card_name)
            
            if (card == card_list[0]):
                save.saveCardToJSON(card_name, card_rank, card_diff, new_file=True)
            else:
                save.saveCardToJSON(card_name, card_rank, card_diff)
            
            card_info = [card_name, card_rank, card_diff, card_player_num]
            card_info_arr.append(card_info)
        
        return card_info_arr
    
    def getCardRank(self, card_name, game_type=const_agricolatools.GAME_TYPE_LIST[0]):
        workbook_list = self.workbook_list
        
        arr_rank = self.__getValuesFromSheet(workbook_list[game_type])
        card_rank = self.__getItemIndexByNameFromArray(card_name, arr_rank, 1, 0, wantcasefold=True)
        return card_rank
    
    def getCardDiff(self, card_name):
        workbook_list = self.workbook_list
        
        arr_diff = self.__getValuesFromSheet(workbook_list[const_agricolatools.ConstPath().xlsx_workbook_diff_name])
        card_diff = self.__getItemIndexByNameFromArray(card_name, arr_diff, 0, 3, wantcasefold=True)
        return card_diff


# test code
if __name__ == '__main__':
    assert False, 'search.py should not be executed'
