#! /usr/bin/python

from twitter import user, tweet, follow 
import time
from datetime import datetime


user = user()
user.cleanAll()
tweet = tweet()
follow = follow()

user.addUser("ich", "pass1")
user.addUser("du", "pass2")
user.addUser("er", "pass3")

follow.follows("du", "ich")
follow.follows("er", "ich")
users = user.getAllUsers()
for u in users :
	print u

ti = time.time()*1000
print "%d" % ti
tweet.addTweet("ich", None, "ein neuer tweet")
print "tweets von ich"
tweets = tweet.getTweetsForUser("ich", 0, 40)
for t in tweets :
	print t
print "followers von ich"
followers = follow.getFollowersOfUser("ich")
for f in followers :
	print f
