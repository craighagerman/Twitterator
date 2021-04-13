
"""
Concatenate all downloaded profile information into a single TSV file

Given a directory containing sub-directories of screen_names. e.g.
    profile_lists
        user_1
            list1
                members.json
                members.tsv
            lists.json
            lists.tsv
            profile.json
            profile.tsv
        user_2
            list1
                members.json
                members.tsv
            lists.json
            lists.tsv
            profile.json
            profile.tsv


    walk through all user directories, parse profile.json to extract the following fields:
        name
        screen_name
        description
        verified
        lang
        followers_count
        statuses_count
        listed_count
        location
        time_zone

"""

import json
import os
import re


profile_list_dir = "/Users/chagerman/Projects/NewsClassifier/InputData/profile_lists"
paths = [os.path.join(profile_list_dir, f, "profile.json") for f in os.listdir(profile_list_dir) if os.path.isdir(os.path.join(profile_list_dir, f))]
paths = [p for p in paths if os.path.exists(p)]


outfile = "/Users/chagerman/Projects/NewsClassifier/InputData/userLists/all_profiles.tsv"


jdata = [json.load(open(p)) for p in paths]


def tupify(jd):
    n = jd['name']
    sn = jd['screen_name']
    des = jd['description']
    v = jd['verified']
    l = jd['lang']
    fc = jd['followers_count']
    sc = jd['statuses_count']
    lc = jd['listed_count']
    loc = jd['location']
    tz = jd['time_zone']
    url = jd['url']
    if 'entities' in jd:
        if 'url' in jd['entities']:
            if 'urls' in jd['entities']['url']:
                if 'display_url' in jd['entities']['url']['urls'][0]:
                    url = jd['entities']['url']['urls'][0]['display_url']
    result = [n, sn, des, v, l, fc, sc, lc, loc, tz, url]
    result = map(str, result)
    result = map(lambda x: re.sub("[\t\n\r]+", " ", x), result )
    return result



tdata = [tupify(jd) for jd in jdata]
tdata = [map(str, x) for x in tdata]

with open(outfile, "w") as fo:
    fo.write("\n".join(["\t".join(x) for x in tdata]))



# ...........

file0 = "/Users/chagerman/Projects/NewsClassifier/InputData/userLists/profiles.BAK.tsv"
file1 = "/Users/chagerman/Projects/NewsClassifier/InputData/userLists/all_profiles.tsv"

outfile = "/Users/chagerman/Projects/NewsClassifier/InputData/userLists/all_profiles_new.tsv"

lines0 = [x.strip().split("\t") for x in open(file0) if len(x.strip().split("\t")) > 1 ]
lines1 = [x.strip().split("\t") for x in open(file1) if len(x.strip().split("\t")) > 1 ]


d0 = {x[1]: x for x in lines0}
d1 = {x[1]: x for x in lines1}

lines = []
for k in d0:
    line = d0[k]
    if k in d1:
        line += d1[k]
    line = "\t".join(line)
    lines.append(line)

for k in d1:
    if not k in d0:
        line ="\t".join( d1[k])
        lines.append(line)

with open(outfile, "w") as fo:
    fo.write("\n".join(lines))


