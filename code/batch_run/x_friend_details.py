##########################################################################################
# Profile 'my' friends and lists
#
##########################################################################################

import json
import re
import sys
import time
sys.path.insert(0, "/Users/chagerman/Projects/_ARCHIVE/Twitterator")

import pandas as pd

# from authClient import AuthClient
# from twitterRest import TwitterRestClient

from twitterator.authClient import AuthClient
from twitterator.twitterRest import TwitterRestClient


def main(cred_file, appname, usr, outpath):
    AC = AuthClient(cred_file)
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    client = TwitterRestClient(consumer_key, consumer_secret)
    raw_results = getAllFriends(client, usr)
    userdicts = extract_info(raw_results)
    df = pd.DataFrame(userdicts)
    df.to_csv(outpath, index=False)





def getAllFriends(client, usr):
    next_cursor = "-1"
    num_results = 0
    results = []
    while next_cursor != "0":
        response = client.get_friends(usr, cursor=next_cursor)
        next_cursor = response['next_cursor_str']
        users = response['users']
        num_results += len(users)
        print("Total number downloaded: {}".format(num_results))
        for u in users:
            results.append(u)
        time.sleep(3)
    return results



def writeAllFriends(client, usr, outpath):
    next_cursor = "-1"
    num_results = 0
    fo = open(outpath, "w")
    while next_cursor != "0":
        response = client.get_friends(usr, cursor=next_cursor)
        next_cursor = response['next_cursor_str']
        users = response['users']
        num_results += len(users)
        print("Total number downloaded: {}".format(num_results))
        for u in users:
            json_str = json.dumps(u)
            fo.write(json_str + "\n")
        time.sleep(3)
    fo.close()


def extract_info(raw_results):
    def process(u):
        name = u['name']
        sn = u['screen_name']
        description = re.sub('[\n\t\r]+', ' ', u['description'])
        location = u['location']
        verified = 'y' if u['verified'] else 'n'
        followers_count = u['followers_count']
        friends_count = u['friends_count']
        text = '' if not 'status' in u else re.sub('[\n\t\r]+', ' ', u['status']['text'])
        return {'name': name,'sn': sn,'description': description,'location': location,'verified': verified,'followers_count': followers_count,'friends_count': friends_count,'text': text}
    results = [process(user) for user in raw_results]
    return results





if __name__ == '__main__':
    cred_file = "/Users/chagerman/Projects/_ARCHIVE/Twitterator/credentials.json"
    appname = "craighagerman"
    usr = "craighagerman"
    outpath = "/Users/chagerman/Desktop/craighagerman_friend_details.csv"
    main(cred_file, appname, usr, outpath)

