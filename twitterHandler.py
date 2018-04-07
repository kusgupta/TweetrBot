"""

This script handles the tweeting.


"""
import time
import tweepy
import TrumpModel
import random
import apiKeysIgnoreinGit

CONSUMER_KEY = apiKeysIgnoreinGit.returnKeys(0)
CONSUMER_SECRET = apiKeysIgnoreinGit.returnKeys(1)
ACCESS_KEY = apiKeysIgnoreinGit.returnKeys(2)
ACCESS_SECRET = apiKeysIgnoreinGit.returnKeys(3)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

rw = TrumpModel.MarkovChain(3, TrumpModel.Tokenization.word)
with open("Trump.txt") as f:
    string = f.read()

rw.trumpTrainer(string)
g = rw.generate()

tweet = ""
while True:
    sleepTime = random.randint(4000, 50000)
    print(sleepTime)
    time.sleep(sleepTime)
    num = random.randint(2, 8)
    tweet = str(rw.generateSentences(num))
    while (len(tweet)) > 280:
        num = random.randint(2, 8)
        tweet = str(rw.generateSentences(num))
    tweet = tweet[:1].upper() + tweet[1:]
    print(tweet)
    api.update_status(status=tweet)
