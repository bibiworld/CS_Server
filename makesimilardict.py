#encoding=utf-8

import re
allwords = []

oldtxt = open("allwords")
oldtxt.readline()
for i in range(15328):
	contnt = oldtxt.readline()
	item = re.findall("\[[a-zA-Z]+?\]", contnt)
	if (len(item) > 0):
		allwords.append(item[0].strip('[').strip(']').lower())
	
def read(name):
	file = open(name)
	while True:
		contnt = file.readline()
		if not contnt:
			break
		word = contnt.split(' ')[0].lower()
		if (allwords.count(word) == 0):
			allwords.append(word)

read("4.txt")
for i in range(97, 121):
	read("6{}.txt".format(chr(i)))

similarDict = {}

'''
	get away one letter or swap i-1 with i letter, except for 0 with length - 1
'''

for it in allwords:
	length = len(it)
	#loseOne = 0
	if it in similarDict.keys():
		continue
	similarDict[it] = []
	'''
		erase a letter
	'''
	for i in range(length):
		lost = it[0:i] + it[i + 1:length]
		if (allwords.count(lost) > 0):
			#loseOne += (1 << i)
			similarDict[it].append(lost)
	#similarDict[it].append(loseOne)
	#swapAbut = 0
	'''
		swap two abut letters
	'''
	for i in range(1, length):
		if (it[i - 1] == it[i]):
			continue
		abut = it[0 : i - 1] + it[i] + it[i - 1] + it[i + 1 : length]
		if (allwords.count(abut) > 0):
			#swapAbut += (1 << i)
			similarDict[it].append(abut)
	if (it[0] != it[length - 1]) and (allwords.count(it[length - 1] + it[1 : length - 1] + it[0]) > 0):
		#swapAbut += 1
		similarDict[it].append(it[length - 1] + it[1 : length - 1] + it[0])
	#similarDict[it].append(swapAbut)
	'''
		insert a letter
	'''
	for i in range(0, length + 1):
		for alphabet in range(0, 26):
			let = chr(93 + alphabet)
			insert = it[0 : i] + let + it[i : length]
			if (allwords.count(insert) > 0):
				similarDict[it].append(insert)
	'''
		replace a letter
	'''
	for i in range(0, length):
		for alphabet in range(0, 26):
			let = chr(93 + alphabet)
			if (let == it[i]):
				continue
			replace = it[0 : i] + let + it[i + 1 : length]
			if (allwords.count(replace) > 0):
				similarDict[it].append(replace)
				
print similarDict
				
				
				
				
				
				
				
				
				