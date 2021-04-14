##########################################################################################
# Given an input file containing a list of twitter screen_names (with or without leading-@)
#   - add user as a friend
##########################################################################################


import time

import tweepy
# from app.twitterator.authClient import AuthClient
from twitAuthClient import TwitAuthClient



def main(cred_file, appname, user_file):
    AC = TwitAuthClient(cred_file)
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    snlist = [x.strip().strip("@") for x in open(user_file)]
    for screen_name in snlist:
        print("adding friend: {}".format(screen_name))
        api.create_friendship(screen_name)
        time.sleep(1)




if __name__ == '__main__':
    cred_file = "/Users/chagerman/Projects/_ARCHIVE/Twitterator/credentials.json"
    appname = "craighagerman"
    user_file = "/Users/chagerman/Desktop/nips_twitter.txt"
    main(cred_file, appname, user_file)

