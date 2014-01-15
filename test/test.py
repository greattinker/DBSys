#! /usr/bin/python

from twitter2 import user, tweet, follow 
import time
from datetime import datetime



tweet = tweet()
follow = follow()
user = user()

users = user.getAllUsers()
for u in users :
	print u
	
print "followers von user_1"
followers = follow.getFollowersOfUser("user_1")
for f in followers :
	print f

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
