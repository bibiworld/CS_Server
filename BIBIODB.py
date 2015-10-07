#!/usr/bin/python
#coding:utf-8

import MySQLdb
import re

serverIP = "localhost"



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
		""" % (word)#problem?
		self.cursor.execute(searchSql)
		infoList = self.cursor.fetchone()
		if (infoList == None):
			return ["Error:no word"]
		else:
			return infoList
			
	def fuzzyQuery(self, word):
		maxSize = 0
		realList = []
		
		bracket_right = word.find(')')
		if (bracket_right != -1):
			#print bracket_right
			maxSize = int(word[1:bracket_right])
			print maxSize
			word = word[bracket_right+1:]
		if (word == ""):
			print "error1"
			return ["Error:Please input!"]
		checkPattern = "[^a-zA-Z*?]"
		isOK = re.findall(checkPattern, word)
		#print isOK
		if (isOK != []):
			print "error2"
			return ["Error:Invalid input!"]
		word = re.sub('\*', '%', word)
		word = re.sub('\?', '_', word)
		#是否贪婪或者非贪婪
		word = MySQLdb.escape_string(word)
		print word
		querySql = "select * from bibi_word \
		where spell like '%s'" % (word)
		print querySql
		self.cursor.execute(querySql)
		wordList = self.cursor.fetchall()
		if (wordList == []):
			return ["Error:No word!"]
		else:
			for wordGet in wordList:
				#print len(wordGet), maxSize
				if ((maxSize != 0) and (len(wordGet[0]) <= maxSize)):
					print wordGet#unicode 
					realList.append(wordGet)
		return realList
		#return ["GoodJob"]
		
	def commit(self):
		self.bibi.commit()
		
	
	
	
