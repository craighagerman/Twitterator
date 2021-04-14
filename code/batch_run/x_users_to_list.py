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

import tweepy

from twitterator.authClient import AuthClient
from twitterator.twitterRest import TwitterRestClient


def main(cred_file, appname, usr, snfile, list_id):
    AC = AuthClient(cred_file)
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    screen_names = [x.strip() for x in open(snfile)]
    add_members_to_list(api, list_id, screen_names)
    
    

def add_members_to_list(api, list_id, screen_names):
    ''' add members contained in screen_names to list given by list_id.
        Can add 100 comma-separated screen_names. nb. Lists cannot have more
        than 5000 members. '''
    for sn in screen_names:
        print("Adding {} to list".format(sn))
        api.add_list_member(screen_name=sn, list_id=list_id)
        time.sleep(1)




if __name__ == '__main__':
    cred_file = "/Users/chagerman/Projects/_ARCHIVE/Twitterator/credentials.json"
    snfile = "/Users/chagerman/Desktop/screen_names.txt"
    appname = "craighagerman"
    usr = "craighagerman"
    list_id = '231171025'
    main(cred_file, appname, usr, snfile, list_id)

