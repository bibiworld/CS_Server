#!/usr/bin/python
#coding:utf-8

import BIBIUserODB
import conn

userName = ""
	
def searchWord(word, user = None):#user is the accout of searchWord
	global userName
	userName = ""
	if (user != None):
		userName = user.userName
		print userName
		
	
	searchSql = """select * from bibi_word
	where spell = '%s'
	""" % (word)#problem?
	print searchSql
	conn.cursor.execute(searchSql)
	infoList = conn.cursor.fetchone()
	if (infoList == None):
		return ["Error:no word"]
	else:
		return infoList
		


def fuzzyQuery(word, user = None):
	global userName
	userName = ""
	if (user != None):
		userName = user.userName
		print userName
		
	
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
	conn.cursor.execute(querySql)
	wordList = conn.cursor.fetchall()
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
