#!/usr/bin/python

import json
import application_only_auth
import tweepy

class AuthClient:
    
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file

    def create_aoa_client(self, app_name):
        client = self.aoa_client(app_name )
        return client

    def aoa_client(self, app_name):
        _, _, consumer_key, consumer_secret  = self.get_credentials(app_name, self.credentials_file)
        return application_only_auth.Client(consumer_key, consumer_secret)

    def create_tweepy_client(self, app_name):
        access_token, access_token_secret, consumer_key, consumer_secret = self.get_credentials(app_name)
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        return api, auth

    def get_credentials(self, app_name):
        keys = json.load(open(self.credentials_file))
        access_token = keys[app_name]['access_token_key']
        access_token_secret = keys[app_name]['access_token_secret']
        consumer_key = keys[app_name]['consumer_key']
        consumer_secret = keys[app_name]['consumer_secret']
        return access_token, access_token_secret, consumer_key, consumer_secret
