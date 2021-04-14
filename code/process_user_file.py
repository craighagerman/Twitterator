import os
from dataclasses import dataclass

import pandas as pd
import re
from twitterator.twitAuthClient import TwitAuthClient
from twitterator.twitterRest import TwitterRestClient


@dataclass(frozen=True)
class UserProfile:
    name: str
    id: str
    screen_name: str
    location: str
    lang: str
    created_at: str
    verified: str
    description: str
    statuses_count: int
    friends_count: int
    followers_count: int


def profile_single_user(client, usr):
    # check out profile on a single user
    try:
        result = client.get_single_user(usr)
        profile = UserProfile(result['name'],
                              result['id_str'],
                              result['screen_name'],
                              result['location'],
                              result['lang'],
                              result['created_at'],
                              result['verified'],
                              re.sub('[\n\t]', ' ', result['description']),
                              result['statuses_count'],
                              result['friends_count'],
                              result['followers_count'])
    except:
        print(f'Count not get profile for user {usr}')
        profile = None
    return profile


########################################################################################################################
#  Main
########################################################################################################################


def main(cred_file, appname, user_file, out_path):
    AC = TwitAuthClient(cred_file)
    print(f'appname: {appname}')
    access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
    client = TwitterRestClient(consumer_key, consumer_secret)

    df = pd.read_csv(user_file, '\t')
    screen_names = [x.replace('@', '') for x in df['Handle'].tolist()]
    profiles = [profile_single_user(client, x) for x in screen_names]
    profiles = [x for x in profiles if x]

    df2 = pd.DataFrame(profiles)
    if len({'Position', 'Company'}.intersection(set(df.columns))) == 2:
        df2 = df2.join(df[['Position', 'Company']])

    df2.to_csv(out_path, sep='\t', index=False)


if __name__ == '__main__':
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

    appname = "craighagerman"
    # user_file = os.path.join(screen_name_dir, 'canadian_news.tsv')
    user_file = os.path.join(screen_name_dir, 'canadian_execs.tsv')

    out_path = user_file.replace('.tsv', '2.tsv')
    main(credentials_file, appname, user_file, out_path)
