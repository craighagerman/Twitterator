
import tweepy



from twitterator.twitAuthClient import TwitAuthClient
from twitterator.twitterRest import TwitterRestClient


def main(cred_file, appname):
	AC = TwitAuthClient(cred_file)
	print(appname)
	access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)


	client = TwitterRestClient(consumer_key, consumer_secret)
	# check out profile on a single user
	result = client.get_single_user('rorycapern')
	# get user timeline for a single user
	result = client.get_user_timeline('rorycapern')
	# get lists for a single user
	result = client.get_lists('rorycapern')
	# get list of friends for a single user (to to 200?)
	result = client.get_friends('rorycapern')
	# get list of followers for a single user (to to 200?)
	result = client.get_followers('rorycapern')
	# search historical tweets for given keywords
	result = client.search_historical(['BCSC'], 'en')
	[x['text'] for x in result['statuses']]





if __name__ == '__main__':
	cred_file = '/Users/chagerman/Projects/Twitterator/credentials/twitter_credentials.json'
	appname = "craighagerman"
	main(cred_file, appname)
