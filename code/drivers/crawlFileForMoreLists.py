import os
import re

from tweepy.error import TweepError
from app.twitterator import tUtils
from app.drivers.listWalker import ListWalker

appname = "xdatax"

cred_file = "/Users/chagerman/Projects/Twitterator/twitter_credentials.json"
basedir = "/Users/chagerman/Desktop/tmp"

dirlist = [os.path.join(basedir, f) for f in os.listdir(basedir) if os.path.isdir(os.path.join(basedir, f))]


def get_lists_from_files(dirlist):
    sn_slug_list = []
    for d in dirlist:
        listfile = os.path.join(d, "lists.tsv")
        if os.path.exists(listfile):
            lines = [x.strip().split("\t")[:2] for x in open(listfile)]
            try:
                for screen_name, slug in lines:
                    sndir = os.path.join(basedir, screen_name.lower())
                    listdir = os.path.join(basedir, screen_name, slug)
                    if os.path.exists(sndir):
                        if not (os.path.exists(listdir) and os.path.isdir(listdir)):
                            sn_slug_list.append([screen_name, slug])
            except ValueError:
                pass
    return sn_slug_list


def processSnSlugList(sn_slug_list, lw):
    # walk out each of the user's lists, save results
    try:
        for screen_name, slug in sn_slug_list:
            print("\tprocessing screen_name/list: {}/{}".format(screen_name, slug))
            members = lw.getAllMembers(screen_name, slug)
            print("\tfound {} list members...".format(len(members)))
            outpath = tUtils._checkOrMakeOutputDir("/".join([screen_name.lower(), slug]))
            tUtils.writeJson(members, os.path.join(outpath, "members.json"))
            tdata = [(m['name'], m['screen_name'], str(m['verified']), m['lang'],
                      re.sub("[\t\n\r]+", " ", m['description'])) for m in members]
            tUtils.writeTuple(tdata, os.path.join(outpath, "members.tsv"))
    except TweepError as e:
        # print("code {}.  {}".format(e['code'], e['message']))
        pass


lw = ListWalker(cred_file, appname, basedir)
sn_slug_list = get_lists_from_files(dirlist)
processSnSlugList(sn_slug_list, lw)



