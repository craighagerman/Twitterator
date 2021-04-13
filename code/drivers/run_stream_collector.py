'''
Driver for streaming random tweets from the Twitter firehose
Example Usage:


#twitdir="/Users/chagerman/Projects/Twitterator"
#outdir="/Users/chagerman/Projects/Twitterator/tweet_data"

twitdir="/home/ubuntu/Twitterator"
outdir="/data/tweet_data"


# COLLECT en RANDOM FROM THE FIREHOSE ..........................................
python3 app/drivers/run_stream_collector.py --cred_file ${twitdir}/credentials.json --email_cred ${twitdir}/email_credentials.json --appname mProbe --kind random --outdir ${outdir} --prefix random_en --langs en


# COLLECT tweets from AllNewsListed
python3 app/drivers/run_stream_collector.py --cred_file ${twitdir}/twitter_credentials.json --email_cred ${twitdir}/email_credentials.json --appname newsynews --kind userlist --outdir ${outdir} --prefix allNews



'''
import http
import os
import sys

# ..................................................................
# provide the Python interpreter with the path to this module
import urllib3

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

import argparse
import os

from app.twitterator.authClient import AuthClient
from prettytable import PrettyTable

import app.twitterator.twitterStream






def main(config_dict):
    kind = config_dict['kind']
    cred_file = os.path.join(ROOT_DIR, "credentials.json") if not config_dict['cred_file'] else  config_dict['cred_file']
    email_cred_file = config_dict['email_cred']
    appname = config_dict['appname']
    prefix = config_dict['prefix']
    langs = None if not config_dict['langs'] else config_dict['langs'].split(",")
    output_dir = config_dict['outdir']
    kwfile = None if not config_dict['kwfile'] else config_dict['kwfile']
    kwlist = None if not kwfile else [x.strip() for x in open(kwfile)]
    geo_bounds = None if not config_dict['geo'] else [float(x) for x in config_dict['geo'].split(",")]
    input_list = None
    if kind == "filter":
        input_list = kwlist
    elif kind == "geo":
        input_list = geo_bounds
    init_msg(config_dict)
    runStreamer(kind, appname, cred_file, os.path.join(output_dir, prefix), prefix, input_list, langs, email_cred_file)


def init_msg(config_dict):
    kind = config_dict['kind']
    cred_file = os.path.join(ROOT_DIR, "credentials.json") if not config_dict['cred_file'] else  config_dict['cred_file']
    email_cred_file = config_dict['email_cred']
    appname = config_dict['appname']
    prefix = config_dict['prefix']
    langs = None if not config_dict['langs'] else config_dict['langs'].split(",")
    output_dir = config_dict['outdir']
    kwfile = None if not config_dict['kwfile'] else config_dict['kwfile']
    kwlist = None if not kwfile else [x.strip() for x in open(kwfile)]
    geo_bounds = None if not config_dict['geo'] else [float(x) for x in config_dict['geo'].split(",")]

    t = PrettyTable(["Variable", "Details"])
    t.align["Variable"] = "l"  # Left align
    t.align["Details"] = "l"  # Left align
    t.add_row(["Twitter Application name", appname])
    t.add_row(["Stream Kind", kind])
    t.add_row(["File Prefix", prefix])
    t.add_row(["Credentials File:", cred_file])
    t.add_row(["Email Credentials File:", email_cred_file])
    t.add_row(["Output Data Directory", output_dir])
    t.add_row(["Languages", langs])
    t.add_row(["Geo Bounds", geo_bounds])
    t.add_row(["Track Terms", kwlist])
    print(t)
    print("\n")


def runStreamer(kind, appname, cred_file, output_dir, fileprefix, input_list, langs=None, email_cred_file="../email_credentials.json"):
    AC = AuthClient(cred_file)
    api, auth = AC.create_tweepy_client(appname)
    while True:
        try:
            st = app.twitterator.twitterStream.Streamer(api, auth, output_dir, fileprefix, email_cred_file)
            if kind == "filter":
                st.streamFilter(input_list, langs)
            elif kind == "geo":
                st.streamLocation(input_list)
            elif kind == "userlist" or kind == "userlist_newsorg":
                st.streamFriends()
            elif kind == "random":
                print("\nRANDOM STREAM...\n")
                st.streamRandom(langs)
            else:
                print("Incorrect stream kind. Must be one of 'filter', 'random' or 'userlist'.")
                exit(0)
        except (KeyboardInterrupt, SystemExit):
            st.disconnect()
            print("*    KeyboardInterrupt or SystemExit caught  ")
            exit(0)
        except (AttributeError, http.client.IncompleteRead, urllib3.exceptions.ReadTimeoutError):
            continue
        # except http.client.IncompleteRead:
        #     continue
        # except urllib3.exceptions.ReadTimeoutError:
        #     continue
        except:
            continue




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute word embedding with injected vocabulary.')
    parser.add_argument("--cred_file", type=str, help="path to credentials file")
    parser.add_argument("--email_cred", type=str, help="path to email credentials file")
    parser.add_argument("--appname", type=str, help="Twitter API app name")
    parser.add_argument("--kind", type=str, help="kind of streaming collection {random, filter, geo, userlist}")
    parser.add_argument("--outdir", type=str, help="path for saving model")
    parser.add_argument("--kwfile", type=str, help="path to file containing track_term keywords for filtering firehose")
    parser.add_argument("--prefix", type=str, help="name used for sub-directory and file prefixes")
    parser.add_argument("--langs", type=str, help="comma-separated list of languages")
    parser.add_argument("--geo", type=str, help="comma-separated list of 4 geo bounds")

    args = parser.parse_args()

    config_dict = vars(args)

    # if len(vars(args)) == 0:
    #     parser.print_help()
    #     parser.exit(message="Incorrect number of command line arguments given")
    #
    # if args.config:
    #     print("Parsing config file: {}".format(args.config))
    #     config_dict = json.loads(open(args.config).read())
    # else:
    #     for k, v in vars(args).items():
    #         if not k in {"config", "max_vocab_size"}:
    #             if v is None:
    #                 parser.exit(message="Error: {} must be initialized".format(k))
    #     config_dict = vars(args)
    #
    #     print('config_dict["input_data"] = '.format(config_dict["input_data"] ))

    main(config_dict)

