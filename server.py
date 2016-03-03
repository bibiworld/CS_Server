#!/usr/bin/python
#coding:utf-8

import SocketServer
import BIBIUserCheck
import BIBIODB
import re
import select
import time


mybibi = BIBIUserCheck.BIBIUserCheck()
curUser = BIBIODB.BIBIODB("未登录")



'''
	replace () with <**>
'''
def bracketDeal(si):
	if (si.count('(') > 0):
		si = si.replace('(', '<*', si.count('('))
	if (si.count(')') > 0):
		si = si.replace(')', '*>', si.count(')'))
	return si



	
class MyTCPHandler(SocketServer.BaseRequestHandler):
	'''
		after handle self.request(socket) will close
	'''
	#def __init__(self, request = 0, client_address = 0, server = 0):
	#	print "wocaonima"
	#	SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
	#	self.exceptBug = 0
		
	'''
	send message
	'''
	def sendMessage(self, curUser, message):
		self.request.sendall(message)
		
		
		
	'''
		register 
	'''
	def doRegister(self, curUser):
		item = re.findall("\([a-zA-Z]+?\)", self.data)
		if (len(item) != 2):
			return
		name = item[0].strip('(').strip(')')
		password = item[1].strip('(').strip(')')
		print "server.py", name, password
		ok = BIBIODB.BIBIODB(name)
		reinfo =  ok.registerAccount(password)
		ok.commit()
		if (reinfo == True):
			self.request.sendall("BIBI_register((1))")
		elif (reinfo == False):
			self.request.sendall("BIBI_register((0))")
		else:
			self.request.sendall("error register")
	
	
	
	
	'''
		login
	'''
	def doLogin(self, curUser):
		item = re.findall("\([a-zA-Z0-9]+?\)", self.data)
		if (len(item) != 2):
			return
		name = item[0].strip('(').strip(')')
		password = item[1].strip('(').strip(')')
		print "server.py", name, password
		ok = BIBIODB.BIBIODB(name)
		reinfo =  ok.loginAccount(password)	
		ok.commit()
		if (reinfo.count("Error:Name is wrong") == 1):
			self.request.sendall("BIBI_login((0)(0))")
		elif (reinfo.count("Error:passwd is wrong") == 1):
			self.request.sendall("BIBI_login((1)(0))")
		elif (reinfo.count("GoodJob") == 1):
			self.request.sendall("BIBI_login((1)(1))")
			curUser = ok
		else:
			self.request.sendall("error login")
	
	
	
	
	'''
		search
	'''	
	def doSearch(self, curUser):
		item = re.findall("\([a-zA-Z]+?\)", self.data)
		if (len(item) != 1):
			return
		word = item[0].strip('(').strip(')').lower()
		reinfo = curUser.searchWord(word)
		if (len(reinfo) == 1):
			self.request.sendall("BIBI_search((0)(0)(0)(0))")
		else:
			wordInfo = []
			for i in range(4):
				si = reinfo[i]
				if (si.count('(') > 0):
					si = si.replace('(', '<*', si.count('('))
				if (reinfo[i].count(')') > 0):
					si = si.replace(')', '*>', si.count(')'))
				if (len(si) == 0):
					si = '0'
				wordInfo.append(si)
			self.request.sendall("BIBI_search(({words})({soundmark})({meaning})({examples}))".format(words=wordInfo[0].encode("utf-8"), soundmark=wordInfo[1].encode("utf-8"), meaning=wordInfo[2].encode("utf-8"),examples=wordInfo[3].encode("utf-8")))
			
			
			
			
	'''
		fuzzy
	'''
	def doFuzzy(self, curUser):
		item = re.findall("\([a-zA-Z\*\?]+?\)", self.data)
		if (len(item) == 0):
			item = re.findall("\(\([0-9]+?\)[a-zA-Z\*\?]+?\)", self.data)
		if (len(item) != 1):
			return
		word = item[0].strip('(').strip(')').lower()
		if (word.count(')') > 0):
			word = '(' + word
		print "server.py", word, item[0]
		reinfo = curUser.fuzzyQuery(word)
		if (len(reinfo) == 0 or isinstance(reinfo[0], str)):
			self.request.sendall("BIBI_fuzzy(0)")
		else:
			wordlist = ""
			for it in reinfo:
				wordlist = wordlist + it[0].encode("utf-8") + ',' + bracketDeal(it[2]).encode("utf-8") + ';'
			self.request.sendall("BIBI_fuzzy({wordlist})".format(wordlist = wordlist))	
	
	
	
	
	
	'''
		similar
	'''
	def doSimilar(self, curUser):
		item = re.findall("\([a-zA-Z]+?\)", self.data)
		if (len(item) != 1):
			return
		word = item[0].strip('(').strip(')').lower()
		reinfo = curUser.similarQuery(word)
		if (len(reinfo) == 0):
			self.request.sendall("BIBI_similar(0)")
		else:
			wordlist = ""
			for it in reinfo:
				wordlist = wordlist + it.encode("utf-8") + ','
			self.request.sendall("BIBI_similar({word}:{wordlist})".format(word = word, wordlist = wordlist))
		
		
		
	'''
		sentence
	'''
	def doSentence(self, curUser):
		english, chinese =  curUser.sentenceQuery()
		english = bracketDeal(english)
		chinese = bracketDeal(chinese)
		
		diaoshi = "BIBI_sentence(({english})({chinese}))".format(english = english, chinese = chinese.encode("utf-8"))
		print "sentence::: " + diaoshi
		self.request.sendall(diaoshi)
		#self.request.sendall("BIBI_sentence(({english})({chinese}))".format(english = english, chinese = chinese.encode("utf-8")))
		
	'''
		deal every handle request
	'''
	def handle_deal_request(self):
		ready_to_read, ready_to_write, in_error = select.select([self.request], [self.request,], [])
		self.data = ""
		if len(ready_to_read) > 0:
			try:
				self.data = self.request.recv(1024).strip()
				'''if (self.data.count(self.lastCMD) > 0):
					time.sleep(1)
				else:
					self.lastCMD = self.data'''
				print "data read", len(self.data), self.data
			except Exception as msg:
				print "self.request.recv with bug", msg
				'''self.exceptBug += 1
				if (self.exceptBug > 10):
					return False
				return True'''
				return False
			
		if (len(ready_to_read) == 1 and len(self.data) == 0) or (self.data.count('BIBI_quit') > 0):
			return False
		
		global curUser
	
		if (mybibi.isRegister(self.data)):
			self.doRegister(curUser)
			
		elif (mybibi.isLogin(self.data)):
			self.doLogin(curUser)
			
		elif (mybibi.isSearch(self.data)):
			self.doSearch(curUser)
			
		elif (mybibi.isFuzzy(self.data)):
			self.doFuzzy(curUser)
			
		elif (mybibi.isSimilar(self.data)):
			self.doSimilar(curUser)
			
		elif (mybibi.isSentence(self.data)):	
			self.doSentence(curUser)
			
		return True
		
		
		
		
		
	def handle(self):
		print "{} wrote".format(self.client_address[0])
		self.exceptBug = 0
		self.lastCMD = ""
		while (True):
			if (self.handle_deal_request() == False):
				break
			time.sleep(1)
		print "{} quit".format(self.client_address[0])	
				
				
				
				
if __name__ == "__main__":
	HOST, PORT = "0.0.0.0", 1234
	server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	
	server.serve_forever()
