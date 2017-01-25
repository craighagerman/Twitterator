# coding: utf-8
#!/usr/bin/python
'''
    PURPOSE:  Pull data from Twitter using the REST API, using the application_only_auth library
'''
# builtin imports
import json
import os
import re
import sys
import time
import urllib.parse
# 3rd party imports
# UGLY HACK - IS THERE A BETTER WAY TO IMPORT?
# SRC_DIR = os.path.abspath(os.path.dirname(__file__))
# ROOT_DIR = os.path.dirname(SRC_DIR)
# sys.path.insert(0, ROOT_DIR)
import application_only_auth

from AuthClient import *


class TwitterRestClient(application_only_auth.Client):

    def __init__(self, consumer_key, consumer_secret):
        super().__init__(consumer_key, consumer_secret)
        self.API_ENDPOINT = 'https://api.twitter.com'
        self.API_VERSION = '1.1'

    # private methods
    def _concatParam(self, d):
        return "&".join(["=".join([k, d[k]]) for k in d])

    def _queryRestApi(self, resource, parameters):
        query = "{}/{}/{}?{}".format(self.API_ENDPOINT, self.API_VERSION,
                                     resource, self._concatParam(parameters))
        print("\n\tQuery:\t{}\n".format(query))
        return self.request(query)

    def _get_community(self, screen_name, resource, cursor, skip_status, include_user_entities):
        parameters = {"screen_name": screen_name,
                      "count": "200",
                      "include_rts": "false",
                      "cursor": cursor,
                      "skip_status": skip_status}
        return self._queryRestApi(resource, parameters)

    def _get_statuses(self, screen_name, resource, max_id=None):
        parameters = {"screen_name": screen_name,
                      "count": "200",
                      "include_rts": "false"}
        if max_id:
            parameters.update({"max_id": max_id})
        return self._queryRestApi(resource, parameters)

    # public methods
    # GET users/show rate limit: 180 / 15 min
    def get_single_user(self, screen_name):
        '''  (Previously get_profile) Return the profile metadata associated with a single user's screen_name  '''
        resource = "users/show.json"
        parameters = {"screen_name": screen_name}
        return self._queryRestApi(resource, parameters)

    # GET statuses/user_timeline rate limit: 300 / 15 min
    def get_user_timeline(self, screen_name, max_id=None):
        resource = "statuses/user_timeline"
        return self._get_statuses(screen_name, resource, max_id)

    # GET statuses/user_timeline rate limit: 300 / 15 min
    def get_home_timeline(self, screen_name, max_id=None):
        resource = "statuses/user_timeline"
        resource = "statuses/user_timeline"
        return self._get_statuses(screen_name, resource, max_id)

    def get_lists(self, screen_name):  # GET lists/list rate limit: 15 / 15 min
        resource = "lists/list.json"
        parameters = {"screen_name": screen_name}
        return self._queryRestApi(resource, parameters)

    def get_list_members(self, list_id):                        # GET lists/members rate limit: 180 / 15 min
        resource = "lists/members.json"
        parameters = {"list_id": list_id}
        return self._queryRestApi(resource, parameters)

    # GET friends/list rate limit: 30 / 15 min
    def get_friends(self, screen_name, cursor="-1", skip_status="false", include_user_entities="false"):
        resource = "friends/list.json"
        return self._get_community(screen_name, resource, cursor, skip_status, include_user_entities)

    # GET followers/list rate limit: 30 / 15 min
    def get_followers(self, screen_name, cursor="-1", skip_status="false", include_user_entities="false"):
        resource = "followers/list.json"
        return self._get_community(screen_name, resource, cursor, skip_status, include_user_entities)

    # TODO: confirm that the following are working
    def get_mentions(self, screen_name):
        '''   '''
        resource = "statuses/mentions_timeline.json"
        parameters = {"screen_name": screen_name}
        return self._queryRestApi(resource, parameters)

    def get_single_tweet(self, tweet_id):
        ''' Return a single tweet for a given numerical tweet_id '''
        resource = "statuses/show.json"
        parameters = {"tweet_id": tweet_id}
        return self._queryRestApi(resource, parameters)

    # app_auth = 60/15 min   user_auth = 180/15 min
    def get_users_lookup(self, id_list, id_type="screen_name"):
        '''  Return the profile metatdata associated with a list of screen_names (max len = 100)
            id_type = {screen_name, user_id'''
        resource = "users/lookup.json"
        parameters = {id_type: ",".join(id_list)}
        return self._queryRestApi(resource, parameters)

    # GET statuses/lookup rate limit: 60 / 15 min
    def get_statuses_lookup(self, tweet_id_list):
        ''' Return statuses associated with up to 100 tweet_ids  '''
        resource = "statuses/lookup.json"
        parameters = {"id": ",".join(tweet_id_list)}
        return self._queryRestApi(resource, parameters)

    # --------- WON'T WORk - NEEDS USER AUTH ---------
    # # def create_list(self, name, mode, description):
    # def create_list(self, name):
    #     '''  Create a new list for the authenicated user. n.b. cannot have more
    #          than 1000 lists per accounts. '''
    #     resource = "lists/create.json"
    #     # parameters = {"name": name, "mode": mode, "description": description}
    #     parameters = {"name": name}
    #     return self._queryRestApi(resource, parameters)
    #
    # def add_members_to_list(self, list_id, screen_names):
    #     ''' add members contained in screen_names to list given by list_id.
    #         Can add 100 comma-separated screen_names. nb. Lists cannot have more
    #         than 5000 members. '''
    #     resource = "lists/members/create_all.json"
    #     parameters = {"list_id": list_id,  "screen_name": ",".join(screen_names)}
    #     return self._queryRestApi(resource, parameters)
    #
    # def add_friend(self, screen_name):
    #     # https://api.twitter.com/1.1/friendships/create.json
    #     resource = "friendships/create.json"
    #     parameters = {"screen_name": screen_name}
    #     return self._queryRestApi(resource, parameters)

    ''' n.b. Limit searches to 10 keywords and operators '''

    def search_historical(self, search_terms, lang=None, max_id=None):
        resource = "search/tweets.json"
        query = ",".join(search_terms)
        parameters = {"q": query, "count": "200"}
        if lang:
            parameters.update({"lang": lang})
        if max_id:
            parameters.update({"max_id": max_id})
        return self._queryRestApi(resource, parameters)



