



import json
import os
import sys
import re

nlpattern = re.compile(r"[\n|\t|\r]+")

def null2None(text):
    if text == "":
        return "None"
    else:
        return text

'''
Receive: json Twitter object
Return : TSV-formatted line containing 37 fields
'''

def json2tsv(df:  org.apache.spark.sql.DataFrame):
    val df = sqlContext.sql("SELECT id, created_at, user.screen_name, place.full_name, coordinates.coordinates[1], coordinates.coordinates[0], text, lang, source, entities.hashtags, favorited, favorite_count, retweeted, retweet_count, retweeted_status.favorite_count, retweeted_status.retweet_count, entities.urls.expanded_url, place.country, place.place_type, entities.user_mentions, in_reply_to_screen_name, in_reply_to_status_id, entities.media, user.id_str, user.statuses_count, user.followers_count, user.friends_count, user.description, user.created_at, user.geo_enabled, user.listed_count, user.location, user.profile_banner_url, user.time_zone, user.url, user.verified, user.name FROM data")


    val rdd = df.map(Array(_)).map(_.map(_.toString))




                
                


                if 'user_mentions' in data['entities']:
                    user_mentions = ",".join([x['screen_name'] for x in  data['entities']['user_mentions']])
                else:
                    user_mentions = "None"

                if 'media' in data['entities']:
                    media = [",".join([x['type'], x['media_url'] ]) for x in data['entities']['media']]
                else:
                    media = "None"

 





                if 'hashtags' in data['entities'] and data['entities']['hashtags']:
                    htags = data['entities']['hashtags']
                    hashtags = ",".join([x['text'] for x in htags])
                else:
                    hashtags = ""

  
                place = data['place']
                if place:
                    country = re.sub(nlpattern, " ", place['country'])
                    place_full_name = re.sub(nlpattern, " ", place['full_name'])
                    place_type = re.sub(nlpattern, " ", place['place_type'])
                else:
                    country = place_full_name = place_type = "None"
                





                
                if 'location' in data['user'] and data['
                    location = re.sub(nlpattern, " ", data['user']['location'])
                else:
                    location = ""

                if 'profile_banner_url' in data['user'] and data['
                    profile_banner_url = data['user']['profile_banner_url']
                else:
                    profile_banner_url = ""

                
                
                







                output = [null2None(x) for x in output]                 # make sure all "" are converted to "None"
                output = [re.sub(nlpattern, " ", x) for x in output]    # make sure all tabs and newlines are stripped out
                tsvline = "\t".join(output)
                return tsvline



def convert(infile, outfile):
    lines = (line.strip() for line in open(infile) if not line.strip() == "")
    with open(outfile, "w") as fo:
        for line in lines:
            s = re.sub(nlpattern, " ", line)
            jdata = json.loads(s)
            tdata = json2tsv(jdata)
            fo.write(tdata + "\n")

def processDir(indir, outdir):
    jfiles = [f for f in os.listdir(indir) if f.endswith(".json")]
    jfiles.sort()
    for jf in jfiles:
        infile = os.path.join(indir, jf)
        outfile = os.path.join(outdir, jf.replace(".json", ".tsv"))
        print("processing {}".format(infile))
        convert(infile, outfile)















