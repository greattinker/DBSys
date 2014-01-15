#! /usr/bin/python

from twitter import user, tweet, follow 
import time
from datetime import datetime



user = user()
users = user.getAllUsers()
for u in users :
	print u
#tweet = tweet()
#follow = follow()

#user.addUser("ich", "pass1")
#user.addUser("du", "pass2")
#user.addUser("er", "pass3")

#follow.follows("du", "ich")
#follow.follows("er", "ich")
#users = user.getAllUsers()
#for u in users :
#	print u

#ti = time.time()*1000
#print "%d" % ti
#tweet.addTweet("ich", None, "ein neuer tweet")
#print "tweets von hagrid"
#tweets = tweet.getTweetsForUser("Hagrid", 0, 40)
#for t in tweets :
#	print t
#print "followers von ich"
#followers = follow.getFollowersOfUser("ich")
#for f in followers :
#	print f
