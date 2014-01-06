#!/usr/bin/python

from flask import Flask, jsonify, request, abort
from twitter import user, tweet, follow

tweet = tweet()
user = user()
follow = follow()
app = Flask(__name__)


@app.route("/tweets", methods = ["POST"])
def get_tweetspost():
	username = request.json["username"]
	return jsonify( { username: tweet.getTweetsForUser(str(username), 0, 40)})

@app.route("/tweets/<string:username>", methods = ["GET"])
def get_tweets(username):
	return jsonify( { username: tweet.getTweetsForUser(str(username), 0, 40)})
	
@app.route("/post_tweet", methods = ["POST"])
def post_tweet():
	if not request.json or not "username" in request.json:
		abort(400)
	tweet.addTweet(str(request.json["username"]), None, str(request.json["body"]))
	return "", 201
	
@app.route("/create_user", methods = ["POST"])
def create_user():
	user.addUser(request.json["username"], request.json["password"])
	return "", 201
	
@app.route("/add_friend", methods = ["POST"])
def add_friend():
	follow.follows(request.json["friend"],request.json["username"])
	return 201
	
@app.route("/import_friends", methods = ["POST"])
def import_friends():
	for x in request.json["friends"]:
		follow.follows(x,request.json["username"])
	return "Hammer, Bohrer, Zieher, Guenther, Lehner", 201
	
@app.route("/import_tweets", methods = ["POST"])
def import_tweets():
	bodies = request.json["bodies"]
	timestamps = request.json["timestamps"]
	for x,t in zip(bodies, timestamps):
		tweet.addTweet(str(request.json["username"]), int(t), str(x))
	return "", 201
	
#@app.route("/add_user", methods = ["POST"])
#def import_user():
#	for x in request.json["body"]:
#		tweet.addTweet(request.json["username"], None, x)
#	return "Der alte Walter ist ein ganz Kalter"
	
if __name__ == "__main__":
	app.run(debug = True)
	
