


# ..................................................................
# provide the Python interpreter with the path to this module
import os
import sys
SRC_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

print("SRC_DIR: {}".format(SRC_DIR))
print("ROOT_DIR: {}".format(ROOT_DIR))
print("os.path.dirname(ROOT_DIR): {}".format(os.path.dirname(ROOT_DIR)))

sys.path.append(SRC_DIR)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.dirname(ROOT_DIR))
# ..................................................................

import argparse

from app.drivers.listWalker import ListWalker


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Access Twitter REST API using Tweepy user authentication.')
    parser.add_argument("-r", "--run", help="Which Twitterator access function to run")
    parser.add_argument("-a", "--appname", help="Twitter app name to authenticate with")
    parser.add_argument("-c", "--credfile", help="Path to Twitter credentials json file")
    parser.add_argument("-o", "--basedir", help="Base directory under which to save downloaded data")
    parser.add_argument("-u", "--user", help="A single screen_name to process")
    parser.add_argument("-i", "--infile", help="Path to a file to read input data from")
    # parser.add_argument("-x", "--idx", help="Column index of the above file to extract")
    args = parser.parse_args()

    credfile = args.credfile
    appname = args.appname
    basedir = args.basedir
    lw = ListWalker(credfile, appname, basedir)

    def runner(argument):
        switcher = {
            "profile": lw.collectProfiles,
            "profileList": lw.collectProfiles_Lists_Members_fromFile,
        }
        return switcher.get(argument, "nothing")

    f = runner(args.run)
    f(args.infile)




'''
EXAMPLE USAGE

cd /Users/chagerman/Projects/Twitterator/

credfile="/Users/chagerman/Projects/Twitterator/twitter_credentials.json"
basedir="/Users/chagerman/Projects/NewsClassifier/InputData/profile_lists"
infile="/Users/chagerman/Projects/NewsClassifier/InputData/userLists/2process.txt"

python3 app/drivers/runRest.py -r profile -a xdatax -c ${credfile} -o ${basedir} -i ${infile}

python3 app/drivers/runRest.py -r profileList -a xdatax -c ${credfile} -o ${basedir} -i ${infile}


'''


