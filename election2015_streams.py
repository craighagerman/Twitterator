# builtin imports
from functools import partial
import datetime
import http
from http.client import IncompleteRead
import itertools
import json
import gzip
import os
from prettytable import PrettyTable
import re
import sys
import shutil
import threading
import time
from urllib3 import exceptions
import urllib3

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
    langs = ["en", "fr"]
    # track_terms = [t.strip().split("\t")[0].strip() for t in open("election2015Keywords.txt") if not t.startswith("#")]
    # print(",".join(track_terms))

    while True:
        print("Streamkind is ..... {}".format(streamkind))
        try:
            st = Streamer(api, auth, rootdir, fileprefix)
            if streamkind == "filter":
                print("FILTERING TRACK TERMS")
                # st.streamFilter(track_terms, langs)
                st.streamFilter(input_list, langs)
            elif streamkind == "geo":
                print("FILTERING GEO BOUNDS")
                # canada_geo_bounds = [-141.0, 41.7, -52.6, 83.1]
                # st.streamLocation(canada_geo_bounds)
                st.streamLocation(input_list)
            elif streamkind == "userlist" or streamkind == "userlist_newsorg":
                print("STREAMING USER TIMELINE")
                st.streamFriends()
            else:
                print("Incorrect stream kind. Must be one of 'filter', 'random' or 'userlist'.")
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

    canada_geo_bounds = [-141.0, 41.7, -52.6, 83.1]
    input_list = []
    if len(sys.argv) == 3:
        machine = sys.argv[1].strip()
        streamkind = sys.argv[2].strip()
        print(machine)
        print(streamkind)
        if streamkind == "userlist":
            appname = "CanPol"
            outdir = fileprefix = "canpoli"
        elif streamkind == "userlist_newsorg":
            appname = "goat_team_0"
            outdir = fileprefix = "newsOrg"
        elif streamkind == "geo":
            appname = "mProbe_1"
            outdir = fileprefix = "cangeo"
            input_list = canada_geo_bounds
        elif streamkind == "filter":
            appname = "Crisix_1"
            outdir = fileprefix = "election2015"
            track_terms = [t.strip().split("\t")[0].strip() for t in open("election2015Keywords.txt") if not t.startswith("#")]
            input_list = track_terms
        elif streamkind == "filter1":
            streamkind = "filter"
            appname = "goat_team_1"
            outdir = fileprefix = "election2015a"
            track_terms = [t.strip().split("\t")[0].strip() for t in open("candidates_a.txt") if not t.startswith("#")]
            input_list = track_terms
        elif streamkind == "filter2":
            streamkind = "filter"
            appname = "goat_team_2"
            outdir = fileprefix = "election2015b"
            track_terms = [t.strip().split("\t")[0].strip() for t in open("candidates_b.txt") if not t.startswith("#")]
            input_list = track_terms
        elif streamkind == "filter3":
            streamkind = "filter"
            appname = "goat_team_3"
            outdir = fileprefix = "election2015c"
            track_terms = [t.strip().split("\t")[0].strip() for t in open("candidates_c.txt") if not t.startswith("#")]
            input_list = track_terms
        elif streamkind == "filter4":
            streamkind = "filter"
            appname = "Sekr_2"
            outdir = fileprefix = "election2015d"
            track_terms = [t.strip().split("\t")[0].strip() for t in open("candidates_d.txt") if not t.startswith("#")]
            input_list = track_terms
    else:
        print("wrong number of command line arguments")
        exit(0)

    rd = {  "mb" : "/Users/chagerman/Projects/Twitter/Twitterator/stream_data/",
            "hack" : "/Volumes/BlueSky/Code/Twitterator/stream_data/" }
    default_rootdir = rd[machine]
    rootdir = os.path.join(default_rootdir, outdir)

    run(streamkind, appname, default_cred_file, rootdir, fileprefix, input_list)




'''
python3 election2015_streams.py hack geo
python3 election2015_streams.py hack userlist
python3 election2015_streams.py hack filter

python3 election2015_streams.py hack filter1
python3 election2015_streams.py hack filter2
python3 election2015_streams.py hack filter3
python3 election2015_streams.py hack filter4

python3 election2015_streams.py hack userlist_newsorg
'''


