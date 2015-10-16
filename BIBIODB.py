#!/usr/bin/python
#coding:utf-8
import BIBIUserODB
import Search

class BIBIODB:
	def __init__(self, username):
		self.UserClass = BIBIUserODB.BIBIUserODB(username)
		
	def __del__(self):
		UserClass.__del__()
		
	def registerAccount(self, passwd, tishi = "Íü¼ÇÃÜÂë"):
		return UserClass.registerAccount(passwd, tishi)
	
	def loginAccount(self, passwd):
		return UserClass.loginAccount(passwd)
		
	def commit(self):
		return UserClass.commit()
		
	def searchWord(self, word):
		return Search.searchWord(word, self.UserClass)
		
	def fuzzyQuery(self, word):
		return Search.fuzzyQuery(word, self.UserClass)
		
	def similarQuery(self, word):
		return Search.similarQuery(word, self.UserClass)
		
