from pathlib import Path
from github import Github
import requests
import csv
import json
from openpyxl import load_workbook
import io

# the access token should be generated for read/write access to public repos
# see https://developer.github.com/v3/auth/#working-with-two-factor-authentication
# see https://github.com/settings/tokens/new
# select public_repo

# reference on PyGithub: https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
# reference on GitHub API: https://developer.github.com/v3/guides/getting-started/

# value of directory should be either 'home' or 'working'
def loadCredential(filename, directory):
    cred = ''
    # to change the script to look for the credential in the working directory, change the value of home to empty string
    if directory == 'home':
        home = str(Path.home()) #gets path to home directory; supposed to work for Win and Mac
        credentialPath = home + '/' + filename
    else:
        directory = 'working'
        credentialPath = filename
    try:
        with open(credentialPath, 'rt', encoding='utf-8') as fileObject:
            cred = fileObject.read()
    except:
        print(filename + ' file not found - is it in your ' + directory + ' directory?')
        exit()
    return(cred)

# pass in an empty string for organizationName to use an individual account
# pass in an empty string for githubUsername to use a token instead of username login
def loginGetRepo(repoName, githubUsername, organizationName, credDirectory):
    if githubUsername == '':
        token = loadCredential('token.txt', credDirectory)
        g = Github(login_or_token = token)
    else:
        pwd = loadCredential('pwd.txt', credDirectory)
        g = Github(githubUsername, pwd)
    
    if organizationName == '':
        # this option accesses a user's repo instead of an organizational one
        # In this case, the value of organizationName is not used.
        user = g.get_user()
        repo = user.get_repo(repoName)
    else:
        # this option creates an instance of a repo in an organization
        # to which the token creator has push access
        organization = g.get_organization(organizationName)
        repo = organization.get_repo(repoName)
    return(repo)

def getUserList(repo):
    personList = []
    people = repo.get_collaborators()
    for person in people:
        personList.append(person.login)
    return personList

def getFileSha(account, repo, filePath):
    # get the data about the file to get its blob SHA
    r = requests.get('https://api.github.com/repos/' + account + '/' + repo + '/contents/' + filePath)
    fileData = r.json()
    try:
        sha = fileData['sha']
    except:
        # if the file doesn't already exist on GitHub, no sha will be returned
        sha = ''
    return sha

# use this function to update an existing text file
def updateFile(account, repoName, path, commitMessage, content):
    sha = getFileSha(account, repoName, path)
    if sha == '':
        response = repo.create_file(path, commitMessage, content)
    else:
        response = repo.update_file(path, commitMessage, content, sha)
    return response

def readFilenames():
    with open('filenames.txt', 'rt', encoding='utf-8') as fileObject:
        text = fileObject.read()
        fileList = text.strip().split('\n')
        return fileList    

def readCsv(filename):
    fileObject = open(filename, 'r', newline='', encoding='utf-8')
    readerObject = csv.reader(fileObject)
    array = []
    for row in readerObject:
        array.append(row)
    fileObject.close()
    return array

def readRawCsv(filename):
    with open(filename, 'rt', encoding='utf-8') as fileObject:
        text = fileObject.read()
        return text

def readDict(filename):
    # had to make this change to get rid of leading byte order mark from first key
    fileObject = open(filename, 'r', newline='', encoding='utf-8-sig')
    #fileObject = open(filename, 'r', newline='', encoding='utf-8')
    dictObject = csv.DictReader(fileObject)
    array = []
    for row in dictObject:
        array.append(row)
    fileObject.close()
    return array

# ***********************************************************
# set variable values
githubUsername = ''  # set to empty string if using a token (for 2FA)
organizationName = 'heardlibrary'  # set to empty string if the repo belongs to the token issuer
repoName = 'dashboard'
credDirectory = 'home' # set to 'home' if the credential is in the home directory, otherwise working directory
pathToDirectory = 'data/'
excelFilename = 'BytheNumbersWorksheet.xlsx'

# script starts here

# This is just to produce something that shows the connection with the repo is successful
repo = loginGetRepo(repoName, githubUsername, organizationName, credDirectory)
print(getUserList(repo))

# load the Excel spreadsheet as a workbook object
# see https://stackoverflow.com/questions/28517508/read-excel-cell-value-and-not-the-formula-computing-it-openpyxl
# for information about reading values rather than formulas
wb = load_workbook(filename = excelFilename, data_only=True)
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

    # Push JSON file
    content = json.dumps(sheetDictList)
    filename = outFileNameRoot + '.json'
    path = pathToDirectory + filename
    commitMessage = 'Update ' + outFileNameRoot + ' JSON file via API'
    response = updateFile(organizationName, repoName, path, commitMessage, content)
    print(response)

    # Push CSV file.
    # refer to https://stackoverflow.com/questions/38232838/convert-a-python-list-of-lists-to-a-string
    csvOutputObject = io.StringIO()
    writerObject = csv.writer(csvOutputObject)
    for row in sheetListList:
        writerObject.writerow(row)
    csvString = csvOutputObject.getvalue()
    filename = outFileNameRoot + '.csv'
    path = pathToDirectory + filename
    commitMessage = 'Update ' + outFileNameRoot + ' CSV file via API'
    response = updateFile(organizationName, repoName, path, commitMessage, csvString)
    print(response)
    print()
    
# These commented out lines can be uncommented to perform various operations on the repo
#response = repo.create_file(path, commitMessage, content)

#response = repo.add_to_collaborators('username','push')
#response = repo.remove_from_collaborators('username')
#print(response)

