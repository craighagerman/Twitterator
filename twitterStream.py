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
from functools import partial
import datetime
import http
from http.client import IncompleteRead
import itertools
import json
import gzip
import os
# from prettytable import PrettyTable
import re
import sys
import shutil
import threading
import time
from urllib3 import exceptions
import urllib3

# 3rd party imports : n.b. tweepy is in ~/Code since master branch in pip is broken
import tweepy
# import tweepy.StreamListener

# local imports
# UGLY HACK - IS THERE A BETTER WAY TO IMPORT?
# SRC_DIR = os.path.abspath(os.path.dirname(__file__))
# ROOT_DIR = os.path.dirname(SRC_DIR)
# sys.path.insert(0, ROOT_DIR)
from AuthClient import *





class StreamOutputListener(tweepy.StreamListener):
    
    def __init__(self, api=None, rootdir="./streaming_data/", prefix="streaming",
            counter=0, compress=True, delete_uncompressed=True, compression="gz", verbose=True):
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

    # PRIVATE METHODS ----------------------------------------------------------------------------
    # create a string corresponding to the current path to write a file to
    def _getOutpath(self, prefix):
        outpath = os.path.join(self.outdir, prefix + time.strftime('-%Y%m%d-%H%M%S') + '.json')
        return outpath

    # outdir consists of the root path plus a directory corresponding to the year-month-date
    def _set_outdir(self):
        outdir = os.path.join(self.rootdir, self._ymd())
        os.makedirs(outdir, exist_ok=True)
        print("* OUTDIR:\t{}".format(outdir))
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

    def _print_console_msg(self, status):
        if self.verbose:
            print("{:<15}\t{}".format(status.user.screen_name, re.sub(self.nlpattern, " ", status.text) ))
        else:
            sys.stdout.write(next(self.spinner) )  # write the next character
            sys.stdout.flush()                # flush stdout buffer (actual character display)
            sys.stdout.write('\b')            # erase the last written char

    # PUBLIC METHODS ----------------------------------------------------------------------------
    def on_status(self, status):
        self._print_console_msg(status)
        self.counter += 1
        json_str = json.dumps(status._json)
        self._writeJson(json_str)
        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True
 
    def on_timeout(self):
        print('Timeout ...')
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



