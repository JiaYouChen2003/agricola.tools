import openpyxl

import const_agricolatools
import scrape

class SearchMachine():
    def __init__(self):
        self.xlsx_name = const_agricolatools.XLSXPATH
        self.workbook_list = openpyxl.load_workbook(self.xlsx_name)

    def __getValuesFromSheet(self, sheet):
        arr = []
        for row in sheet:
            list = []
            for column in row:
                list.append(str(column.value).strip())
            arr.append(list)
        return arr

    def __getItemIndexByNameFromArray(self, itemName, arr, column4name, column4index, wantcasefold = False):
        for row in arr:
            if wantcasefold:
                if row[column4name].casefold() == itemName.casefold():
                    return row[column4index]
            else:
                if row[column4name] == itemName:
                    return row[column4index]
    
    # Functions that can be called
    def getCardInfoArr(self, url, game_type = const_agricolatools.GAME_TYPE_LIST[0]):
        card_info_arr = []
        
        machine_scrape = scrape.ScrapeMachine()
        # if still in draft phase, return fake card that say still in draft phase
        card_name_list = machine_scrape.getCardListFromBGA(url=url)
        
        for card in card_name_list:
            card_name = card.text
            card_rank = self.getCardRank(card_name=card_name, game_type=game_type)
            card_diff = self.getCardDiff(card_name=card_name)
            
            card_info_list = [card_name, card_rank, card_diff]
            card_info_arr.append(card_info_list)
        return card_info_arr
    
    def getCardRank(self, card_name, game_type = const_agricolatools.GAME_TYPE_LIST[0]):
        workbook_list = self.workbook_list
        
        arr_rank = self.__getValuesFromSheet(workbook_list[game_type])
        card_rank = self.__getItemIndexByNameFromArray(card_name, arr_rank, 1, 0, wantcasefold=True)
        return card_rank

    def getCardDiff(self, card_name):
        workbook_list = self.workbook_list
        
        arr_diff = self.__getValuesFromSheet(workbook_list[const_agricolatools.WORKBOOK_DIFF_NAME])
        card_diff = self.__getItemIndexByNameFromArray(card_name, arr_diff, 0, 3, wantcasefold=True)
        return card_diff

# test code
if __name__ == '__main__':
    machine_search = SearchMachine()
    machine_scrape = scrape.ScrapeMachine()
    
    card_name_list = machine_scrape.getCardListFromBGA()
    
    card_draftphase_name = const_agricolatools.ConstMessage().draftphase
    if card_name_list[0].text == card_draftphase_name:
        print('Now in Draft Phase')
        exit()
    
    print()
    print("Name".rjust(20), "Rank".rjust(5), "Diff".rjust(5))
    for card in card_name_list:
        card_name = card.text
        card_rank = machine_search.getCardRank(card_name=card_name)
        card_diff = machine_search.getCardDiff(card_name=card_name)
        
        print(card_name.rjust(20), str(card_rank).rjust(5), str(card_diff).rjust(5))