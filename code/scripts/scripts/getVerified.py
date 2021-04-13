from AuthClient import *

from twitterRest import *

appname = "CanPol"
cred_file = "../credentials.json"


verifiedFile = "/home/craig/Data/Twitter/VerifiedUsers_20170120.json"
next_cursor = "1476332539729139290"

get_all_verified(appname, cred_file, outpath, next_cursor=next_cursor)