#e.g.
#getAllFriends(appname, cred_file, "AllTwittterNews", outpath)
def getAllFriends(appname, cred_file, usr, outpath):
    AC = AuthClient(cred_file)
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    client = TwitterRestClient(consumer_key, consumer_secret)
    next_cursor = "-1"
    num_results = 0
    fo = open(outpath, "w")
    while next_cursor != "0":
        response = client.get_friends(usr, cursor=next_cursor)
        next_cursor = response['next_cursor_str']
        users = response['users']
        num_results += len(users)
        print("Total number downloaded: {}".format(num_results))
        for u in users:
            json_str = json.dumps(u)
            fo.write(json_str + "\n")
        time.sleep(3)
    fo.close()




# can be used for collecting all verified from the start or updating list
# To update you just need to specify the last cursor (look at the previous logs)
# n.b. currently over 250k
# Rate Limits
# GET friends/list  friends 15  15
#
#        Query:  https://api.twitter.com/1.1/friends/list.json?count=200&screen_name=verified&skip_status=false&cursor=1476332539729139290&include_rts=false
#
#Total number downloaded: 67599 / 239658
#
def get_all_verified(appname, cred_file, verifiedFile, next_cursor="-1"):
    usr = "verified"
    AC = AuthClient(cred_file)
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    client = TwitterRestClient(consumer_key, consumer_secret)
    profile = client.get_single_user(usr)
    num_friends = profile['friends_count']
    fo = open(verifiedFile, "a")
    num_results = 0
    while num_results < num_friends-1:
        result = client.get_friends(usr, cursor=next_cursor)
        next_cursor = result['next_cursor_str']
        users = result['users']
        num_results += len(users)
        print("Total number downloaded: {} / {}".format(num_results, num_friends))
        for u in users:
            u["next_cursor"] = next_cursor
            u["cursor"] = result['cursor_str']
            json_str = json.dumps(u)
            fo.write(json_str + "\n")
        time.sleep(60)
    fo.close()





