import openpyxl
import scrape

def getValuesFromSheet(sheet):
    arr = []
    for row in sheet:
        arr2 = []
        for column in row:
            arr2.append(column.value)
        arr.append(arr2)
    return arr

def getItemIndexByNameFromArray(itemName, arr, column4name, column4index):
    for row in arr:
        if row[column4name] == itemName:
            return row[column4index]

class SearchMachine():
    def __init__(self):
        self.xlsx_name = 'Agricola_2307.xlsx'
        self.workbook_list = openpyxl.load_workbook(self.xlsx_name)
    
    def getCardRank(self, card_name):
        workbook_list = self.workbook_list
        
        arr_rank = getValuesFromSheet(workbook_list['Ranking'])
        card_rank = getItemIndexByNameFromArray(card_name, arr_rank, 1, 0)
        return card_rank

    def getCardDiff(self, card_name):
        workbook_list = self.workbook_list

        arr_diff = getValuesFromSheet(workbook_list['Difference'])
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
    