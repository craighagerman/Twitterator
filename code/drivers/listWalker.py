"""
    Collect Twitter list membership for a given input of Twitter screen_names
    Collect Twitter list membership for a given input Twitter lists


Vocabulary:
    to avoid confusion....
        T-list   = Twitter list (i.e. a list of 'members' created by a Twitter user
        list     = normal usage (itemized collection of items)

input file schema (one of)
    (1)     list of screen_names    (\n-delimited)
    (2)     list of T-lists          (\n-delimited)


PseudoCode .............................................................................
    for (1):
        for each screen_name:
            get a list of all T-lists
                optionally filter out any lists NOT owned by screen_name
                extract (slug, user.screen_name, description) as <T-list>.tsv
                save T-list.tsv and T-list.json (raw json response) to file to screen_name/ directory
                for each T-list:
                    do (2)

    for (2):
        for each T-list:
            get a list of members:
                extract (name, screen_name, description, verified) as members.tsv
                save list of members (raw json) and tsv to screen_name/list/ directory

........................................................................................




"""

import os
import sys

# ..................................................................
# provide the Python interpreter with the path to this module
SRC_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

print("SRC_DIR: {}".format(SRC_DIR))
print("ROOT_DIR: {}".format(ROOT_DIR))
print("os.path.dirname(ROOT_DIR): {}".format(os.path.dirname(ROOT_DIR)))

sys.path.append(SRC_DIR)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.dirname(ROOT_DIR))
# ..................................................................

import re
import time

import tweepy
from tweepy.error import TweepError

from twitterator.authorizeTweepy import AuthorizeTweepy
from twitterator import tUtils


