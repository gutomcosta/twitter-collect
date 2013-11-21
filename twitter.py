import sys
import tweepy
import json
from pymongo import MongoClient

consumer_key="VVAWlLLW7BBf68hcbQtQ"
consumer_secret="yn2kTROHx9v0OCgSB8AAjd8IWbVaYP1hmyqhiCt7Q"
access_key = "14197558-NSVdf0kt7pgWESQ1BtVNBgcYfbT2fIIgDhdPsts9R"
access_secret = "l9VITMfMCWTtTYstfsS9prpuA9ozy56OusUz93KzEMQfT" 



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

client = MongoClient()
# db = client.tweets_db
# tweets = db.tweets
db = client.tweets_phillipines_db
tweets = db.tweets

@classmethod
def parse(cls, api, raw):
	status = cls.first_parse(api, raw)
	setattr(status, 'json', json.dumps(raw))
	return status

tweepy.models.Status.first_parse = tweepy.models.Status.parse
tweepy.models.Status.parse = parse


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        message = "[{0}] - {1} - {2}".format(status.user, status.text.encode('utf8'), status.created_at)
        tweet = json.loads(status.json)
        tweets.insert(tweet)
        print message
        
    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

def get_stream():
  sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
  sapi.filter(track=['typhoon philippines'])