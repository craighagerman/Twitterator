
import tweepy



from twitterator.twitAuthClient import TwitAuthClient
from twitterator.twitterRest import TwitterRestClient



def get_single_user(client, usr):
	# check out profile on a single user
	result = client.get_single_user(usr)
	print(f"Name:            {result['name']}")
	print(f"ID:              {result['id']}")
	print(f"Location:        {result['location']}")
	print(f"Description:     {result['description']}")
	print(f"Statuses count:  {result['statuses_count']}")
	print(f"Friends count:   {result['friends_count']}")
	print(f"Followers count: {result['followers_count']}")
	print(f"Recent Status:	 {result['status']['text']}")


def search_historical(client, usr):
	# search historical tweets for given keywords
	result = client.search_historical(['BCSC'], 'en')
	# [x['text'] for x in result['statuses']]
	for status in result['statuses']:
		print(status['text'])

def demo_other_calls(client, usr):
	# get user timeline for a single user
	result = client.get_user_timeline(usr)
	print(f"Number of statuses on timeline: {len(result)}")
	# get lists for a single user
	result = client.get_lists(usr)
	print(f"Number of lists: {len(result)}")
	# get list of friends for a single user (to to 200?)
	result = client.get_friends(usr)
	print(f"Number of friends (initial): {len(result['users'])}")
	# get list of followers for a single user (to to 200?)
	result = client.get_followers(usr)
	print(f"Number of followers (initial): {len(result['users'])}")


########################################################################################################################
#  Main
########################################################################################################################


def main(cred_file, appname):
	AC = TwitAuthClient(cred_file)
	print(f'appname: {appname}')
	access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)
	client = TwitterRestClient(consumer_key, consumer_secret)

	# define a valid user to search on
	usr = 'rorycapern'

	# search_historical(client, usr)
	# demo_other_calls(client, usr)
	get_single_user(client, usr)


if __name__ == '__main__':
	cred_file = '/Users/chagerman/Projects/Twitterator/credentials/twitter_credentials.json'
	appname = "craighagerman"
	main(cred_file, appname)