class ListWalker:

    def __init__(self, cred_file, appname, basedir=None):
        self.basedir = basedir if not basedir==None else os.path.join(ROOT_DIR, "Output")
        print("credentials file:\t{}".format(cred_file))
        print("Twitter app name:\t{}".format(appname))
        print("base directory:\t{}".format(basedir))
        if not os.path.exists(self.basedir):
            os.mkdir(self.basedir)
        at = AuthorizeTweepy(cred_file, appname)
        self.client = at.userAuth()

    def resetClient(self, cred_file, appname):
        at = AuthorizeTweepy(cred_file, appname)
        self.client = at.userAuth()



    #
    # ......................  PUBLIC METHODS  .........................................................................
    #


    def processListOTLists(self, infile, include_subscribed=False):
        userslugs = [x.strip().split("\t")[:2] for x in open(infile)]
        try:
            for screen_name, slug in userslugs:
                print("processing name/list: {}/{}".format(screen_name, slug))
                members = self.getAllMembers(screen_name, slug)
                print("found {} list members...".format(len(members)))
                outpath = tUtils.checkOrMakeOutputDir(self.basedir, "/".join([screen_name, slug]))
                print("saving data to: {}".format(os.path.join(outpath, "members.json")))
                tUtils.writeJson(members, os.path.join(outpath, "members.json"))
                tdata = [(m['name'], m['screen_name'], str(m['verified']), m['lang'], re.sub("[\t\n\r]+", " ", m['description'])) for m in members]
                tUtils.writeTuple(tdata, os.path.join(outpath, "members.tsv"))
        except TweepError as e:
            # print("code {}.  {}".format(e['code'], e['message']))
            pass



    # def collectProfiles_Lists_Members(self, infile, include_subscribed=False):
    #     '''
    #     :param infile: a file containg a list of screen_names to process
    #     '''
    #     users = [x.strip().split("\t")[0] for x in open(infile)]
    #     for user in users:
    #         print("processing user: {}".format(user))
    #         # get and save user's profile
    #         self._output_profile(user)
    #
    #         # get and save user's list metadata
    #         jlists, tlists = self._get_lists(user, include_subscribed)
    #         outpath = tUtils.checkOrMakeOutputDir(self.basedir, user.lower())
    #         self._write(jlists, tlists, outpath, "lists")
    #
    #         # for each list (found above), get and save member metadata
    #         if tlists:
    #             for screen_name, slug, _, _ in tlists:
    #                 if not (os.path.exists(os.path.join(self.basedir, screen_name.lower(), slug, "members.json")) and os.path.exists(
    #                         os.path.join(self.basedir, screen_name.lower(), slug, "members.tsv"))):
    #                     try:
    #                         jmembers, tmembers = self._get_list_members(screen_name, slug)
    #                         outpath = tUtils.checkOrMakeOutputDir(self.basedir, "/".join([screen_name.lower(), slug]))
    #                         self._write(jmembers, tmembers, outpath, "members")
    #                     except TweepError as e:
    #                         pass


    def get_users(self, infile):
        return [x.strip().split("\t")[0] for x in open(infile)]

    def collectProfiles_Lists_Members_fromFile(self, infile, include_subscribed=False):
        users = self.get_users(infile)
        self.collectProfiles_Lists_Members(users)

    def collectProfiles_Lists_Members(self, users, include_subscribed=False):
        '''
        :param infile: a file containg a list of screen_names to process
        '''

        for user in users:
            print("processing user: {}".format(user))
            # get and save user's profile
            self._output_profile(user)

            # get and save user's list metadata
            jlists, tlists = self._get_lists(user, include_subscribed)
            outpath = tUtils.checkOrMakeOutputDir(self.basedir, user.lower())
            self._write(jlists, tlists, outpath, "lists")

            # for each list (found above), get and save member metadata
            if tlists:
                for screen_name, slug, _, _ in tlists:
                    if not (os.path.exists(os.path.join(self.basedir, screen_name.lower(), slug, "members.json")) and os.path.exists(
                            os.path.join(self.basedir, screen_name.lower(), slug, "members.tsv"))):
                        try:
                            jmembers, tmembers = self._get_list_members(screen_name, slug)
                            outpath = tUtils.checkOrMakeOutputDir(self.basedir, "/".join([screen_name.lower(), slug]))
                            self._write(jmembers, tmembers, outpath, "members")
                        except TweepError as e:
                            pass



    #......................................................................
    #
    # Lists
    #
    # read a file containing a list of screen_names. For each get a list of their lists
    # save results to files <basedir><screen_name>lists.<json|tsv>
    def collectUsersLists(self, infile, include_subscribed=False):
        users = [x.strip().split("\t")[0] for x in open(infile)]
        for user in users:
            jlists, tlists = self._get_lists(user)
            outpath = tUtils.checkOrMakeOutputDir(self.basedir, user.lower())
            self._write(jlists, tlists, outpath, "lists")

    #......................................................................
    #
    # Profiles
    #
    def collectProfiles(self, infile):
        users = [x.strip().split("\t")[0] for x in open(infile)]
        for user in users:
            self._output_profile(user)


    #
    # ......................  PRIVATE METHODS  .......................................................................
    #
    # ------------------------------------------------------------------
    #   Get profile metadata for a given user
    # ------------------------------------------------------------------
    def _get_profile(self, user):
        print("profiling user: {}".format(user))
        p = self.client.get_user(user)
        jprofile = p._json
        tprofile = self._tupify(jprofile)
        # tprofile = (p.name, p.screen_name, p.description, p.verified, p.lang, p.followers_count, p.statuses_count, p.location, p.time_zone)
        return jprofile, tprofile

    def _output_profile(self, user):
        # if not (os.path.exists(os.path.join(self.basedir, user, "profile.json")) and os.path.exists(
        #         os.path.join(self.basedir, user, "profile.tsv"))):
            try:
                jprofile, tprofile = self._get_profile(user)
                outpath = tUtils.checkOrMakeOutputDir(self.basedir, user.lower())
                self._write([jprofile], [tprofile], outpath, "profile")
            except Exception:
                print("Exception encountered with user: ({})".format(user))



    # ------------------------------------------------------------------
    #   Get all list metadata for a given user
    # ------------------------------------------------------------------
    def _get_lists(self, user, include_subscribed=False):
        jlists = []
        tlists = []
        if not (os.path.exists(os.path.join(self.basedir, user, "lists.json")) and os.path.exists(
                os.path.join(self.basedir, user, "lists.tsv"))):
            print("processing user: {}".format(user))
            # find out what lists the user has created
            ulists = self.client.lists_all(screen_name=user)
            if include_subscribed:
                ulists = [x for x in ulists if x.user.screen_name == user]
            jlists = self._jsonifyListData(ulists)
            tlists = [(ul.user.screen_name, ul.slug, ul.uri, ul.description) for ul in ulists]
            print("found {} lists ...".format(len(tlists)))

        return jlists, tlists








    # ------------------------------------------------------------------
    #   Get all the members in a given user's given list
    # ------------------------------------------------------------------
    # NOTE: tweepy User object contains both original json as a _json field
    #       as well as _ALL_ the same data in a class-like structure.
    #       It is only necessary to save the raw json as retrieved from Twitter
    def _get_list_members(self, screen_name, slug):
        ''' Return a list of json objects (twitter user json)'''
        jmembers = []
        for member in tweepy.Cursor(self.client.list_members, screen_name, slug).items():
            jmembers.append(member._json)
        tmembers = [
            (m['name'], m['screen_name'], str(m['verified']), m['lang'], re.sub("[\t\n\r]+", " ", m['description'])) for
            m in jmembers]
        return jmembers, tmembers


    def _jsonifyListData(self, ulists):
        def jsonify(ul):
            return {"slug": ul.slug,
                    "uri": ul.uri,
                    "description": re.sub("[\t\n\r]+", " ", ul.description),
                    "id_str": ul.id_str,
                    "member_count": ul.member_count,
                    "users": {
                    "name": ul.user.name,
                    "screen_name ": ul.user.screen_name,
                    "description": re.sub("[\t\n\r]+", " ", ul.user.description),
                    "followers_count": ul.user.followers_count,
                    "statuses_count ": ul.user.statuses_count,
                    "verified": ul.user.verified,
                    "lang": ul.user.lang,
                    "time_zone": ul.user.time_zone,
                    "url": ul.user.url,
                    "location": ul.user.location,
                    }}
        return [jsonify(ul) for ul in ulists]

    def _tupify(self, jd):
        n = jd['name']
        sn = jd['screen_name']
        des = jd['description']
        v = jd['verified']
        l = jd['lang']
        fc = jd['followers_count']
        sc = jd['statuses_count']
        lc = jd['listed_count']
        loc = jd['location']
        tz = jd['time_zone']
        url = jd['url']
        if 'entities' in jd:
            if 'url' in jd['entities']:
                if 'urls' in jd['entities']['url']:
                    if 'display_url' in jd['entities']['url']['urls'][0]:
                        url = jd['entities']['url']['urls'][0]['display_url']
        result = [n, sn, des, v, l, fc, sc, lc, loc, tz, url]
        result = map(str, result)
        result = map(lambda x: re.sub("[\t\n\r]+", " ", x), result)
        return result

    #
    # ......................  OUTPUT METHODS  .........................................................................
    #

    def _write(self, jdata, tdata, outdir, identifier):
        # save json/TSV T-list data
        tUtils.writeJson(jdata, os.path.join(outdir, "{}.json".format(identifier)))
        # tdata = [list(map(lambda y: re.sub("[\t\n\r]+", " ", str(y)), x)) for x in tdata]
        tUtils.writeTuple(tdata, os.path.join(outdir, "{}.tsv".format(identifier)))





if __name__ == '__main__':
    '''
    cd Twitterator
    from app.drivers.listWalker import ListWalker
    '''






    #
    #   Input Parameters
    #
    appname = "xdatax"
    cred_file = "/Users/chagerman/Projects/Twitterator/twitter_credentials.json"
    basedir = "/Users/chagerman/Projects/NewsClassifier/InputData/profile_lists"

    lw = ListWalker(cred_file, appname, basedir)

    infile = "/Users/chagerman/Projects/NewsClassifier/InputData/inputLists/all_users.txt"
    lw.collectProfiles(infile)


    '''

    #
    #  Collect Profiles
    #
    infile = "/Users/chagerman/Projects/NewsClassifier/InputData/newsOrgs/friends_of_AllTwittterNews.txt"
    lw.collectProfiles(infile)

    user = "craighagerman"
    pj, pt = lw._get_profile(user)




    #
    #   Collect Profiles, Lists, Members
    #
    infile = "/Users/chagerman/Projects/NewsClassifier/InputData/possible_news_accounts2.txt"
    users = lw.get_users(infile)

    lw.collectProfiles_Lists_Members(users)



    '''