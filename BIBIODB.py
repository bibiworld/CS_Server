#!/usr/bin/python
#coding:utf-8

import MySQLdb

serverIP = "59.66.131.31"



class BIBIUserODB:
	def __init__(self, username):
		global serverIP
		self.bibi = MySQLdb.connect(host = serverIP, user = "root", passwd = "unityispower",db = "bibidata", charset = "utf8");
		self.cursor= self.bibi.cursor()
		self.userName = username
	def __del__(self):
		self.cursor.close()
		self.bibi.close()
		
	def registerAccount(self, passwd, tishi = "忘记密码"):
		checkSql = "select * from bibi_admin \
		where name = '%s'" % (self.userName)
		self.cursor.execute(checkSql)
		checkIsOk = self.cursor.fetchone()
		print checkIsOk
		if (checkIsOk == None):
			regSql = "insert into bibi_admin (name, pwd, tishi) \
			values('%s', '%s', '%s')" % (self.userName, passwd, tishi)
			#print regSql
			try:
				self.cursor.execute(regSql)
			except:
				print "Error:regAcconut"
			return True
		else:
			return False
		
	def loginAccount(self, passwd):
		loginSql = """select * from bibi_admin
		where name = '%s'
		""" % (self.userName)
		self.cursor.execute(loginSql)
		infoList = self.cursor.fetchone()
		if (infoList == None):
			return "Error:Name is wrong"
		elif(infoList[2] == passwd):
			return "GoodJob"
		else:
			return "Error:passwd is wrong"
			
	def searchWord(self, word):
		searchSql = """select * from bibi_word
		where spell = '%s'
		""" % (word)
		self.cursor.execute(searchSql)
		infoList = self.cursor.fetchone()
		if (infoList == None):
			return ["Error:no word"]
		else:
			return infoList
		
	def commit(self):
		self.bibi.commit()
		
	
	
	
