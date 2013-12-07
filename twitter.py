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


#db = fdb.open()
#twitter = directory.create_or_open(db, ('twitter',))	

class twitter (object) :
	def __init__(self, subspace) :
		fdb.api_version(100)
		self._db = fdb.open()
		self._directory = directory.create_or_open(self._db, ('twitter',))
		if subspace != None :
			self._subspace = self._directory[subspace]
			
	def cleanAll(self) :
		self.cleanDB(self._db)
		
	@fdb.transactional
	def cleanDB(self, tr) :
		tr.clear_range_startswith(self._directory)

class user (twitter):
	def __init__ (self) :
		super(user, self).__init__('user')
		
	def addUser(self, username) :
		self.addUserDB(self._db, username)
	
	@fdb.transactional
	def addUserDB(self, tr, username) :
		tr[self._subspace.pack((username,))] = ''
		
	def getUser(self, username) :
		return self.getUserDB(self._db, username)
	
	@fdb.transactional
	def getUserDB(self, tr, username) :
		return tr[self._subspace.pack((username,))]
	
	def getAllUsers(self) :
		return self.getAllUsersDB(self._db)
	
	@fdb.transactional
	def getAllUsersDB(self, tr) :
		return [fdb.tuple.unpack(k)[2] for k,v in tr[self._subspace.range()]]


class tweet(twitter):
	def __init__ (self) :
		super(tweet, self).__init__('tweet')
	
	def addTweetDB(self, username, created, body) :
		self.addTweetDB(self._db, username, created, body)
	
	@fdb.transactional
	def addTweetDB(self, tr, username, created, body) :
		if created == None :
			created = time.time() 
		tr[self._subspace.pack((username,int(created)))] = str(body)
		
	def getTweet(self, username, created) :
		return self.getTweetDB(self._db, username, created)
		
	@fdb.transactional
	def getTweetDB(self, tr, username, created) :
		return tr[self._subspace.pack((username, int(created)))]
		
	def getTweetsForUser(self, username) :
		return self.getTweetsForUserDB(self._db, username)
		
	@fdb.transactional
	def getTweetsForUserDB(self, tr, username) :
		return [v for k,v in tr[self._subspace.range((username,))]]




class follow(twitter) :
	def __init__(self) :
		super(follow, self).__init__(None)
		self._follow_space = self._directory['follow']
		self._follow_by_space = self._directory['follow_by']
	
	def follows(self, user, follows) :
		self.followsDB(self._db, user, follows)
	
	@fdb.transactional
	def followsDB(self, tr, user, follows) :
		tr[self.__follow_space.pack((user,follows))] = ''
		tr[self.__follow_by_space.pack((follows,user))] = ''
	
	def resign(self, user, follows) :
		self.resignDB(self._db, user, follows)
	
	@fdb.transactional
	def resignDB(self, tr, user, follows) :
		del tr[self.__follow_space.pack((user,follows))] 
		del tr[self.__follow_by_space.pack((follows,user))] 
		
	def getFollowersForUser(self, user) :
		return self.getFollowersOfUserDB(self._db, user)
		
	@fdb.transactional
	def getFollowersOfUserDB(self, tr, user) :
		return [fdb.tuple.unpack(k)[3] for k,v in tr[self.__follow_by_space.range((user,))]]
	
	def getFollowing(self, user) :
		return self.getFollowingDB(self._db, user)
	
	@fdb.transactional
	def getFollowingDB(self, tr, user) :
		return [fdb.tuple.unpack(k)[3] for k,v in tr[self.__follow_space.range((user,))]]


