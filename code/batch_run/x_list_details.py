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
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)

    client = TwitterRestClient(consumer_key, consumer_secret)
    # getAllFriends(client, usr, outpath)

    frames = []
    user_lists = client.get_lists(usr)
    for lst in user_lists:
        list_id = lst['id']
        name = lst['name']
        sn = lst['user']['screen_name']
        description = lst['description']
        member_count = lst['member_count']
        print("Processing list: {}\t member count: {}".format(name, member_count))
        subscriber_count = lst['subscriber_count']
        d2 = {"list_id": list_id, "list_name": name, "list_owner_screen_name": sn, "list_description": description, "list_member_count": member_count, "list_subscriber_count": subscriber_count}
        allmembers = getAllListMembers(client, list_id)
        allmembers2 = [dict(item, **d2) for item in allmembers]
        frames.append(pd.DataFrame(allmembers2))
    df = pd.concat(frames)
    df.to_csv(outpath, index=False)





# def getAllFriends(client, usr, outpath):
#     next_cursor = "-1"
#     num_results = 0
#     fo = open(outpath, "w")
#     while next_cursor != "0":
#         response = client.get_friends(usr, cursor=next_cursor)
#         next_cursor = response['next_cursor_str']
#         users = response['users']
#         num_results += len(users)
#         print("Total number downloaded: {}".format(num_results))
#         for u in users:
#             json_str = json.dumps(u)
#             fo.write(json_str + "\n")
#         time.sleep(3)
#     fo.close()




if __name__ == '__main__':
    cred_file = "/Users/chagerman/Projects/_ARCHIVE/Twitterator/credentials.json"
    appname = "craighagerman"
    usr = "craighagerman"
    outpath = "/Users/chagerman/Desktop/craighagerman_list_details.csv"
    main(cred_file, appname, usr, outpath)

