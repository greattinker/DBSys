#!/usr/bin/python

import fdb
import fdb.tuple
import time
import sys
import struct
sys.path.append('./python-layers/lib')
from subspace import Subspace
from directory import directory


fdb.api_version(100)

db = fdb.open()
twitter = directory.create_or_open(db, ('twitter',))
#class dbHandler(object):
#	
#	def __init__ (self) :
#		self._host = '127.0.0.1'
#		self._port = ''
#		self._username =''
#		self._password = ''
#		self._cluster = ''
#		self._db = 'twitter'
#		self._event_model ='None'
#		self.connect()
#		
#	def connect(self) :
#		self.db = fdb.open()

#	def getfdb(self) : 
#		return self.db
	

class user(object):
	def __init__ (self, directory) :
		super(user, self).__init__()
		self.__user_space = directory['user']
	
	@fdb.transactional
	def addUser(self, tr, username) :
		tr[self.__user_space.pack((username,))] = ''
		
	@fdb.transactional
	def getUser(self, tr, username) :
		return tr[self.__user_space.pack((username,))]
	
	@fdb.transactional
	def getAllUsers(self, tr) :
		return [fdb.tuple.unpack(k)[2] for k,v in tr[self.__user_space.range()]]


class tweet(object):
	def __init__ (self, directory) :
#		super(tweet, self).__init__()
		self.__tweet_space = directory['tweet']
	
	@fdb.transactional
	def addTweet(self, tr, username, created, body) :
		if created == None :
			created = time.time()
		tr[self.__tweet_space.pack((username,created))] = str(body)
		
	@fdb.transactional
	def getTweet(self, tr, username, created) :
		return tr[self.__tweet_space.pack((username,created))]
		
	@fdb.transactional
	def getTweetsForUser(self, tr, username) :
		return tr[fdb.tuple.range((username,))]

user = user(twitter)

user.addUser(db, "ich")
user.addUser(db, "du")
user.addUser(db, "er")
users = user.getAllUsers(db)
for user in users :
	print user
