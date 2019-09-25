from pathlib import Path
from github import Github
import requests

# the access token was generated for read/write access to public repos
# see https://developer.github.com/v3/auth/#working-with-two-factor-authentication
# see https://github.com/settings/tokens/new select public_repo

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
        # neet to test this on a repo without 2 factor authentication
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


# set variable values
githubUsername = ''  # set to empty string if using a token
repoOwner = 'baskauf'
repoName = 'practice'

filename = 'test1.txt'
path = filename # need to modify file name if not in the root directory
commitMessage = 'Modify another test file'
content = '''This is Tomys repository.
This is his second test file.
He is now changing it.'''

# script starts here
repo = loginGetRepo("practice", githubUsername)
print(getUserList(repo))


#response = repo.create_file(path, commitMessage, content)

#response = updateFile(repoOwner, repoName, path, commitMessage, content)
#response = repo.update_file(path, commitMessage, content, sha)
#print(response)

#repo.add_to_collaborators('baskaufs','push')
#repo.remove_from_collaborators('baskaufs')