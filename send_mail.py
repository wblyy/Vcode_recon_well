#!/bin/python
#-*- encoding: utf-8 -*-

import smtplib,mimetypes
from email.mime.text import MIMEText

def send_mail(sub, content):
	'''
	mailto_list:发给谁
	sub:主题
	content:内容
	send_mail("aaa@126.com","主题","内容")
	'''
	#要发给谁
	#mailto_list = ["cye520love@gmail.com"]#"baonanhai@gmail.com"]#, "1126918258@qq.com", "peng2011@vip.qq.com"]
	mailto_list = ["baonanhai@gmail.com", "wblyy0911@gmail.com"]

	#设置服务器，用户名、口令以及邮箱的后缀
	mail_host = "smtp.126.com"
	mail_user = "b1n2h3"
	mail_pass = "nihao123"
	mail_postfix="126.com"

	me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
	msg = MIMEText(content)
	msg['Subject'] = sub
	msg['From'] = me
	msg['To'] = ";".join(mailto_list)
	try:
		s = smtplib.SMTP(mail_host)
		#对于使用gmail的情况无本行则会出现 "SMTP AUTH extension not supported by server."
		s.docmd("EHLO server")
		#使用ssl加密
		s.starttls()
		s.login(mail_user,mail_pass)
		s.sendmail(me, mailto_list, msg.as_string())
		s.close()
		return True,"Send Email OK."
	except Exception, e:
		print str(e)
		return False,"Send Email Error."

if __name__ == '__main__':
	send_mail('通知:机器人,验证码', '.填验证码')
