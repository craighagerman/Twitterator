

'''
top-level driver for the twitterator package




EXAMPLE USAGE
=============

ARABIC:
python3 Twitterator.py arabic filter
python3 Twitterator.py arabic random

ELECTION2015:
python3 Twitterator.py election filter



'''
import http
from http.client import IncompleteRead
import os
from prettytable import PrettyTable
import sys
import urllib3
import uuid

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
    t.align["Variable"] = "l" # Left align
    t.align["Details"] = "l" # Left align
    t.add_row(["Twitter Application name", appname])
    t.add_row(["Stream Kind", kind])
    t.add_row(["File Prefix", fileprefix])
    t.add_row(["Credentials File:", cred_file])
    t.add_row(["Output Data Directory", rootdir])
    print(t)
    print("\n")

#  runStreamer("filter", appname1, credfile, outdir, "ar-keywords", track_terms=keywords)
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


#
# ---------------------------------------------------------------------------------------------------------------------------------------
#
# SPECIFIC STREAMING FUNCTIONS
def collectElection2015(kind, variation, outdir):
    credfile, resources = init()
    rd = {  106618766460442 :   "/Users/chagerman/Projects/Twitter/Twitterator/stream_data/",   # macbook
            274973440742298:    "/home/chagerman/Twitterator/stream_data",                      # uscc
            110392253461240 :   "/Volumes/BlueSky/Code/Twitterator/stream_data/" }                         # hackintosh
    default_rootdir = rd[uuid.getnode()]
    rootdir = outdir if outdir != None else default_rootdir
    canada_geo_bounds = [-141.0, 41.7, -52.6, 83.1]
    # {streamkind:  {variation:  (appname,  prefix,  input_list)}}
    electionStreamDict = {
        "geo":      {   None:   ("mProbe_1", "cangeo", canada_geo_bounds)},
        "filter":   {   "1": ("Crisix_1",    "election2015a", _getTrackTerms(os.path.join(resources, "election2015Keywords.txt"))),
                        "2": ("goat_team_1", "election2015b", _getTrackTerms(os.path.join(resources, "candidates_a.txt"))),
                        "3": ("goat_team_2", "election2015c", _getTrackTerms(os.path.join(resources, "candidates_b.txt"))),
                        "4": ("goat_team_3", "election2015d", _getTrackTerms(os.path.join(resources, "candidates_c.txt"))),
                        "5": ("Sekr_2",      "election2015e", _getTrackTerms(os.path.join(resources, "candidates_d.txt")))},
        "userlist": {    None:       ("CanPol",      "canpoli", None),
                        "newsOrg":   ("goat_team_0", "newsOrg", None)}}
    try:
        appname, fileprefix, input_list = electionStreamDict[kind][variation]
    except KeyError:
        print("ERROR: KeyError: invalid input into electionStreamDict")
        exit(0)
    rootdir = os.path.join(rootdir, fileprefix)
    runStreamer(kind, appname, credfile, rootdir, fileprefix, input_list, langs=["en", "fr"])

def collectArabic(kind, variation, outdir):
    credfile, resources = init()
    rootdir = outdir if outdir != None else "/Users/chagerman/Projects/Data_Collection/Arabic_keywords_10-06/stream_data"
    # {streamkind:  {variation:  (appname,  prefix,  input_list, langs)}}
    arabicStreamDict = {
        # "filter": {     None: ("mProbe_2",    "ar-keywords", _getTrackTerms("/Users/chagerman/Projects/Data_Collection/Arabic_keywords_10-06/ar_keywords_10-06.txt"), None )},
        "filter": {     "1": ("mProbe_0",    "ar-keywords-zero", _getTrackTerms("/Users/chagerman/Projects/Data_Collection/Arabic_keywords_10-06/KEYWORD_DATA/ar_keywords_10-15.txt"), None ),
                        "2": ("goat_team", "ar-keywords-1020", _getTrackTerms("/Users/chagerman/Projects/Data_Collection/Arabic_keywords_10-06/KEYWORD_DATA/ar_keywords_10-20.txt"), None )},
        "random": {     None: ("mProbe_3",  "ar-random", None, ["ar"])}
    }
    try:
        appname, prefix, keywords, langs = arabicStreamDict[kind][variation]
    except KeyError:
        print("ERROR: KeyError: invalid input into electionStreamDict")
        exit(0)
    runStreamer(kind, appname, credfile, rootdir, prefix, keywords, langs=langs)

