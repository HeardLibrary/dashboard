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

def loginGetRepo(repoName, githubUsername):
    if githubUsername == '':
        token = loadCredential('token.txt')
        g = Github(login_or_token = token)
    else:
        pwd = loadCredential('pwd.txt')
        g = Github(githubUsername, pwd)
    user = g.get_user()
    repo = user.get_repo(repoName)
    return(repo)

def getUserList(repo):
    personList = []
    people = repo.get_collaborators()
    for person in people:
        personList.append(person.login)
    return personList

def getFileSha(owner, repo, filePath):
    # get the data about the file to get its blob SHA
    r = requests.get('https://api.github.com/repos/' + owner + '/' + repo + '/contents/' + filePath)
    fileData = r.json()
    sha = fileData['sha']
    return sha

def updateFile(repoOwner, repoName, path, commitMessage, content):
    sha = getFileSha(repoOwner, repoName, path)
    response = repo.update_file(path, commitMessage, content, sha)

def readCsv(filename):
    fileObject = open(filename, 'r', newline='', encoding='utf-8')
    readerObject = csv.reader(fileObject)
    array = []
    for row in readerObject:
        array.append(row)
    fileObject.close()
    return array

def readDict(filename):
    fileObject = open(filename, 'r', newline='', encoding='utf-8')
    dictObject = csv.DictReader(fileObject)
    array = []
    for row in dictObject:
        array.append(row)
    fileObject.close()
    return array

# set variable values
githubUsername = ''  # set to empty string if using a token
repoOwner = 'baskauf'
repoName = 'practice'

filename = 'test2.txt'
path = filename # need to modify file name if not in the root directory
commitMessage = 'File created via API'
content = '''This is new file content.
Second line.'''

# script starts here

# This is just to produce something that shows the connection with the repo is successful
repo = loginGetRepo("practice", githubUsername)
print(getUserList(repo))

# Test of reading in a CSV
inputFilename = '../data/collections.csv'
outputFilename = '../data/collections.json'
tableData = readCsv(inputFilename)
dictData = readDict(inputFilename)

# Test of writing JSON converted from the CSV
json = json.dumps(dictData)
print(json)
with open(outputFilename, 'wt', encoding='utf-8') as fileObject:
    fileObject.write(json)

# These commented out lines can be uncommented to perform various operations on the repo
#response = repo.create_file(path, commitMessage, content)

#response = updateFile(repoOwner, repoName, path, commitMessage, content)
#response = repo.update_file(path, commitMessage, content, sha)

#response = repo.add_to_collaborators('baskaufs','push')
#response = repo.remove_from_collaborators('baskaufs')
#print(response)


