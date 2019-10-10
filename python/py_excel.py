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
        if count == 0:
            for value in row:
                if value == None:
                    rowList.append('')
                else:
                    rowList.append(value)
            headerList = rowList
            sheetListList.append(rowList)
        else:
            rowDict = {}
            rowPosition = 0
            for value in row:
                if value == None:
                    rowList.append('')
                    rowDict.update( {headerList[rowPosition] : ''} )
                else:
                    rowList.append(value)
                    rowDict.update( {headerList[rowPosition] : value} )
                rowPosition +=1
            sheetListList.append(rowList)
            sheetDictList.append(rowDict)
        count +=1
    print(sheetListList)
    print(sheetDictList)
    print(json.dumps(sheetDictList))

        
#sheet = wb['Collections']
#print(sheet['A1'].value)
