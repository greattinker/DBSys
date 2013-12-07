#! /usr/bin/python

from twitter import user, tweet, follow 



user = user()
user.cleanAll()
tweet = tweet()
follow = follow()

user.addUser("ich")
user.addUser("du")
user.addUser("er")

follow.follows("du", "ich")
follow.follows("er", "ich")
users = user.getAllUsers()
for u in users :
	print u
	
tweet.addTweet("ich", None, "ein neuer tweet")
print "tweets von ich"
tweets = tweet.getTweetsForUser("ich")
for t in tweets :
	print t
print "followers von ich"
followers = follow.getFollowersOfUser("ich")
for f in followers :
	print f
