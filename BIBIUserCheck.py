#encoding=utf-8

class BIBIUserCheck(object):
	BIBI_INIT_POS = 5
	BIBI_REGISTER_BRACKETS = 3
	BIBI_LOGIN_BRACKETS = 3
	BIBI_SEARCH_BRACKETS = 1
	BIBI_FUZZY_BRACKETS = 2
	BIBI_SIMILAR_BRACKETS = 1
	'''
		check if it is register request
	'''
	def isRegister(self, tcpData):
		if (tcpData.find('register') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_REGISTER_BRACKETS) and (tcpData.count(')') == self.BIBI_REGISTER_BRACKETS):
				print tcpData, "Rigister"
				return True
		return False
		
	'''
		check if it is login request
	'''
	def isLogin(self, tcpData):
		if (tcpData.find('login') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_LOGIN_BRACKETS) and (tcpData.count(')') == self.BIBI_LOGIN_BRACKETS):
				print tcpData, "Login"
				return True
		return False
		
	'''
		check if it is search request
	'''
	def isSearch(self, tcpData):
		if (tcpData.find('search') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_SEARCH_BRACKETS) and (tcpData.count(')') == self.BIBI_SEARCH_BRACKETS):
				print tcpData, "Search"
				return True
		return False
		
	'''
		check if it is fuzzy
	'''
	def isFuzzy(self, tcpData):
		if (tcpData.find('fuzzy') == self.BIBI_INIT_POS):
			if ((tcpData.count('(') == self.BIBI_SEARCH_BRACKETS) and (tcpData.count(')') == self.BIBI_SEARCH_BRACKETS))\
			or ((tcpData.count('(') == self.BIBI_FUZZY_BRACKETS) and (tcpData.count(')') == self.BIBI_FUZZY_BRACKETS)):
				print tcpData, "Fuzzy"
				return True
		return False
	
	def isSimilar(self, tcpData):
		if (tcpData.find('similar') == self.BIBI_INIT_POS):
			if (tcpData.count('(') == self.BIBI_SIMILAR_BRACKETS) and (tcpData.count(')') == self.BIBI_SIMILAR_BRACKETS):
				print tcpData, "Similar"
				return True
		return False
	
	
	