import openpyxl

def get_values(sheet):
    arr = []
    for row in sheet:
        arr2 = []
        for column in row:
            arr2.append(column.value)
        arr.append(arr2)
    return arr

wb = openpyxl.load_workbook('Agricola_2307.xlsx')

names = wb.sheetnames
s1 = wb['Ranking']
s2 = wb['Difference']

rank = get_values(s1)
diff = get_values(s2)

while True:
    card = input() # implement by using mouse
    print(rank[0])
    for row in rank:
        if row[1] == card:
            print(row)
            break
    print(diff[0])
    for row in diff:
        if row[0] == card:
            print(row)
            break
    print()
    