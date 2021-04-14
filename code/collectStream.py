# builtin imports
import http
from dataclasses import dataclass
from enum import Enum
from http.client import IncompleteRead
from typing import List

import urllib3
import yaml
from prettytable import PrettyTable
import pandas as pd
from twitterator.twitAuthClient import TwitAuthClient
from twitterator.twitterStream import *


class StreamKind(Enum):
    RANDOM = 1
    USERLIST = 2
    KEYWORD = 3
    GEO = 4
    MYFRIENDS = 5


@dataclass(frozen=True)
class CollectorConfig:
    streamkind: StreamKind
    appname: str
    langs: List
    file_prefix: str
    filter_list: List
    credentials_file: str
    email_credentials_file: str
    out_dir: str


class Collector:
    def __init__(self, config: CollectorConfig):
        self.streamkind = config.streamkind
        self.appname = config.appname
        self.langs = config.langs
        self.file_prefix = config.file_prefix
        self.filter_list = config.filter_list
        self.credentials_file = config.credentials_file
        self.email_credentials_file = config.email_credentials_file
        self.out_dir = config.out_dir
        print('initializing Twitter Auth Client...')
        self.api, self.auth = self._get_client()


    def init_msg(self):
        t = PrettyTable(["Variable", "Details"])
        t.align["Variable"] = "l"  # Left align
        t.align["Details"] = "l"  # Left align
        t.add_row(["Twitter Application name", self.appname])
        t.add_row(["Stream Kind", self.streamkind.name])
        t.add_row(["File Prefix", self.file_prefix])
        t.add_row(["Credentials File:", self.credentials_file])
        t.add_row(["Output Data Directory", self.out_dir])
        print(t)
        print("\n")


    def _get_client(self):
        AC = TwitAuthClient(self.credentials_file)
        return AC.create_tweepy_client(self.appname)

    def run_collector(self):

        while True:
            try:
                st = Streamer(self.api, self.auth, self.out_dir, self.file_prefix, self.email_credentials_file)
                if self.streamkind == StreamKind.RANDOM :
                    print("Filtering for keyword terms...")
                    # st.streamFilter(track_terms, langs)
                    st.streamRandom(self.langs)
                elif self.streamkind == StreamKind.KEYWORD :
                    print("Filtering for keyword terms...")
                    # st.streamFilter(track_terms, langs)
                    st.streamFilter(self.filter_list, self.langs)
                elif self.streamkind == StreamKind.GEO:
                    print("Filtering for geo lat/long bounds...")
                    # canada_geo_bounds = [-141.0, 41.7, -52.6, 83.1]
                    # st.streamLocation(canada_geo_bounds)
                    st.streamLocation(self.filter_list)
                elif self.streamkind == StreamKind.USERLIST:
                    print("Filtering for list of users...")
                    st.streamUserList(self.filter_list)
                elif self.streamkind == StreamKind.MYFRIENDS:
                    print("Filtering for my friends...")
                    st.streamFriends()
                else:
                    print("Incorrect stream kind. Must be one of 'filter', 'random' or 'userlist'.")
                    exit(0)
            except http.client.IncompleteRead:
                continue
            except urllib3.exceptions.ReadTimeoutError:
                continue
            except (KeyboardInterrupt, SystemExit):
                st.disconnect()
                print("*    KeyboardInterrupt or SystemExit caught  ")
                break
            except:
                continue


########################################################################################################################
########################################################################################################################

def get_filter_list(streamkind, config_dict, base_data_dir):
    if streamkind == StreamKind.RANDOM:
        return []
    else:
        data_dir = config_dict['data_dir']
        filter_file = config_dict['filter_file']
        file_path = os.path.join(base_data_dir, data_dir, filter_file)
        df = pd.read_csv(file_path, sep='\t')
        if 'Handle' in df:
            df['filter_list'] = df['Handle']
        return [x.replace('@', '') for x in df['filter_list'].tolist()]


def main(config_dict):
    # path to this python project
    project_dir = os.path.dirname(os.path.dirname(__file__))
    # define path to credentials directory
    credentials_dir = os.path.join(project_dir, 'credentials')
    # define path to Twitter credentials file
    credentials_file = os.path.join(credentials_dir, 'twitter_credentials.json')
    email_credentials_file = os.path.join(credentials_dir, 'email_credentials.json')
    # define path to data directory
    data_dir = os.path.join(project_dir, 'data')
    # define path to screen_name directory
    screen_name_dir = os.path.join(data_dir, '01_screen_names')
    # define path to keyword filter directory
    keyword_filter_dir = os.path.join(data_dir, '02_keyword_filter')
    # define path to base output directory for storing collected tweets
    base_out_dir = os.path.join(data_dir, '03_stream_data')

    # define path to specific output directory depending on prefix
    out_dir = os.path.join(base_out_dir, config_dict['file_prefix'])

    streamkind = StreamKind[config_dict['streamkind'].upper()]
    appname = config_dict['appname']
    langs = config_dict['langs']
    file_prefix = config_dict['file_prefix']

    # filter_list = get_filter_list(streamkind, config_dict, data_dir)

    filter_list = ['10495312', '10495312']

    print('filter_list:')
    for f in filter_list:
        print(f'\t{f}')

    collect_config = CollectorConfig(streamkind, appname, langs, file_prefix, filter_list, credentials_file, email_credentials_file, out_dir)

    col = Collector(collect_config)
    col.init_msg()
    col.run_collector()


if __name__ == '__main__':
    # path to this python project
    project_dir = os.path.dirname(os.path.dirname(__file__))
    # define path to config directory
    config_dir = os.path.join(project_dir, 'config')
    # define which yaml config file to use
    # yaml_file = os.path.join(config_dir, 'random_firehose.yaml')
    yaml_file = os.path.join(config_dir, 'user_filter_can_execs.yaml')
    # yaml_file = os.path.join(config_dir, 'keyword_filter_covid.yaml')

    with open(yaml_file) as f:
        config_dict = yaml.safe_load(f)

    main(config_dict)






'''

DESIRED ARGS:
    python3 collectStream.py <streamkind> <filename> <appname>



OLD ARGS:
python3 NewsOrgTweets.py aws userlist
or
python3 NewsOrgTweets.py aws userlist_newsorg

'''
