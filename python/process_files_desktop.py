from pathlib import Path
from github import Github
import requests
import csv
import json

# the access token should be generated for read/write access to public repos
# see https://developer.github.com/v3/auth/#working-with-two-factor-authentication
# see https://github.com/settings/tokens/new
# select public_repo

# reference on PyGithub: https://pygithub.readthedocs.io/en/latest/github_objects/Repository.html
# reference on GitHub API: https://developer.github.com/v3/guides/getting-started/

def loadCredential(filename):
    cred = ''
    home = str(Path.home()) #gets path to home directory; supposed to work for Win and Mac
    try:
        with open(home + '/' + filename, 'rt', encoding='utf-8') as fileObject:
            cred = fileObject.read()
    except:
        print(filename + ' file not found - is it in your home directory?')
        exit()
    return(cred)

def loginGetRepo(repoName, githubUsername, organizationName):
    if githubUsername == '':
        token = loadCredential('token.txt')
        g = Github(login_or_token = token)
    else:
        pwd = loadCredential('pwd.txt')
        g = Github(githubUsername, pwd)
    
    # to access a user's repo instead of an organizational one, use the following code:
    # In this case, the value of organizationName is not used and can have any value.
    '''
    user = g.get_user()
    repo = user.get_repo(repoName)
    '''

    # this is the method to create an instance of a repo in an organization to which the token
    # creator has push access
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
    sha = fileData['sha']
    return sha

# use this function to update an existing text file
def updateFile(account, repoName, path, commitMessage, content):
    sha = getFileSha(account, repoName, path)
    response = repo.update_file(path, commitMessage, content, sha)
    return response

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
    fileObject = open(filename, 'r', newline='', encoding='utf-8')
    dictObject = csv.DictReader(fileObject)
    array = []
    for row in dictObject:
        array.append(row)
    fileObject.close()
    return array

# ***********************************************************
# set variable values
githubUsername = ''  # set to empty string if using a token (for 2FA)
organizationName = 'heardlibrary'
repoName = 'dashboard'
filenameRoot = 'collections'
pathToDirectory = 'data/'

# script starts here

# This is just to produce something that shows the connection with the repo is successful
repo = loginGetRepo(repoName, githubUsername, organizationName)
print(getUserList(repo))

# Read in a CSV
inputFilename = filenameRoot + '.csv'
tableData = readCsv(inputFilename) # not used yet, but in future when CSV is edited by script
rawCsvText = readRawCsv(inputFilename)
dictData = readDict(inputFilename)

# Write JSON converted from the CSV
content = json.dumps(dictData)
filename = filenameRoot + '.json'
'''
outputFilename = '../data/collections.json'
with open(outputFilename, 'wt', encoding='utf-8') as fileObject:
    fileObject.write(content)
'''
path = pathToDirectory + filename
commitMessage = 'Update ' + filenameRoot + ' JSON file via API'
response = updateFile(organizationName, repoName, path, commitMessage, content)
print(response)

# Write CSV file. The text is just dumped as it was read in from the local file.
filename = filenameRoot + '.csv'
'''
with open(filename, 'wt', encoding='utf-8') as fileObject:
    fileObject.write(rawCsvText)
'''
path = pathToDirectory + filename
commitMessage = 'Update ' + filenameRoot + ' CSV file via API'
response = updateFile(organizationName, repoName, path, commitMessage, rawCsvText)

# These commented out lines can be uncommented to perform various operations on the repo
#response = repo.create_file(path, commitMessage, content)

#response = repo.add_to_collaborators('username','push')
#response = repo.remove_from_collaborators('username')
print(response)


