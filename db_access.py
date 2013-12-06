#!/usr/bin/python

import fdb
import fdb.tuple
import sys
import struct
sys.path.append('./python-layers/lib')


class dbHandler(object):
	
	def __init__ (self) :
		self._host = '127.0.0.1'
		self._port = ''
		self._username =''
		self._password = ''
		self._cluster = ''
		self._db = 'twitter'
		self._event_model ='None'
		self.connect()
		return self.__db
		
	def connect(self) :
		fdb.api_version(100)
		self.__db = fdb.open(self._cluster, self._db, self._event_model)
	

class user(object):
	def __init__ (self) :
		print("test")

dbh = dbHandler();
