#!/usr/bin/python
#coding:utf-8

import conn
import re
import similar

class BIBIUserODB:
	def __init__(self, username):
		self.userName = username

	def __del__(self):
		conn.close()
		


	def registerAccount(self, passwd, tishi = "忘记密码"):
		checkSql = "select * from bibi_admin \
		where name = '%s'" % (self.userName)
		conn.cursor.execute(checkSql)
		checkIsOk = conn.cursor.fetchone()
		print checkIsOk
		if (checkIsOk == None):
			regSql = "insert into bibi_admin (name, pwd, tishi) \
			values('%s', '%s', '%s')" % (self.userName, passwd, tishi)
			#print regSql
			try:
				conn.cursor.execute(regSql)
			except:
				print "Error:regAcconut"
			return True
		else:
			return False
		


	def loginAccount(self, passwd):
		loginSql = """select * from bibi_admin
		where name = '%s'
		""" % (self.userName)
		conn.cursor.execute(loginSql)
		infoList = conn.cursor.fetchone()
		if (infoList == None):
			return "Error:Name is wrong"
		elif(infoList[2] == passwd):
			return "GoodJob"
		else:
			return "Error:passwd is wrong"
			

		
	
		
	
	def similarQuery(self, word):
		return similarDict[word]
		'''
		loseOne = similar.similarDict[word][0]
		swapAbut = similar.similarDict[word][1]
		length = len(word)
		rewords = []
		
		for i in range(length):
			if ((loseOne >> i) & 1) == 1:
				rewords.append(word[0 : i] + word[i + 1 : length])
		for i in range(1, length):
			if ((swapAbut >> i) & 1) == 1:
				rewords.append(word[0 : i - 1] + word[i] + word[i - 1] + word[i + 1 : length])
		return rewords
		'''
	
	
	def commit(self):
		conn.commit()
	
	
	
