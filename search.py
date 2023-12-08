import openpyxl
import scrape
import os

class SearchMachine():
    def __init__(self):
        PATH = os.path.abspath('./raw_asset/card_statistic/Jul_2023/agricola_statistic.xlsx')
        self.xlsx_name = PATH
        self.workbook_list = openpyxl.load_workbook(self.xlsx_name)

    def __getValuesFromSheet(self, sheet):
        arr = []
        for row in sheet:
            list = []
            for column in row:
                list.append(str(column.value).strip())
            arr.append(list)
        return arr

    def __getItemIndexByNameFromArray(self, itemName, arr, column4name, column4index):
        for row in arr:
            if row[column4name] == itemName:
                return row[column4index]
    
    # Functions that can be called
    def getCardInfoArr(self, url, game_type):
        card_info_arr = []

        machine_scrape = scrape.ScrapeMachine()
        card_name_list = machine_scrape.getCardListFromBGA(url=url)
    
        for card in card_name_list:
            card_name = card.text
            card_rank = self.getCardRank(card_name=card_name, game_type=game_type)
            card_diff = self.getCardDiff(card_name=card_name)
            
            card_info_list = [card_name, card_rank, card_diff]
            card_info_arr.append(card_info_list)
        return card_info_arr
    
    def getCardRank(self, card_name, game_type = '4player_default'):
        workbook_list = self.workbook_list
        
        arr_rank = self.__getValuesFromSheet(workbook_list[game_type])
        card_rank = self.__getItemIndexByNameFromArray(card_name, arr_rank, 1, 0)
        return card_rank

    def getCardDiff(self, card_name):
        workbook_list = self.workbook_list

        arr_diff = self.__getValuesFromSheet(workbook_list['Diff'])
        card_diff = self.__getItemIndexByNameFromArray(card_name, arr_diff, 0, 3)
        return card_diff


if __name__ == '__main__':
    machine_search = SearchMachine()
    machine_scrape = scrape.ScrapeMachine()

    card_name_list = machine_scrape.getCardListFromBGA()
    
    print()
    print("Name".rjust(20), "Rank".rjust(5), "Diff".rjust(5))
    for card in card_name_list:
        card_name = card.text
        card_rank = machine_search.getCardRank(card_name=card_name)
        card_diff = machine_search.getCardDiff(card_name=card_name)

        print(card_name.rjust(20), str(card_rank).rjust(5), str(card_diff).rjust(5))
    