# def run(streamkind, appname, cred_file, rootdir, fileprefix):
def update_verified(appname, cred_file, verifiedFile):
    usr = "verified"
    updatedVerifedFile = ".tempUpdatedVerifiedFile.json"
    AC = AuthClient(cred_file)
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    client = TwitterRestClient(consumer_key, consumer_secret)
    profile = client.get_single_user(usr)
    num_friends = profile['friends_count']
    num_required =  num_friends - sum(1 for i in (line.strip() for line in open(verifiedFile)))
    fo = open(updatedVerifedFile, "w")
    num_results = 0
    while num_results < num_required:
        result = client.get_friends(usr)
        next_cursor = result['next_cursor_str']
        users = result['users']
        num_results += len(users)
        print("Total number downloaded: {}".format(num_results))
        for u in users:
            json_str = json.dumps(u)
            fo.write(json_str + "\n")
        time.sleep(5)
    fo.close()
    mergedVerified(verifiedFile, updatedVerifedFile)


def mergedVerified(verifiedFile, updatedVerifedFile):
    vusers = set([])
    vlines = (line.strip() for line in open(verifiedFile))
    for line in vlines:
        d = json.loads(line)
        vusers.add(d['id_str'])
    nvlines = (line.strip() for line in open(updatedVerifedFile))
    with open(verifiedFile, "a") as fo:
        for line in nvlines:
            d = json.loads(line)
            usr = d['id_str']
            if not usr in vusers:
                fo.write(line + "\n")
    os.remove(updatedFile)


def makeTSV(verifiedFile, outputTSVfile):
    nlpattern = re.compile(r"[\n|\t|\r]+")
    vlines = (line.strip() for line in open(verifiedFile))
    with open(outputTSVfile, "w") as fo:
        for line in vlines:
            d = json.loads(line)
            tsv = "\t".join(list(map(lambda x: re.sub(nlpattern, " ", str(x)), [d['id_str'], d['screen_name'], d['name'], d['lang'], d['description'], d[
                            'statuses_count'], d['friends_count'], d['followers_count'], d['listed_count'], d['location'], d['time_zone'], d['url']])))
            fo.write(tsv + "\n")





if __name__ == '__main__':
    SRC_DIR = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.dirname(SRC_DIR)
    print("SCR DIR: {}".format(SRC_DIR))
    print("ROOT DIR: {}".format(ROOT_DIR))
    cred_file = "../credentials.json"
    default_cred_file = os.path.join(ROOT_DIR, "credentials.json")
    print(default_cred_file)
    appname = "Crisix"
    run(appname, default_cred_file)

    # Update verified friends with recent additions.
    appname = "Crisix"
    cred_file = "../credentials.json"
    verifiedFile = "/Users/chagerman/Projects/Sentiment/News_Organizations/cache/verified-accounts.json"
    # update_verified(appname, cred_file, verifiedFile)



# --------------------------------------------------------------------------------------------------------------
def getClient(appname, cred_file):
    AC = AuthClient(cred_file)
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    client = TwitterRestClient(consumer_key, consumer_secret)
    return client

def make_friends(appname, cred_file, usr):
    client = getClient(appname, cred_file)
    newfriend = client.add_friend(usr)
    profile = client.get_single_user(usr)




def backfill(appname, cred_file, search_terms, outfile):
    import json
    import time
    client = getClient(appname, cred_file)
    with open(outfile, "w") as fo:
        for search_term in search_terms:
            kw = urllib.parse.quote(search_term)        # have to convert to ASCII % representation
            result = client.search_historical([kw])
            statuses = result['statuses']
            print("{} results returned for {}".format(len(statuses), search_term))
            jstr = [json.dumps(s) for s in statuses]
            fo.write("\n".join(jstr))
            time.sleep(1)









''' Receive tweepy API and a list of user screen_names
    Return a list of expanded details on each of the users
'''


def queryUserList(api, userlist, outfile):
    udetails = []
    with open(outfile, "a") as fo:
        for user in userlist:
            u = api.get_user(user)._json
            json_str = json.dumps(u)
            fo.write(json_str + "\n")
            # print(u['id_str'] + "\t" +  u['screen_name'] + "\t" +  u['name'] + "\t" +  u['entities']['url']['urls'][0]['expanded_url'] + "\t" + str(u['statuses_count']) + "\t" +  u['location'] + "\t" + u['time_zone'])
            userdetails = [u['id_str'], u['screen_name'], u['name'],
                           str(u['statuses_count']), u['location'], u['time_zone']]
            userdetails = list(map(lambda x: str(x), userdetails))
            print("\t".join(userdetails))
            udetails.append(userdetails)
            time.sleep(6)
    return udetails


'''
# NOTES
=======



It's been, like, four months of, like, AMAZING summer ... and now its like, coming down...


'''
