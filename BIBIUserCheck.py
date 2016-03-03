#encoding=utf-8

class BIBIUserCheck(object):
	BIBI_INIT_POS = 5
	BIBI_REGISTER_BRACKETS = 3
	BIBI_LOGIN_BRACKETS = 3
	BIBI_SEARCH_BRACKETS = 1
	BIBI_FUZZY_BRACKETS = 2
	BIBI_SIMILAR_BRACKETS = 1
	BIBI_SENTENCE_BRACKETS = 1
	
	
	'''
		check if it is register request
	'''
	def isRegister(self, tcpData):
		if (tcpData.count('(') < self.BIBI_REGISTER_BRACKETS):
			return False
		#remain the first request
		while (tcpData.count('(') > self.BIBI_REGISTER_BRACKETS):
			tcpData = tcpData[:-1]
			
		if (tcpData.find('register') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_REGISTER_BRACKETS) and (tcpData.count(')') == self.BIBI_REGISTER_BRACKETS):
				print "Rigister ", tcpData, "Rigister"
				return tcpData
		return False
		
	'''
		check if it is login request
	'''
	def isLogin(self, tcpData):
		if (tcpData.count('(') < self.BIBI_LOGIN_BRACKETS):
			return False
		#remain the first request
		while (tcpData.count('(') > self.BIBI_LOGIN_BRACKETS):
			tcpData = tcpData[:-1]
			
		if (tcpData.find('login') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_LOGIN_BRACKETS) and (tcpData.count(')') == self.BIBI_LOGIN_BRACKETS):
				print "Login ", tcpData, "Login"
				return tcpData
		return False
		
	'''
		check if it is search request
	'''
	def isSearch(self, tcpData):
		if (tcpData.count('(') < self.BIBI_SEARCH_BRACKETS):
			return False
		#remain the first request	
		while (tcpData.count('(') > self.BIBI_SEARCH_BRACKETS):
			tcpData = tcpData[:-1]

		if (tcpData.find('search') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_SEARCH_BRACKETS) and (tcpData.count(')') == self.BIBI_SEARCH_BRACKETS):
				print "Search ", tcpData, "Search"
				return tcpData
		return False
		
	'''
		check if it is fuzzy
	'''
	def isFuzzy(self, tcpData):
		if (tcpData.count('(') < self.BIBI_FUZZY_BRACKETS):
			return
		#remain the first request
		while (tcpData.count('(') > self.BIBI_FUZZY_BRACKETS):
			tcpData = tcpData[:-1]
			
		if (tcpData.find('fuzzy') == self.BIBI_INIT_POS):
			if ((tcpData.count('(') == self.BIBI_SEARCH_BRACKETS) and (tcpData.count(')') == self.BIBI_SEARCH_BRACKETS))\
			or ((tcpData.count('(') == self.BIBI_FUZZY_BRACKETS) and (tcpData.count(')') == self.BIBI_FUZZY_BRACKETS)):
				print "Fuzzy ", tcpData, "Fuzzy"
				return tcpData
		return False
		
	'''
		check if it is similar
	'''
	def isSimilar(self, tcpData):
		if (tcpData.count('(') < self.BIBI_SIMILAR_BRACKETS):
			return
		#remain the first request
		while (tcpData.count('(') > self.BIBI_SIMILAR_BRACKETS):
			tcpData = tcpData[:-1]
			
		if (tcpData.find('similar') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_SIMILAR_BRACKETS) and (tcpData.count(')') == self.BIBI_SIMILAR_BRACKETS):
				print "Similar ", tcpData, "Similar"
				return tcpData
		return False
		
	'''
		check if it is sentence
	'''
	def isSentence(self, tcpData):
		if (tcpData.count('(') < self.BIBI_SENTENCE_BRACKETS):
			return
		#remain the first request
		while (tcpData.count('(') > self.BIBI_SENTENCE_BRACKETS):
			tcpData = tcpData[:-1]
			
		if (tcpData.find('sentence') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_SENTENCE_BRACKETS) and (tcpData.count(')') == self.BIBI_SENTENCE_BRACKETS):
				print "Sentence ", tcpData, "Sentence"
				return tcpData
		return False
		
		
		
	
	