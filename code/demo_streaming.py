
import tweepy

import http
import urllib3
from http.client import IncompleteRead
from twitterator.twitAuthClient import TwitAuthClient
from twitterator.twitterRest import TwitterRestClient

from twitterator import twitterStream
# import twitterator.twitterStream


def foo(client, usr):
    pass


########################################################################################################################
#  Main
########################################################################################################################


def main(cred_file, appname):
    AC = TwitAuthClient(cred_file)
    # print('TwitAuthClient methods')
    # methods = [x for x in dir(AC) if not x.startswith('_')]
    # for m in methods:
    #     print(f'\t{m}')

    api, auth = AC.create_tweepy_client(appname)

    fileprefix = 'foobar'
    rootdir = '/Users/chagerman/Projects/Twitterator/data/02_stream'
    email_cred_file = '/Users/chagerman/Projects/Twitterator/credentials/email_credentials.json'
    kind = 'random'
    input_list = ['Covid']
    langs = ['en']


    # while True:

    try:
        st = twitterStream.Streamer(api, auth, rootdir, fileprefix, email_cred_file)
        if kind == "filter":
            print("KIND == FILTER")
            st.streamFilter(input_list, langs)
        elif kind == "geo":
            st.streamLocation(input_list)
        elif kind == "userlist" or kind == "userlist_newsorg":
            st.streamFriends()
        elif kind == "random":
            print("KIND == RANDOM")
            st.streamRandom(langs)
        else:
            print("Incorrect stream kind. Must be one of 'filter', 'random' or 'userlist'.")
            exit(0)

    # except http.client.IncompleteRead:
    #     continue
    # except urllib3.exceptions.ReadTimeoutError:
    #     continue
    except (KeyboardInterrupt, SystemExit):
        st.disconnect()
        print("*    KeyboardInterrupt or SystemExit caught  ")
        exit(0)




if __name__ == '__main__':
	cred_file = '/Users/chagerman/Projects/Twitterator/credentials/twitter_credentials.json'
	appname = "craighagerman"
	main(cred_file, appname)
