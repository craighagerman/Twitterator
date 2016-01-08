
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
def json2tsv(data):
                # data = json.loads(data)
                created_at = data['created_at']
                user_id_str = data['user']['id_str']
                screen_name = data['user']['screen_name']
                description = data['user']['description']
                if description:
                    description = re.sub(nlpattern, " ", description)
                else:
                    description = "None"
                followers_count = data['user']['followers_count']
                friends_count = data['user']['friends_count']
                statuses_count = data['user']['statuses_count']
                id_str = data['id_str']
                text = re.sub(nlpattern, " ", data['text'])

                lang = data['lang']
                source = re.sub(nlpattern, " ", data['source'])

                if 'user_mentions' in data['entities']:
                    user_mentions = ",".join([x['screen_name'] for x in  data['entities']['user_mentions']])
                else:
                    user_mentions = "None"

                if 'media' in data['entities']:
                    media = [",".join([x['type'], x['media_url'] ]) for x in data['entities']['media']]
                else:
                    media = "None"

                if 'urls' in data['entities'] and data['entities']['urls']:
                    urls = data['entities']['urls']
                    expanded_url = ",".join([x['expanded_url'] for x in urls])
                else:
                    expanded_url = ""

                if 'hashtags' in data['entities'] and data['entities']['hashtags']:
                    htags = data['entities']['hashtags']
                    hashtags = ",".join([x['text'] for x in htags])
                else:
                    hashtags = ""

                coordinates = data['coordinates']
                if coordinates:
                    lat = coordinates['coordinates'][1]
                    lon = coordinates['coordinates'][0]
                else:
                    lat = lon = "None"
                place = data['place']
                if place:
                    country = re.sub(nlpattern, " ", place['country'])
                    place_full_name = re.sub(nlpattern, " ", place['full_name'])
                    place_type = re.sub(nlpattern, " ", place['place_type'])
                else:
                    country = place_full_name = place_type = "None"
                

                if 'retweeted_status' in data:
                    rt_retweet_count = data['retweeted_status']['retweet_count']
                    rt_favorite_count = data['retweeted_status']['favorite_count']
                else:
                    rt_retweet_count = rt_favorite_count = "None"

                favorited = str(data['favorited'])
                favorite_count = str(data['favorite_count'])
                retweeted = str(data['retweeted'])
                retweet_count = str(data['retweet_count'])
                in_reply_to_screen_name = data['in_reply_to_screen_name']
                in_reply_to_status_id = data['in_reply_to_status_id']

                user_created_at = data['user']['created_at']
                geo_enabled = str(data['user']['geo_enabled'])
                listed_count = str(data['user']['listed_count'])
                
                if 'location' in data['user'] and data['user']['location']:
                    location = re.sub(nlpattern, " ", data['user']['location'])
                else:
                    location = ""

                if 'profile_banner_url' in data['user'] and data['user']['profile_banner_url']:
                    profile_banner_url = data['user']['profile_banner_url']
                else:
                    profile_banner_url = ""

                user_time_zone = data['user']['time_zone']
                user_url = data['user']['url']
                verified = data['user']['verified']
                user_name = data['user']['name']

                output = list((map(str, [  id_str,
                                                created_at,
                                                screen_name,
                                                place_full_name,
                                                lat,
                                                lon,
                                                text,
                                                lang,
                                                source,
                                                hashtags,
                                                favorited,
                                                favorite_count,
                                                retweeted,
                                                retweet_count,
                                                rt_favorite_count,
                                                rt_retweet_count,
                                                expanded_url,
                                                country,
                                                place_type,
                                                user_mentions,
                                                in_reply_to_screen_name,
                                                in_reply_to_status_id,
                                                media,
                                                user_id_str,
                                                statuses_count,
                                                followers_count,
                                                friends_count,
                                                description,
                                                user_created_at,
                                                geo_enabled,
                                                listed_count,
                                                location,
                                                profile_banner_url,
                                                user_time_zone,
                                                user_url,
                                                verified,
                                                user_name
                                                ])))
                output = [null2None(x) for x in output]                 # make sure all "" are converted to "None"
                output = [re.sub(nlpattern, " ", x) for x in output]    # make sure all tabs and newlines are stripped out
                tsvline = "\t".join(output)
                return tsvline



def convert(infile, outfile):
    lines = (line.strip() for line in open(infile) if not line.strip() == "")
    with open(outfile, "w") as fo:
        for line in lines:
            try:
                s = re.sub(nlpattern, " ", line)
                jdata = json.loads(s)
                tdata = json2tsv(jdata)
                fo.write(tdata + "\n")
            except ValueError:
                print("ValueError")








def processDir(indir, outdir):
    jfiles = [f for f in os.listdir(indir) if f.endswith(".json")]
    jfiles.sort()
    for jf in jfiles:
        infile = os.path.join(indir, jf)
        outfile = os.path.join(outdir, jf.replace(".json", ".tsv"))
        print("processing {}".format(infile))
        convert(infile, outfile)




if __name__ == '__main__':
    indir = sys.argv[1]
    for root, dirs, files in os.walk(indir):
        paths = [os.path.join(root, f) for f in files if f.endswith(".json")]
        ## n.b. paths is a list of paths to .json files
        # paths = [os.path.join(indir, f) for f in os.listdir(indir) if f.endswith(".json")]
        for path in paths:
            outpath = os.path.splitext(path)[0] + ".tsv"
            with open(outpath, "w") as fo:
                lines = [line.strip() for line in open(path)]
                for line in lines:
                    print(line[0:100])
                    try:
                        d = json.loads(line)
                        tsvline = json2tsv(d)
                        fo.write(tsvline + "\n")
                    except: ValueError
            print("\n====================================================\n")




'''
    import gzip
    # GZIP compress existing file
    def gzip_it(self, inpath):
        outpath = inpath + ".gz"
        with open(inpath, 'rb') as f_in:
            with gzip.open(outpath, 'wb') as f_out:
                f_out.writelines(f_in)
        if self.delete_uncompressed:
            self._deleteFile(inpath)


'''





# for d in dirs:
#     outfile = os.path.join(d, os.path.split(d)[1] + ".tsv")
#     with open(outfile, "w") as fo:
#         jfiles = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(".json")]
#         for jfile in jfiles:
#             print("processing {}".format(jfile))
#             lines = [x.strip() for x in open(jfile)]
#             for line in lines:
#                 try:
#                     data = json.loads(line)
#                     tsvline = json2tsv(data)
#                     fo.write(tsvline + "\n")
#                 except:
#                     continue
















