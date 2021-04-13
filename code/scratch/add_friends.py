
import tweepy

# from app.twitterator.authClient import AuthClient
from authClient import AuthClient



def main(cred_file, appname):
	AC = AuthClient(cred_file)
	print(appname)
	access_token, access_token_secret, consumer_key, consumer_secret = AC.get_credentials(appname)

	snlist = [x.strip().strip("@") for x in open("nips_twitter.txt")]
	for item in snlist:
		print(item)


# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# public_tweets = api.home_timeline()



# api.create_friendship(screen_name)



if __name__ == '__main__':
	cred_file = "/Users/chagerman/Projects/_ARCHIVE/Twitterator/credentials.json"
	appname = "craighagerman"
	main(cred_file, appname)
