'''
top-level driver for the twitterator package
Example Usage:

python Twitterator.py <collection> <kind> <outdir> <kwfile> <appname> <prefix> <csv_list_of_langs>
'''
import http
import os
import sys
import urllib3
import uuid

from http.client import IncompleteRead
from prettytable import PrettyTable

import twitterStream
# import twitterRest
from AuthClient import *


def init():
    SRC_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.dirname(SRC_DIR)
    sys.path.insert(0, ROOT_DIR)
    cred_file = os.path.join(ROOT_DIR, "credentials.json")
    resources = os.path.join(ROOT_DIR, "resources")
    return cred_file, resources


def init_msg(kind, appname, cred_file, rootdir, fileprefix):
    t = PrettyTable(["Variable", "Details"])
    t.align["Variable"] = "l"  # Left align
    t.align["Details"] = "l"  # Left align
    t.add_row(["Twitter Application name", appname])
    t.add_row(["Stream Kind", kind])
    t.add_row(["File Prefix", fileprefix])
    t.add_row(["Credentials File:", cred_file])
    t.add_row(["Output Data Directory", rootdir])
    print(t)
    print("\n")




def runStreamer(kind, appname, cred_file, rootdir, fileprefix, input_list, langs=None):
    init_msg(kind, appname, cred_file, rootdir, fileprefix)
    AC = AuthClient(cred_file)
    api, auth = AC.create_tweepy_client(appname)
    while True:
        try:
            st = twitterStream.Streamer(api, auth, rootdir, fileprefix)
            if kind == "filter":
                st.streamFilter(input_list, langs)
            elif kind == "geo":
                st.streamLocation(input_list)
            elif kind == "userlist" or kind == "userlist_newsorg":
                st.streamFriends()
            elif kind == "random":
                st.streamRandom(langs)
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
            exit(0)
        except:
            continue



# -----------------------------------------------------------------------------------------------------------------------------
# STREAMING FUNCTION
def collect(kind, outdir, kwfile, appname, prefix, langs):
    print("kind:\t{}\noutdir:\t{}\nkwfile:\t{}\nappname:\t{}\nprefix:\t{}\n".format(
        kind, outdir, kwfile, appname, prefix))
    credfile, resources = init()
    streamdir = outdir
    # {streamkind:  {variation:  (appname,  prefix,  input_list, langs)}}
    track_terms = None if (kwfile == "None" or kwfile == None) else _getTrackTerms(kwfile)
    streamDict = {
        "filter": (appname, prefix, track_terms, langs),
        "random": (appname, prefix, None, langs)
    }
    try:
        appname, prefix, keywords, langs = streamDict[kind]
    except KeyError:
        print("ERROR: KeyError: invalid input into ukraineStreamDict")
        exit(0)
    runStreamer(kind, appname, credfile, streamdir, prefix, keywords, langs=langs)


#
# -----------------------------------------------------------------------------------------------------------------------------
#
# UTILITY FUNCTIONS
def _getTrackTerms(path):
    return [t.strip().split("\t")[0].strip() for t in open(path) if not t.startswith("#") and not t.strip() == ""]

#
# -----------------------------------------------------------------------------------------------------------------------------
#
# CL MAIN ENTRY POINT
if __name__ == '__main__':
    collection = sys.argv[1]
    kind = sys.argv[2]
    outdir = None if len(sys.argv) < 4 else sys.argv[3]
    kwfile = sys.argv[4]
    appname = sys.argv[5]
    prefix = sys.argv[6]
    langs = None if len(sys.argv) < 8 else sys.argv[7].split(",")
    print("langs = ", langs)


    def collection_to_function(argument):
        switcher = {
            "arabic": collect,
            "ukraine": collect,
            "infra": collect
        }
        func = switcher.get(argument, lambda: "nothing")
        return func

    collector = collection_to_function(collection)
    # collector(kind, variation, outdir)
    collector(kind, outdir, kwfile, appname, prefix, langs)
