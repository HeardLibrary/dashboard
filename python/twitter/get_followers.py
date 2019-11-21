from pathlib import Path
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
import json
import requests   # best library to manage HTTP transactions

# load the credentials
home = str(Path.home()) #gets path to home directory; supposed to work for Win and Mac
keyFilename = 'twitter_api_keys.txt'
apiKeyPath = home + '/' + keyFilename

try:
    with open(apiKeyPath, 'rt', encoding='utf-8') as fileObject:
        fileStringList = fileObject.read().split('\n')
        clientKey = fileStringList[0]
        clientSecret = fileStringList[1]
        #print('key: ', clientKey) # delete this line once the script is working; don't want printout as part of the notebook
        #print('secret: ', clientSecret) # delete this line once the script is working; don't want printout as part of the notebook
except:
    print(keyFilename + ' file not found - is it in your home directory?')

# get the access token
requestTokenUrl = 'https://api.twitter.com/oauth2/token'

clientObject = BackendApplicationClient(client_id=clientKey)
oauth = OAuth2Session(client=clientObject)
accessTokenJson = oauth.fetch_token(token_url=requestTokenUrl, client_id=clientKey, client_secret=clientSecret)
# access token should be cached/saved and used repeatedly rather than making many requests fo a new token
#print(accessTokenJson)
#print()
accessToken = accessTokenJson.get('access_token') # extract the value of access_token from the JSON
#print(accessToken)

# query the API
resourceUrl = 'https://api.twitter.com/1.1/users/show.json'
accountsList = ['vandylibraries', 'liblairy', 'vandyfinearts', 'vutvnews']
for account in accountsList:
    paramDict = {
                 'screen_name' : account, 
                 'include_entities' : 'false'
                }
    r = requests.get(resourceUrl, headers={'Authorization' : 'Bearer '+ accessToken}, params = paramDict)
    data = r.json()
    # print(json.dumps(data, indent = 2))
    print(account, data['followers_count'])
