import os

def lambda_handler(event, context):
    os.chdir('/tmp')
    someText = "Goin' into the file!"
    with open('datafile.txt', 'wt', encoding='utf-8') as fileObject:
        fileObject.write(someText)
    
    with open('datafile.txt', 'rt', encoding='utf-8') as fileObject:
        lineList = fileObject.read()
    print(lineList)