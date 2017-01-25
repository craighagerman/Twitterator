#coding: utf-8
#!/usr/bin/python
'''
    PURPOSE:  Pull data from Twitter using the Streaming API, using the Tweepy library

    NOTE:
    The default access level allows up to
        400 track keywords
        5,000 follow userids
        25 0.1-360 degree location boxes.
'''
# builtin imports
import datetime
import gzip
import http
import itertools
import json
import os
import re
import shutil
import sys
import threading
import time
import urllib3

from functools import partial
from http.client import IncompleteRead
from urllib3 import exceptions

# 3rd party imports : n.b. tweepy is in ~/Code since master branch in pip is broken for Python3
import tweepy

# local imports
from AuthClient import *
from email_logger import *


class StreamOutputListener(tweepy.StreamListener):
    def __init__(self, api=None, rootdir="./streaming_data/", prefix="streaming",
            counter=0, compress=True, delete_uncompressed=True, compression="gz", verbose=False):
        self.MAXTWEETS = 100000
        self.spinner = itertools.cycle(['-', '/', '|', '\\'])
        self.verbose = verbose
        self.counter = counter
        self.compress = compress
        self.delete_uncompressed = delete_uncompressed
        self.compression = compression
        self.api = api or API()
        self.nlpattern = re.compile(r"[\n|\t|\r]+")
        self.prefix = prefix
        self.rootdir = rootdir
        self.outdir = self._set_outdir()
        self.outpath = self._getOutpath(prefix)
        self.today = self._ymd()
        self.fo = open(self.outpath, "a")
        self.rate_counter = 0
        self.epochtime = time.time()

        # Initialize logger with TLS SMTP emailing capability
        email_cred_file = "../email_credentials.json"
        logger = EmailLogger(email_cred_file)
        identifier = prefix          # unique twitter collector identifier or app name
        logger.create_logger(identifier)

    # PRIVATE METHODS ----------------------------------------------------------------------------
    # create a string corresponding to the current path to write a file to
    def _getOutpath(self, prefix):
        outpath = os.path.join(self.outdir, prefix + time.strftime('-%Y%m%d-%H%M%S') + '.json')
        return outpath

    # outdir consists of the root path plus a directory corresponding to the year-month-date
    def _set_outdir(self):
        outdir = os.path.join(self.rootdir, self._ymd())
        os.makedirs(outdir, exist_ok=True)
        # print("* OUTDIR:\t{}".format(outdir))
        logging.debug("* OUTDIR:\t{}".format(outdir))
        return outdir

    # get the current year-month-date string
    def _ymd(self):
        return datetime.date.today().strftime("%y-%m-%d")

    # GZIP compress existing file
    def _gzip_it(self, inpath):
        outpath = inpath + ".gz"
        with open(inpath, 'rb') as f_in:
            with gzip.open(outpath, 'wb') as f_out:
                f_out.writelines(f_in)
        if self.delete_uncompressed:
            self._deleteFile(inpath)

    # remove uncompressed file (after compressing it)
    def _deleteFile(self, path):
        os.remove(path)

    def _is_new_day(self):
        result = self._ymd() != self.today
        self.today = self._ymd()
        return result

    def _resetOutput(self):
            self.fo.close()
            if self.compress:
                threading.Thread(target=self._gzip_it, args=[self.outpath]).start()
            self.outdir = self._set_outdir()
            self.outpath = self._getOutpath(self.prefix)
            self.fo = open(outpath, "a")
            self.counter = 0

    def _writeJson(self, json_str):
        self.fo.write(json_str + "\n")
        if (self.counter >= self.MAXTWEETS) or (self._is_new_day()):
            self._resetOutput()

    # def _print_console_msg(self, status):
    #     if self.verbose:
    #         print("{:<15}\t{}".format(status.user.screen_name, re.sub(self.nlpattern, " ", status.text) ))
    #     else:
    #         sys.stdout.write(next(self.spinner) )  # write the next character
    #         sys.stdout.flush()                # flush stdout buffer (actual character display)
    #         sys.stdout.write('\b')            # erase the last written char

    def _log_tweet(self, status):
        logging.debug("{:<15}\t{}".format(status.user.screen_name, re.sub(self.nlpattern, " ", status.text) ))

    def _log_rate(self):
        n_sec = time.time() - self.epochtime
        self.epochtime = time.time()
        n_tweets = self.rate_counter
        self.rate_counter = 0
        rate = n_tweets / n_sec
        logging.info("Number of tweets-per-minute: {}".format(int(rate * 60)))
        # logging.info("# tweets:  {}".format(n_tweets))
        # logging.info("# seconds: {}".format(n_sec))


    # PUBLIC METHODS ----------------------------------------------------------------------------
    def on_status(self, status):
        # self._print_console_msg(status)
        n = 10                                                # number of min to sample tweets
        if (time.time() >= (self.epochtime + (n * 60)) ):     # log the tweets-per-min rate every n min.
            self._log_rate()
        self._log_tweet(status)
        self.counter += 1
        self.rate_counter += 1
        json_str = json.dumps(status._json)
        self._writeJson(json_str)
        return True

    def on_error(self, status_code):
        # print('Got an error with status code: ' + str(status_code))
        logging.error("Error with status code {}".format(str(status_code)))
        return True
 
    def on_timeout(self):
        # print('Timeout ...')
        logging.error("Timeout")
        return True
 

class Streamer():
    def __init__(self, api, auth, rootdir, fileprefix):
        self.stream = self._setup(api, auth, rootdir, fileprefix)

    def _setup(self, api, auth, rootdir, fileprefix):
        listener = StreamOutputListener(api, rootdir, fileprefix)
        stream = tweepy.streaming.Stream(auth, listener)
        return stream

    def streamRandom(self, langs):
        if langs:
            self.stream.sample(languages=langs)
        else:
            self.stream.sample()

    def streamFilter(self, track_terms, langs):
        if langs:
            self.stream.filter(track=track_terms, languages=langs)
        else:
            self.stream.filter(track=track_terms)

    def streamLocation(self, geo_bounds):
        # e.g geo_bounds = [-6.38,49.87,1.77,55.81]
        # westlimit=-14.02; southlimit=49.67; eastlimit=2.09; northlimit=61.06
        self.stream.filter(locations=geo_bounds)

    '''  Return all tweets/retweets/replies of a list of users '''
    def streamUserList(self, follow_list):
        self.stream.filter(follow=follow_list)

    '''  Return tweets sent from users "I" follow (i.e. the Twitter account associated with the appname)  '''
    def streamFriends(self):
        self.stream.userstream(_with='followings')

    def disconnect(self):
        self.stream.disconnect()



