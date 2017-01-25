'''
PURPOSE:
	Run collector on random Twitter stream.

Note:
	May have to change the value of outdir,
	and possibly appname (Twitter account) if it is currently used by another collector

USAGE:
	python3 random_stream.py
'''

import http
import os
import sys
import urllib3
import uuid

from http.client import IncompleteRead
from prettytable import PrettyTable

import twitterStream
# import twitterRest
from AuthClient import *

from Twitterator import *


SRC_DIR = "/Users/chagerman/Dropbox/Code/Twitterator/twitterator"
ROOT_DIR = "/Users/chagerman/Dropbox/Code/Twitterator/"




def main():
	# Define Parameters
	kind = "random"
	outdir = "/Users/chagerman/Data/Twitter_Stream"
	kwfile = None
	appname = "goat_team"
	prefix = "random"
	langs = None
	# Setup & Initialize
	cred_file, resources = init()
	init_msg(kind, appname, cred_file, ROOT_DIR, prefix)
	AC = AuthClient(cred_file)
	api, auth = AC.create_tweepy_client(appname)
	# Run random streaming collector
	collect(kind, outdir, kwfile, appname, prefix, langs)


def parseJsonData():
	import json2tsv
	import json
	path = "/Users/chagerman/Data/Twitter_Stream/16-10-03/random-20161003-110029.json"
	path = "/Users/chagerman/Data/Twitter_Stream/16-10-03/random-20161003-113440.json"
	path = "/Users/chagerman/Data/Twitter_Stream/16-10-03/random-20161003-110453.json"

	
	jdata = [x.strip() for x in open(path)]

	for data in jdata:
		tsv = json2tsv.json2tsv(json.loads(data))
		print(tsv.split("\t")[0])



t = jdata[73]
t = jdata[74]
tsv = json2tsv.json2tsv(json.loads(t))

d = json.loads(t)


if __name__ == '__main__':
	
	main()