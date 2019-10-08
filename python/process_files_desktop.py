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
    print(fileData)
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
organizationName = 'heardlibrary'  # set to empty string if the repo belongs to the token issuer
repoName = 'dashboard'
credDirectory = 'home' # set to 'home' if the credential is in the home directory, otherwise working directory
pathToDirectory = 'data/'

# script starts here

# This is just to produce something that shows the connection with the repo is successful
repo = loginGetRepo(repoName, githubUsername, organizationName, credDirectory)
print(getUserList(repo))

# Get the list of filename roots
filenames = readFilenames()
for filenameRoot in filenames:
    fileFound = True
    try:
        # Read in a CSV
        inputFilename = filenameRoot + '.csv'
        tableData = readCsv(inputFilename) # not used yet, but in future when CSV is edited by script
        rawCsvText = readRawCsv(inputFilename)
        dictData = readDict(inputFilename)
    
    except Exception as e:
        fileFound = False
        print(str(e))
    
    if fileFound:
        # Write JSON converted from the CSV
        content = json.dumps(dictData)
        filename = filenameRoot + '.json'
        path = pathToDirectory + filename
        commitMessage = 'Update ' + filenameRoot + ' JSON file via API'
        response = updateFile(organizationName, repoName, path, commitMessage, content)
        print(response)

        # Write CSV file. The text is just dumped as it was read in from the local file.
        filename = filenameRoot + '.csv'
        path = pathToDirectory + filename
        commitMessage = 'Update ' + filenameRoot + ' CSV file via API'
        response = updateFile(organizationName, repoName, path, commitMessage, rawCsvText)
        print(response)

# These commented out lines can be uncommented to perform various operations on the repo
#response = repo.create_file(path, commitMessage, content)

#response = repo.add_to_collaborators('username','push')
#response = repo.remove_from_collaborators('username')
#print(response)

