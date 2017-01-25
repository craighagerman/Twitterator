# builtin imports
import datetime
import gzip
import http
import itertools
import json
import os
import re
import shutil
import uuid
import sys
import threading
import time
import urllib3

from functools import partial
from http.client import IncompleteRead
from prettytable import PrettyTable
from urllib3 import exceptions


from http.client import IncompleteRead
from prettytable import PrettyTable

from twitterRest import *


# 3rd party imports : n.b. tweepy is in ~/Code since master branch in pip is broken
import tweepy

# local imports
# UGLY HACK - IS THERE A BETTER WAY TO IMPORT?
# sys.path.insert(0, "../")
from AuthClient import *
from twitterStream import *


appname = "CanPol"
cred_file = "/Users/chagerman/Dropbox/Code/Twitterator/credentials.json"
AC = AuthClient(cred_file)
access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
client = TwitterRestClient(consumer_key, consumer_secret)


# screen_name = "JustinTrudeau"
# # EXAMPLE: how to add 'friends' by screen_name
# newfriend = client.add_friend(screen_name)

# # EXAMPLE: how to get profile information for a single user
# profile = client.get_single_user(usr)

# # EXAMPLE: how to get profile information for a list of users
# id_list = ["783214", "6253282"]
# profiles = get_users_lookup(id_list, id_type="user_id")


ctrlsec_file = "/Users/chagerman/Data/ISIL_accounts/CTRLSecAnonymous_suspectedISILAccounts.txt"
suspected_file = "/Users/chagerman/Data/ISIL_accounts/suspectedISIL.tsv"


def get_user_ids(path):
    return (x.strip().split("\t")[0] for x in open(path) if not path.startswith("#"))

user_id_list = list(set(list(get_user_ids(ctrlsec_file)) + list(get_user_ids(suspected_file))))


outfile = "/Users/chagerman/Data/ISIL_accounts/twitter_profiles.json"

with open(outfile, "w") as fo:
    for i in range(0, len(user_id_list), 100):
        print("processing block {}".format(i))
        user_ids = user_id_list[i: i + 100]
        profiles = client.get_users_lookup(user_ids, id_type="user_id")
        for profile in profiles:
            fo.write(json.dumps(profile) + "\n")
        time.sleep(15)
