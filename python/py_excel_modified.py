from openpyxl import load_workbook
import csv
import json

wb = load_workbook(filename = 'BytheNumbersWorksheet.xlsx')
for sheet in wb:
    outFileNameRoot = sheet.title
    print(outFileNameRoot)
    sheetListList = []
    sheetDictList = []
    count = 0
    for row in sheet.values:
        rowList = []
        rowDict = {}
        rowPosition = 0
        for value in row:
            if value == None:
                rowList.append('')
                if count != 0:
                    rowDict.update( {headerList[rowPosition] : ''} )
            else:
                rowList.append(value)
                if count != 0:
                    rowDict.update( {headerList[rowPosition] : value} )
            rowPosition +=1
        sheetListList.append(rowList)
        if count == 0:
            headerList = rowList
        else:
            sheetDictList.append(rowDict)
        count +=1
    print(sheetListList)
    print(json.dumps(sheetDictList))
    print()

        
#sheet = wb['Collections']
#print(sheet['A1'].value)
