#!/usr/bin/python
#coding:utf-8
import BIBIUserODB
import Search

class BIBIODB:
	def __init__(self, username):
		UserClass = BIBIUserODB.BIBIUserODB(username)
		
	def __del__(self):
		UserClass.__del__()
		
	def registerAccount(self, passwd, tishi = "Íü¼ÇÃÜÂë"):
		UserClass.registerAccount(passwd, tishi)
	
	def loginAccount(self, passwd):
		UserClass.loginAccount(passwd)
		
	def commit(self):
		UserClass.commit()
		
	def searchWord(word):
		Search.searchWord(word, UserClass)
		
	def fuzzyQuery(word):
		Search.fuzzyQuery(word, UserClass)
		
	def similarQuery(word):
		Search.similarQuery(word, UserClass)
		
