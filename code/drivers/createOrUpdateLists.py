#
'''
For a given Twitter user (screen_name),
    create a new list
        iteratively add members to that list




'''

import os
import sys

# ..................................................................
# provide the Python interpreter with the path to this module
import time

SRC_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

print("SRC_DIR: {}".format(SRC_DIR))
print("ROOT_DIR: {}".format(ROOT_DIR))
print("os.path.dirname(ROOT_DIR): {}".format(os.path.dirname(ROOT_DIR)))

sys.path.append(SRC_DIR)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.dirname(ROOT_DIR))
# ..................................................................

from app.drivers.listWalker import ListWalker
from app.twitterator.authClient import AuthClient
import tweepy


class ListMaker:
    def __init__(self, cred_file, appname):
        self.client = self.authenticate(cred_file, appname)


    def authenticate(self, cred_file, appname):
        ##################################################################
        #   Tweepy OAuth Authentication dance
        ##################################################################
        # NOTE: the appname must have read/write permissions on twitter.com in order to modify and account
        AC = AuthClient(cred_file)
        access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        client = tweepy.API(auth)
        # check my credentials
        print("Using appname associated with account:\t{}\t{}".format(client.verify_credentials().name, client.verify_credentials().screen_name))
        return client


    #   Create & populate a new Twitter list from a (python) list of users
    # ..................................................................
    def createAndPopulateList(self, screen_names, list_name, list_description):
        # newlist = client.create_list("News-ish", "News and Finance related accounts")
        newlist = self.client.create_list(list_name, list_description)
        sid = newlist.id_str
        # populate list
        for sname in screen_names:
            print("\tadding {}".format(sname))
            self.client.add_list_member(list_id=sid, screen_name=sname)


    #   Get screen_names from a given profile file
    # ..................................................................
    def parseProfileFile(self, infile):
        lines = (x.strip().split("\t") for x in open(infile))
        return [x[1] for x in lines]


    #   Get screen_names from a given profile file
    # ..................................................................
    def getProfileFiles(self, indir):
        return [os.path.join(indir, f) for f in os.listdir(indir) if f.endswith(".txt")]



# _____________________________________________________________________________________________________________________
def main():
    cred_file = "/Users/chagerman/Projects/Twitterator/twitter_credentials.json"
    appname = "allTwittterNews"
    basedir = "/Users/chagerman/Projects/NewsClassifier/InputData/profile_lists"

    # directory containing files which contain a list of profiles
    indir = "/Users/chagerman/Projects/NewsClassifier/Docs/AllTwittterNews"

    lm = ListMaker(cred_file, appname)
    files = lm.getProfileFiles(indir)
    for fil in files:
        print("reading file {}".format(fil))
        name = os.path.split(fil)[1].replace(".txt", "")
        print("Processing list {}".format(name))
        screen_names = lm.parseProfileFile(fil)
        lm.createAndPopulateList(screen_names, name, name)
        time.sleep(60)




if __name__ == '__main__':
    main()
