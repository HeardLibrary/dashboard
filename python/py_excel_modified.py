from openpyxl import load_workbook
import csv
import json
import io

wb = load_workbook(filename = 'BytheNumbersWorksheet.xlsx')
# step through each sheet in the file
for sheet in wb:
    outFileNameRoot = sheet.title
    print(outFileNameRoot)
    # create lists to hold the structures for creating the CSV and JSON
    sheetListList = [] # list for creating CSV
    sheetDictList = [] # list for creating JSON
    rowCount = 0
    for row in sheet.values:
        # create structures to hold row list (for CSV) and dict (for JSON)
        rowList = []
        rowDict = {}
        column = 0 # keep track of column to know which key to use for dict
        for value in row:
            if value == None:
                # this is the case where a cell has no value
                rowList.append('')
                # the header row does not have a dict; its labels are used for keys
                if rowCount != 0:
                    rowDict.update( {headerList[column] : ''} )
            else:
                # need to talk to Tao about whether this is a good idea
                valueString = str(value) # turn any numbers into strings
                rowList.append(valueString)
                # header row has no dict
                if rowCount != 0:
                    rowDict.update( {headerList[column] : valueString} )
            column +=1
        sheetListList.append(rowList) # every row gets added for the CSV
        if rowCount == 0:
            # on the first row, the list is saved to use for dict keys
            headerList = rowList
        else:
            # after the header row, add the dict to the list for the JSON
            sheetDictList.append(rowDict)
        rowCount +=1
    print(sheetListList)
    # refer to https://stackoverflow.com/questions/38232838/convert-a-python-list-of-lists-to-a-string
    csvOutputObject = io.StringIO()
    writerObject = csv.writer(csvOutputObject)
    for row in sheetListList:
        writerObject.writerow(row)
    csvString = csvOutputObject.getvalue()
    print(csvString)
    print()
        
#sheet = wb['Collections']
#print(sheet['A1'].value)
