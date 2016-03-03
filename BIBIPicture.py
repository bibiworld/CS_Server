#coding:utf-8
import conn
import os,sys

def BIBIPicture(word):
	path1 = "../data/image/imgcombination/"+word+".jpg"
	path2 = "../data/image/imgcombination/"+word+".png"
	#print path1, path2
	if os.path.isfile(path1):
		return path1
	if os.path.isfile(path2):
		return path2
	return ""
		