from pathlib import Path
import facebook
import hmac
import hashlib
import base64

# see https://stackoverflow.com/questions/26248105/facebook-graph-api-calls-with-appsecret-proof-in-python
def genAppSecretProof(app_secret, access_token):
    h = hmac.new (
        app_secret.encode('utf-8'),
        msg=access_token.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    return h.hexdigest()

# load the credentials
home = str(Path.home()) #gets path to home directory; supposed to work for Win and Mac
keyFilename = 'facebook_api_keys.txt'
apiKeyPath = home + '/' + keyFilename

try:
    with open(apiKeyPath, 'rt', encoding='utf-8') as fileObject:
        fileStringList = fileObject.read().split('\n')
        app_id = fileStringList[0]
        app_secret = fileStringList[1]
        access_token = fileStringList[2]
        print('id: ', app_id) # delete this line once the script is working; don't want printout as part of the notebook
        print('secret: ', app_secret) # delete this line once the script is working; don't want printout as part of the notebook
        print('access token: ', access_token)
except:
    print(keyFilename + ' file not found - is it in your home directory?')


# see https://facebook-sdk.readthedocs.io/en/latest/api.html
api = facebook.GraphAPI(access_token=access_token)
postargs = {"appsecret_proof": genAppSecretProof(app_secret, access_token)}

