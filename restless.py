#!/usr/bin/python

from flask import Flask, jsonify, request, abort
from twitter import user, tweet, follow

tweet = tweet()
user = user()
follow = follow()
app = Flask(__name__)


@app.route("/clear", methods = ["POST"])
def clear():
	tweet.cleanAll()
	return "", 200
	
@app.route("/tweets", methods = ["POST"])
def get_tweetspost():
	username = request.json["username"]
	return jsonify( { username: tweet.getTweetsForUser(str(username), 0, 40) }), 200

@app.route("/tweets/<string:username>", methods = ["GET"])
def get_tweets(username):
	return jsonify( { username: tweet.getTweetsForUser(str(username), 0, 40)}), 200
	
@app.route("/post_tweet", methods = ["POST"])
def post_tweet():
	if not request.json or not "username" in request.json:
		abort(400)
	tweet.addTweet(str(request.json["username"]), None, str(request.json["body"]))
	return "", 200
		
@app.route("/create_user", methods = ["POST"])
def create_user():
	user.addUser(request.json["username"], request.json["password"])
	return "", 200
	
@app.route("/add_friend", methods = ["POST"])
def add_friend():
	follow.follows(request.json["username"],request.json["friend"])
	return "", 200
	
@app.route("/import_friends", methods = ["POST"])
def import_friends():
	friends = request.json["friends"]
	username = request.json["username"]
	follow.import_follows(friends,username)
	return "", 200
	
@app.route("/import_tweets", methods = ["POST"])
def import_tweets():
	bodies = request.json["bodies"]
	timestamps = request.json["timestamps"]
	tweet.import_tweets(str(request.json["username"]), timestamps, bodies)
	return "", 200

@app.route("/get_friends", methods = ["POST"])
def get_friends():
	username = request.json["username"]
	return jsonify( { username: follow.getFollowing(username)}), 200
	
@app.route("/get_followers", methods = ["POST"])
def get_followers():
	username = request.json["username"]
	return jsonify( { username: follow.getFollowersOfUser(username)}),200
	
if __name__ == "__main__":
	app.run(debug = True)
	
