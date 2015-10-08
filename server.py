#!/usr/bin/python
#coding:utf-8

import SocketServer
import BIBIUserCheck
import BIBIODB
import re
import select

mybibi = BIBIUserCheck.BIBIUserCheck()
curUser = BIBIODB.BIBIUserODB("未登录")

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
				
	def handle_deal_request(self):
		ready_to_read, ready_to_write, in_error = select.select([self.request], [self.request,], [])
		try:
			self.data = self.request.recv(1024).strip()
		except Exception as msg:
			print "self.request.recv with bug", msg
			self.exceptBug += 1
			if (self.exceptBug > 10):
				return False
			return True
			
		if (len(ready_to_read) == 1 and len(self.data) == 0) or (self.data.count('BIBI_quit') > 0):
			return False
		
		global curUser
		'''
			register 
		'''
		if (mybibi.isRigister(self.data)):
			item = re.findall("\([a-zA-Z]+?\)", self.data)
			print item
			name = item[0].strip('(').strip(')')
			password = item[1].strip('(').strip(')')
			print name, password
			ok = BIBIODB.BIBIUserODB(name)
			reinfo =  ok.registerAccount(password)
			ok.commit()
			print reinfo
			if (reinfo == True):
				self.request.sendall("BIBI_register((1))")
			elif (reinfo == False):
				self.request.sendall("BIBI_register((0))")
			else:
				self.request.sendall("error register")
			'''
				login
			'''
		elif (mybibi.isLogin(self.data)):
			item = re.findall("\([a-zA-Z]+?\)", self.data)
			print item
			name = item[0].strip('(').strip(')')
			password = item[1].strip('(').strip(')')
			print name, password
			ok = BIBIODB.BIBIUserODB(name)
			reinfo =  ok.loginAccount(password)	
			ok.commit()
			print reinfo
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
		elif (mybibi.isSearch(self.data)):
			item = re.findall("\([a-zA-Z]+?\)", self.data)
			word = item[0].strip('(').strip(')')
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
		elif (mybibi.isFuzzy(self.data)):
			item = re.findall("\([a-zA-Z\*\?]+?\)", self.data)
			if (len(item) == 0):
				item = re.findall("\(\([0-9]+?\)[a-zA-Z\*\?]+?\)", self.data)
			print item
			word = item[0].strip('(').strip(')')
			if (word.count(')') > 0):
				word = '(' + word
			print "server.py", word, item[0]
			reinfo = curUser.fuzzyQuery(word)
			#print reinfo
			if (len(reinfo) == 0 or isinstance(reinfo[0], str)):
				self.request.sendall("BIBI_fuzzy(0)")
			else:
				wordlist = ""
				for it in reinfo:
					wordlist = wordlist + it[0].encode("utf-8") + ',' + bracketDeal(it[2]).encode("utf-8") + ';'
				self.request.sendall("BIBI_fuzzy({wordlist})".format(wordlist = wordlist))	
		return True
		
	def handle(self):
		print "{} wrote".format(self.client_address[0])
		self.exceptBug = 0
		while (True):
			if (self.handle_deal_request() == False):
				break
		print "{} quit".format(self.client_address[0])	
				
if __name__ == "__main__":
	HOST, PORT = "59.66.131.106", 1234
	server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	
	server.serve_forever()