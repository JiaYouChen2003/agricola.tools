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

if __name__ == '__main__':
    workbook_list = openpyxl.load_workbook('Agricola_2307.xlsx')

    rank = getValuesFromSheet(workbook_list['Ranking'])
    diff = getValuesFromSheet(workbook_list['Difference'])

    card_name_list = scrape.Scrape().getCardListFromBGA()
    for card in card_name_list:
        card_name = card.text
        card_rank = getItemIndexByNameFromArray(card_name, rank, 1, 0)
        card_diff = getItemIndexByNameFromArray(card_name, diff, 0, 3)
        print(card_name, card_rank, card_diff)
    