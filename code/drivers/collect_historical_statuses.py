
'''
DESCRIPTION
    collect all available statuses for a given list of screen_names
        i.e. the past 3000 statuses for each

    Can use Twitter REST API for this, rather than streaming.
    Therefore use TwitterRest file/class for app Auth rather than user Auth

USAGE EXAMPLES:

    cd /Users/chagerman/Twitterator

    tdir=


    python3 app/drivers/collect_historical_statuses.py  \
        --snfile /Users/chagerman/Desktop/screen_names.txt \
        --cred_file /Users/chagerman/Projects/Twitterator/twitter_credentials.json \
        --appname Crisix_3 \
        --outdir /Users/chagerman/Desktop/tmp


    python3 app/drivers/collect_historical_statuses.py  \
        --snfile /Users/chagerman/Projects/Twitterator/resources/curated_news_orgs_duplicate.txt  \
        --cred_file /Users/chagerman/Projects/Twitterator/twitter_credentials.json \
        --appname Crisix_3 \
        --outdir /Users/chagerman/Projects/NewsClassifier/InputData/profile_lists









'''
import json
import os
import sys
import argparse

# ..................................................................
# provide the Python interpreter with the path to this module
CWD_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(CWD_DIR)
PROJ_DIR = CWD_DIR.split("/app")[0]

print("CWD_DIR: {}".format(CWD_DIR))
print("ROOT_DIR: {}".format(ROOT_DIR))
print("os.path.dirname(ROOT_DIR): {}".format(os.path.dirname(ROOT_DIR)))

sys.path.append(CWD_DIR)
sys.path.append(ROOT_DIR)
sys.path.append(PROJ_DIR)
# ..................................................................

from app.twitterator.authClient import AuthClient
from app.twitterator.twitterRest import TwitterRestClient
from app.twitterator import tUtils


def main(config_dict, screen_names):
    AC = AuthClient(config_dict['cred_file'])
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(config_dict['appname'])
    client = TwitterRestClient(consumer_key, consumer_secret)
    for screen_name in screen_names:
        print("-"*60)
        print("Processing {}".format(screen_name))
        outpath = os.path.join(tUtils.checkOrMakeOutputDir(config_dict['outdir'], screen_name), "statuses.json")
        with open(outpath, "w") as fo:
            for statuses in client.get_all_statuses(screen_name):
                fo.write("\n".join([json.dumps(x) for x in statuses]))



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute word embedding with injected vocabulary.')
    parser.add_argument("--cred_file", type=str, help="path to credentials file")
    parser.add_argument("--appname", type=str, help="Twitter API app name")
    parser.add_argument("--outdir", type=str, help="path for saving model")
    parser.add_argument("--snfile", type=str, help="path to file containing a newline-delimited list of screen_names")
    args = parser.parse_args()

    config_dict = vars(args)
    screen_names = [x.strip().lower() for x in open(config_dict['snfile'])]
    main(config_dict, screen_names)




'''


config_dict = {
    'snfile':     "/Users/chagerman/Desktop/screen_names.txt",
    'cred_file':  "/Users/chagerman/Projects/Twitterator/twitter_credentials.json",
    'appname':    "Crisix_3",
    'outdir':     "/Users/chagerman/Desktop/tmp"
    }

screen_name = "craighagerman"

AC = AuthClient(config_dict['cred_file'])
access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(config_dict['appname'])
client = TwitterRestClient(consumer_key, consumer_secret)


print("processing {}".format(screen_name))
outpath = os.path.join(tUtils.checkOrMakeOutputDir(config_dict['outdir'], screen_name), "statuses.json")
statuses = client.get_all_statuses(screen_name)
with open(outpath, "w") as fo:
    json.dumps("\n".join([json.dumps(x) for x in statuses]))



'''