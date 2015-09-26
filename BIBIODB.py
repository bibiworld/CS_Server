#!/usr/bin/python
#coding:utf-8
'''
registerAccount():
	传入,两个参数，密码，提示，其中提示默认为“忘记密码”
	注册成功时返回True，失败为False，
	出现bug， print "Error:regAcconut"

loginAccount():
	传入一个参数，密码（字符串）
	登陆成功是返回“goodjob”， 失败为 "Error:passwd is wrong"
	
searchWord():
	查询单词，传入一个参数，单词拼写
	成功返回单词列表信息eg:["word","wɜ:d","n.单词","例句"]，失败返回列表 ["Error:no word"]

注意，调用该类的函数后最后必须调用close函数提交数据至数据库	.
'''
import MySQLdb
import re

serverIP = "localhost"



class BIBIUserODB:
	def __init__(self, username):
		global serverIP
		self.bibi = MySQLdb.connect(host = serverIP,user = "root",passwd = "unityispower",db = "bibidata",charset = "utf8");
		self.cursor= self.bibi.cursor()
		self.userName = username
		
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
		
		bracket_right = word.find(')')
		if (bracket_right != -1):
			#print bracket_right
			maxSize = word[1:bracket_right]
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
		wordList = self.cursor.fetchone()
		if (wordList == []):
			return ["Error:No word!"]
		else:
			print wordList[2].encode("gbk")
			#for wordGet in wordList:
			#	print wordGet.encode("gbk")
		return ["GoodJob"]
		
	def close(self):
		self.bibi.commit()
		self.cursor.close()
		self.bibi.close()
	
	
	
