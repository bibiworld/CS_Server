#!/usr/bin/python
#coding:utf-8

import MySQLdb
import re
import similar

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
			
	
	
	def fuzzyQuery(self, word, ):
		'''
		“.”：匹配任意单个字符
		“?”：匹配前面的子表达式0次或1次。
		“+”：匹配前面的子表达式1次或多次。
		“*”：匹配前面的子表达式0次或多次。x*，表示0个或多个x字符；[0-9]*，匹配任何数量的数字。
		“^”：表示匹配开始位置。
		“$”：表示匹配结束位置。
		“[]”：表示一个集合。[hi]，表示匹配h或i；[a-d]，表示匹配a、b、c、d中任一个。
		“{}”：表示重复的次数。8{5}，表示匹配5个8，即88888；[0-9]{5,11}，表示匹配5到11个数字。
		'''
		maxSize = 1000
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
		checkPattern = "[^a-zA-Z.*?+^$\[\]{}]"
		isOK = re.findall(checkPattern, word)
		#print isOK
		if (isOK != []):
			print "error2"
			return ["Error:Invalid input!"]
		#word = re.sub('\*', '%', word)
		#word = re.sub('\?', '_', word)
		word = '^' + word + '$';
		#是否贪婪或者非贪婪
		word = MySQLdb.escape_string(word)
		print word
		querySql = "select * from bibi_word \
		where spell regexp '%s'" % (word)
		print querySql
		self.cursor.execute(querySql)
		wordList = self.cursor.fetchall()
		if (wordList == []):
			return ["Error:No word!"]
		else:
			for wordGet in wordList:
				#print len(wordGet), maxSize
				if (len(wordGet[0]) <= maxSize):
					print wordGet#unicode 
					realList.append(wordGet)
		return realList
		#return ["GoodJob"]
		
		
	
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
		self.bibi.commit()
		
	
	
	
