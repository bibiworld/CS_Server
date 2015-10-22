#!/usr/bin/python
#coding:utf-8
import BIBIUserODB
import Search
import goodSentence

class BIBIODB:
	def __init__(self, username):
		self.UserClass = BIBIUserODB.BIBIUserODB(username)
		
	def registerAccount(self, passwd, tishi = "密码"):
		return self.UserClass.registerAccount(passwd, tishi)
	
	def loginAccount(self, passwd):
		return self.UserClass.loginAccount(passwd)
		
	def commit(self):
		return self.UserClass.commit()
		
	def searchWord(self, word):
		return Search.searchWord(word, self.UserClass)
		
	def fuzzyQuery(self, word):
		return Search.fuzzyQuery(word, self.UserClass)
		
	def similarQuery(self, word):
		return Search.similarQuery(word, self.UserClass)
	
	def sentenceQuery(self):
		return goodSentence.sentenceQuery(self.UserClass)
