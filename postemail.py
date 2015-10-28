#!/usr/bin/env python
#encoding=utf-8

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def _format_addr(s):
	name, addr = parseaddr(s)
	return formataddr(( \
		Header(name, 'utf-8').encode(), \
		addr.encode('utf-8') if isinstance(addr, unicode) else addr))

from_addr = raw_input('From: ')
password = raw_input('Password: ')
to_addr = raw_input('To: ')
smtp_server = raw_input('SMTP server: ')

msg = MIMEText('welcome to bibiworld!\n欢迎来到bibiworld！\n', 'plain', 'utf-8')
msg['From'] = _format_addr(u'BIBIGroup <%s>' % from_addr)
msg['To'] = _format_addr(u'亲 <%s>' % to_addr)
msg['Subject'] = Header(u'来自BIBI的问候', 'utf-8')
'''
	如果MIMEText()中不含中文, subject有中文, 则无法发送邮件
	如果都不含中文, 可以发送邮件; 如果都含中文, 也可以发送邮件
'''

print "******************************"
print "msg:", msg
print "******************************"

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()