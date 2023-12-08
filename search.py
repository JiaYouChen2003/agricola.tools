import openpyxl
import scrape
import os

def getValuesFromSheet(sheet):
    arr = []
    for row in sheet:
        arr2 = []
        for column in row:
            arr2.append(str(column.value).strip())
        arr.append(arr2)
    return arr

def getItemIndexByNameFromArray(itemName, arr, column4name, column4index):
    for row in arr:
        if row[column4name] == itemName:
            return row[column4index]

class SearchMachine():
    def __init__(self):
        PATH = os.path.abspath('./raw_asset/card_statistic/Jul_2023/agricola_statistic.xlsx')
        self.xlsx_name = PATH
        self.workbook_list = openpyxl.load_workbook(self.xlsx_name)
    
    def getCardRank(self, card_name, game_type = '4player_default'):
        workbook_list = self.workbook_list
        
        arr_rank = getValuesFromSheet(workbook_list[game_type])
        card_rank = getItemIndexByNameFromArray(card_name, arr_rank, 1, 0)
        return card_rank

    def getCardDiff(self, card_name):
        workbook_list = self.workbook_list

        arr_diff = getValuesFromSheet(workbook_list['Diff'])
        card_diff = getItemIndexByNameFromArray(card_name, arr_diff, 0, 3)
        return card_diff


if __name__ == '__main__':
    machine_search = SearchMachine()
    machine_scrape = scrape.ScrapeMachine()

    xlsx_name = machine_search.xlsx_name
    card_name_list = machine_scrape.getCardListFromBGA()
    
    print()
    print("Name".rjust(20), "Rank".rjust(5), "Diff".rjust(5))
    for card in card_name_list:
        card_name = card.text
        card_rank = machine_search.getCardRank(card_name=card_name)
        card_diff = machine_search.getCardDiff(card_name=card_name)

        print(card_name.rjust(20), str(card_rank).rjust(5), str(card_diff).rjust(5))
    