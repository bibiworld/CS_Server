#!/usr/bin/python
#coding:utf-8

import MySQLdb

serverIP = "localhost"


bibi = MySQLdb.connect(host = serverIP, user = "root", passwd = "unityispower",db = "bibidata");
cursor = bibi.cursor()

class BIBIUserODB:
	def __init__(self, username):
		self.userName = username
		
	def registerAccount(self, passwd, tishi = "Íü¼ÇÃÜÂë"):
		checkSql = "select * from bibi_admin \
		where name = '%s'" % (self.userName)
		cursor.execute(checkSql)
		checkIsOk = cursor.fetchone()
		print checkIsOk
		if (checkIsOk == None):
			regSql = "insert into bibi_admin (name, pwd, tishi) \
			values('%s', '%s', '%s')" % (self.userName, passwd, tishi)
			#print regSql
			try:
				cursor.execute(regSql)
			except:
				print "Error:regAcconut"
			return True
		else:
			return False
		
	def loginAccount(self, passwd):
		loginSql = """select * from bibi_admin
		where name = '%s'
		""" % (self.userName)
		cursor.execute(loginSql)
		infoList = cursor.fetchone()
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
		cursor.execute(searchSql)
		infoList = cursor.fetchone()
		if (infoList == None):
			return ["Error:no word"]
		else:
			return infoList
		
#user = BIBIUserODB("can")
#print user.loginAccount("can")
#print user.registerAccount("can")

bibi.commit()#*************
cursor.close()
bibi.close()