def collectRussian(kind, variation, outdir):
    credfile, resources = init()
    sd = "/Users/chagerman/Projects/Data_Collection/Russian_ISIL_keywords/stream_data"
    sdcc = "/home/chagerman/Twitterator/stream_data"
    rootdir = outdir if outdir != None else sd
    # {streamkind:  {variation:  (appname,  prefix,  input_list, langs)}}
    russianStreamDict = {
        "filter": {     None: ("ruisil",    "ru-isil-keywords", _getTrackTerms(os.path.join(resources, "ru-isil-keywords.txt")), ["ru"] )},
        "random": {     None: ("mProbe_2",  "ru-random", None, ["ru"])}
    }
    try:
        appname, prefix, keywords, langs = russianStreamDict[kind][variation]
    except KeyError:
        print("ERROR: KeyError: invalid input into electionStreamDict")
        exit(0)
    runStreamer(kind, appname, credfile, rootdir, prefix, keywords, langs=langs)

def collectUkraine(kind, variation, outdir):
    credfile, resources = init()
    sd = "/Users/chagerman/Projects/Data_Collection/Ukraine_crisis/stream_data"
    rootdir = outdir if outdir != None else sd
    # {streamkind:  {variation:  (appname,  prefix,  input_list, langs)}}
    kwf1 = "/Users/chagerman/Projects/Data_Collection/Ukraine_crisis/ukraineKeywords_1028a.txt"
    kwf2 = "/Users/chagerman/Projects/Data_Collection/Ukraine_crisis/ukraineKeywords_1028b.txt"
    kwf3 = "/Users/chagerman/Projects/Data_Collection/Ukraine_crisis/ukraineKeywords_1028c.txt"
    ukraineStreamDict = {
        "filter": {     "1": ("goat_team_1",  "ukraine-keywords-a", _getTrackTerms(kwf1), ["ru", "uk"] ),
                        "2": ("goat_team_2",  "ukraine-keywords-b", _getTrackTerms(kwf2), ["ru", "uk"] ),
                        "3": ("goat_team_3",  "ukraine-keywords-c", _getTrackTerms(kwf3), ["ru", "uk"] )},
        "random": {     None: ("goat_team_2",  "ukraine-random", None, ["uk"])}
    }
    try:
        appname, prefix, keywords, langs = ukraineStreamDict[kind][variation]
    except KeyError:
        print("ERROR: KeyError: invalid input into ukraineStreamDict")
        exit(0)
    runStreamer(kind, appname, credfile, rootdir, prefix, keywords, langs=langs)


def collect(kind, outdir, kwfile, appname, prefix, langs):
    print("kind:\t{}\noutdir:\t{}\nkwfile:\t{}\nappname:\t{}\nprefix:\t{}\n".format(kind, outdir, kwfile, appname, prefix ))
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
# ---------------------------------------------------------------------------------------------------------------------------------------
#
# UTILITY FUNCTIONS
def _getTrackTerms(path):
    return [t.strip().split("\t")[0].strip() for t in open(path) if not t.startswith("#") and not t.strip() == ""]

#
# ---------------------------------------------------------------------------------------------------------------------------------------
#
# CL MAIN ENTRY POINT
if __name__ == '__main__':
    collection = sys.argv[1]
    kind  = sys.argv[2]
    # variation = None if len(sys.argv) < 4 else sys.argv[3]
    # outdir = None if len(sys.argv) < 5 else sys.argv[4]
    outdir = None if len(sys.argv) < 4 else sys.argv[3]
    kwfile = sys.argv[4]
    appname = sys.argv[5]
    prefix = sys.argv[6]
    langs = None if len(sys.argv) < 8 else sys.argv[7].split(",")
    print("langs = ", langs)

    def collection_to_function(argument):
        switcher = {
            # "arabic"   : collectArabic,
            "arabic"   : collect,
            "election" : collectElection2015,
            "russian"  : collectRussian,
            "ukraine"  : collect
        }
        func = switcher.get(argument, lambda: "nothing")
        return func

    collector = collection_to_function(collection)
    # collector(kind, variation, outdir)
    collector(kind, outdir, kwfile, appname, prefix, langs)


