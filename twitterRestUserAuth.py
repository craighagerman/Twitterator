
import json
import sys
import time
# local imports
# UGLY HACK - FIND A BETTER WAY TO IMPORT
# sys.path.insert(0, "../")
from AuthClient import *

from twitter import *


appname = "CanPol"
cred_file = "../credentials.json"
AC = AuthClient(cred_file)
access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
# client = TwitterRestClient(consumer_key, consumer_secret)

# https://api.twitter.com/1.1/friendships/create.json



t = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))
# t.friendships.create(screen_name="dmrider")




'''
PURPOSE:
    given a list of screen_names for valid twitter accounts, add them to "my" accound as friends
    (i.e. people I follow). This allows me to then stream my user.timeline and get ALL of the tweets
    made by these accounts
'''

def bulkAddFriends(t, friendlist):
    profiles = []
    for user in friendlist:
        try:
            print("adding {}".format(user))
            p = t.friendships.create(screen_name=user)
            profiles.append(p)
            time.sleep(4)       # because twitter flag accounts that bulk add/drop friends too fast
        except TwitterHTTPError:
            continue
        except HTTPError:
            continue
    print("All Done!")
    return profiles



def save_json(outdir, json_data):
    try:
        with open(outdir, 'w') as f:
            f.write(json_data)
    except:
        print("ERROR in save_json...")
        print("\toutdir: {}".format(outdir))


def save_profiles(profiles, outfile):
    with open(outfile, "w") as fo:
        fo.write("\n".join([json.dumps(dict(d)) for d in profiles]))



# In [174]: len(pols)
# Out[174]: 257

# In [175]: len(parties)
# Out[175]: 17

# In [176]: len(newspapers)
# Out[176]: 108

outdir = '/Users/chagerman/Dropbox/code/Election2015/resources'

profiles = bulkAddFriends(t, parties)
save_profiles(profiles, os.path.join(outdir, "parties.json"))

profiles = bulkAddFriends(t, pols)
save_profiles(profiles, os.path.join(outdir, "incumbents.json"))

profilesn = bulkAddFriends(t, newspapers)
save_profiles(profilesn, os.path.join(outdir, "newspapers.json"))



