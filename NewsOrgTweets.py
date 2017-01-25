# builtin imports
import datetime
import gzip
import http
import itertools
import json
import os
import re
import shutil
import sys
import threading
import time
import urllib3

from functools import partial
from http.client import IncompleteRead
from prettytable import PrettyTable
from urllib3 import exceptions

# 3rd party imports : n.b. tweepy is in ~/Code since master branch in pip is broken
import tweepy

# local imports
# UGLY HACK - IS THERE A BETTER WAY TO IMPORT?
# sys.path.insert(0, "../")
from AuthClient import *
from twitterStream import *


################################################################################
def init_msg(streamkind, appname, cred_file, rootdir, fileprefix):
    t = PrettyTable(["Variable", "Details"])
    t.align["Variable"] = "l" # Left align
    t.align["Details"] = "l" # Left align
    t.add_row(["Twitter Application name", appname])
    t.add_row(["Stream Kind", streamkind])
    t.add_row(["File Prefix", fileprefix])
    t.add_row(["Credentials File:", cred_file])
    t.add_row(["Output Data Directory", rootdir])
    print(t)
    print("\n")


def run(streamkind, appname, cred_file, rootdir, fileprefix, input_list):
    init_msg(streamkind, appname, cred_file, rootdir, fileprefix)
    AC = AuthClient(cred_file)
    api, auth = AC.create_tweepy_client(appname)

    while True:
        print("Streamkind is ..... {}".format(streamkind))
        try:
            st = Streamer(api, auth, rootdir, fileprefix)
            if streamkind == "userlist" or streamkind == "userlist_newsorg":
                print("STREAMING USER TIMELINE")
                st.streamFriends()
            else:
                print("Incorrect stream kind. Must be one of 'userlist', 'userlist_newsorg'.")
                exit(0)
        except http.client.IncompleteRead:
            continue
        except urllib3.exceptions.ReadTimeoutError:
            continue
        except (KeyboardInterrupt, SystemExit):
            st.disconnect()
            print("*    KeyboardInterrupt or SystemExit caught  ")
            break
        except:
            continue
        # except: # catch *all* exceptions
        #     e = sys.exc_info()
        #     print(e)



if __name__ == '__main__':
    SRC_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.dirname(SRC_DIR)
    print("SCR DIR: {}".format(SRC_DIR))
    print("ROOT DIR: {}".format(ROOT_DIR))
    default_cred_file = os.path.join(ROOT_DIR, "credentials.json")
    input_list = []


    if len(sys.argv) == 3:
        machine = sys.argv[1].strip()
        streamkind = sys.argv[2].strip()
        print(machine)
        print(streamkind)
        
        if streamkind == "userlist":
            appname = "newsynews"
            outdir = fileprefix = "newsOrg"
        elif streamkind == "userlist_newsorg":
            appname = "newsynews"
            outdir = fileprefix = "newsOrg"
    else:
        print("wrong number of command line arguments")
        exit(0)

    rd = {  "mb" : "/Users/chagerman/Projects/Twitter/Twitterator/stream_data/",
            "hack" : "/Volumes/BlueSky/Code/Twitterator/stream_data/",
            "aws"  : "/home/ubuntu/Twitterator/stream_data/" }
    default_rootdir = rd[machine]
    rootdir = os.path.join(default_rootdir, outdir)

    run(streamkind, appname, default_cred_file, rootdir, fileprefix, input_list)




'''

python3 NewsOrgTweets.py aws userlist
or
python3 NewsOrgTweets.py aws userlist_newsorg

'''


