#! /usr/bin/python

from twitter import user, tweet, follow 



user = user()
user.cleanAll()
#tweet = tweet(twitter)
#follow = follow(twitter)

user.addUser("ich2")
user.addUser("du")
#user.addUser(db, "er")

##follow.follows(db, "du", "ich")
##follow.follows(db, "er", "ich")
users = user.getAllUsers()
for u in users :
	print u
	
##tweet.addTweet(db, "ich", None, "ein neuer tweet")
#tweets = tweet.getTweetsForUser(db, "ich")
#for t in tweets :
#	print t

#followers = follow.getFollowersOfUser(db, "ich")
#for f in followers :
#	print f
