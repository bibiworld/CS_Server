#!/usr/bin/python
#coding:utf-8
import MySQLdb

serverIP = "localhost"

bibi = MySQLdb.connect(host = serverIP, user = "root", passwd = "bibiworld",db = "bibidata", charset = "utf8");
cursor= bibi.cursor()

def commit():
	global bibi
	bibi.commit()
	
def close():
	global bibi
	bibi.close()