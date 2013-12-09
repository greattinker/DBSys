#!/usr/bin/python
import sys
sys.path.append('./../.')
sys.path.append('./../python-layers/lib')
from flask import Flask,jsonify,request
from twitter import user, tweet, follow

app = Flask(__name__)
tweet = tweet()
user = user()
follow = follow()


@app.route("/tweets/<string:username>", methods = ["GET"])
def get_tweets(username):
	return jsonify( { username: tweet.getTweetsForUser(username, 0, 40)})
	
@app.route("/post_tweet", methods = ["POST"])
def post_tweet():
	if not request.json or not "username" in request.json:
		abort(400)
	tweet.addTweet(request.json["username"], None, request.json["body"])
	return 201
	
@app.route("/create_user", methods = ["POST"])
def create_user():
	user.addUser(request.json["username"],request.json["passwort"])
	
@app.route("/add_friend", methods = ["POST"])
def add_friend():
	follow.follows(request.json["friend"],request.json["username"])
	return 201
	
@app.route("/import_friends", methods = ["POST"])
def import_friends():
	for x in request.json["friends"]:
		follow.follows(x,request.json["username"])
	return "Hammer, Bohrer, Zieher, Guenther"
	
@app.route("/import_tweets", methods = ["POST"])
def import_tweets():
	for x in request.json["body"]:
		tweet.addTweet(request.json["username"], None, x)
	return "Der alte Walter ist ein ganz Kalter"
	
#@app.route("/add_user", methods = ["POST"])
#def import_tweets():
	#for x in request.json["body"]:
		#tweet.addTweet(request.json["username"], None, x)
	#return "Der alte Walter ist ein ganz Kalter"
	
if __name__ == "__main__":
	app.run(debug = True)
