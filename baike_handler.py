#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import hashlib
import uuid
import time
from datetime import date
from send_mail import send_mail

info_server = 'http://common.taskok.com:9000/Service/ServerConfig.aspx'

S_ID  = 98310
S_KEY = "c454f5cc8cf44ddb9dbb50453c5a67c2"
USER_NAME = 'sonidigg'
USER_PASSWORD = 'sonidigg'

LOGIN_TAIL = '/Upload/UULogin.aspx'
GET_SCORE_TAIL = '/Upload/GetPoint.aspx'
UPLOAD_TAIL = '/Upload/Processing.aspx'
GET_RESULT_TAIL = '/Upload/GetResult.aspx'
REPORT_ERR_TAIL = '/Upload/ReportError.aspx'

class VerificationHandlerForBaike(object):
	"""docstring for VerificationHandlerForBaike"""
	def __init__(self):
		super(VerificationHandlerForBaike, self).__init__()
		self.login_server = ''
		self.upload_server = ''
		self.result_server = ''
		self.backup_server = ''
		self.get_result_delay = 1000
		self.user_id = 100
		self.user_key = ''
		self.last_send_score_date = ''

		self.is_login = False
		if self.get_servers():
			self.is_login = self.login()
		
	def get_servers(self):
		headers = self.get_common_header()
		response = requests.get(info_server, headers = headers)
		if response.status_code == 200:
			all_info = response.text.split(',')
			self.get_result_delay = int(all_info[0])
			for info in all_info:
				if info.endswith(':101'):
					self.login_server = 'http://' + info[0 : len(info) - 4]
				if info.endswith(':102'):
					self.upload_server = 'http://' + info[0 : len(info) - 4]
				if info.endswith(':103'):
					self.result_server = 'http://' + info[0 : len(info) - 4]
				if info.endswith(':104'):
					self. backup_server= 'http://' + info[0 : len(info) - 4]
			return True
		else:
			return False

	def get_common_header(self):
		headers = {}
		headers['SID'] = S_ID
		headers['HASH'] = hashlib.md5(str(S_ID) + S_KEY.upper()).hexdigest()
		headers['UUVersion'] = '1.0.0.1'
		headers['UID'] = self.user_id
		headers['User-Agent'] = hashlib.md5(S_KEY.upper() + str(self.user_id)).hexdigest()
		return headers

	def login(self):
		headers = self.get_common_header()
		mac=uuid.UUID(int=uuid.getnode()).hex[-12:]
		headers['KEY'] = hashlib.md5(S_KEY.upper() + USER_NAME.upper()).hexdigest() + mac
		headers['UUKEY'] = hashlib.md5(USER_NAME.upper() + mac + S_KEY.upper()).hexdigest()
		payload = {'U' : USER_NAME, 'p' : hashlib.md5(USER_PASSWORD).hexdigest()}
		login_server = self.login_server + LOGIN_TAIL
		response = requests.get(login_server, headers = headers, params = payload)
		if '_' in response.text:
			self.user_key = response.text
			self.user_id = int(response.text.split('_')[0])
			return True
		else:
			errorMsg={'-1':'参数错误，用户名为空或密码为空','-2':'用户不存在','-3': '密码错误',
				'-4':' 账户被锁定','-5':' 非法登录','-6':' 用户点数不足，请及时充值',
				'-8':' 系统维护中','-9':' 其他'}
			print errorMsg[response.text]
			send_mail('验证码识别遇到问题', errorMsg[response.text])
			return  False

	def get_score(self):
		headers = self.get_common_header()
		headers['UUAgent'] =  hashlib.md5(self.user_key.upper() + str(self.user_id) + S_KEY).hexdigest()
		headers['KEY'] = self.user_key
		payload = {'U' : USER_NAME, 'p' : hashlib.md5(USER_PASSWORD).hexdigest()}
		login_server = self.login_server + GET_SCORE_TAIL
		response = requests.get(login_server, headers = headers, params = payload)
		return response.text

	def handle(self, codetype, file):
		if not self.is_login:
			if self.get_servers():
				self.is_login = self.login()
		if self.is_login:
			score = int(self.get_score())
			print '验证码识别分数:', score
			if self.last_send_score_date != date.today():
				send_mail('验证码识别', '验证码识别，当前积分' + str(score) + '！')
				self.last_send_score_date = date.today()
			if score < 100:
				send_mail('验证码识别', '验证码识别积分不足，当前积分' + str(score) + '，请尽快充值！')
			if self.get_servers():
				data={'KEY' : self.user_key.upper(), 
				"SID" : S_ID,
				'SKey' : hashlib.md5(self.user_key.lower() + str(S_ID) + S_KEY).hexdigest(),
				'TimeOut' : '30000',
				'Type' : codetype,
				"Version" : "100"}
				response = requests.post(self.upload_server + UPLOAD_TAIL, data = data, files = {"IMG":open(file, 'rb')})
				if '|' in response.text:
					info = response.text.split('|')
					return info[1] + '|' + info[0]
				else:
					return self.get_result(response.text)

	def get_result(self,id):
		headers = self.get_common_header()
		payload = {'key' : self.user_key, 'id' : id}
		result_server = self.result_server + GET_RESULT_TAIL
		response = requests.get(result_server , headers = headers, params = payload)
		context = response.text
		if context=="203" or context=="-3":
			time.sleep(self.get_result_delay/1000)
			return self.get_result(id)
		else:
			return context + '|' + id

	def report_err(self, id):
		headers = self.get_common_header()
		skey = hashlib.md5(self.user_key.lower() + str(S_ID) + S_KEY).hexdigest()
		payload = {'KEY' : self.user_key, 'ID' : id, 'SID' : S_ID, 'SKEY' : skey}
		result_server = self.result_server + REPORT_ERR_TAIL
		rety_count = 0
		while True:
			response = requests.get(result_server , headers = headers, params = payload)
			context = response.text
			if context =='OK':
				print 'Report err ok!'
				break
			else:
				rety_count += 1
				if rety_count > 3:
					print 'Report err end and report result is fail!'
					break
				else:
					print 'Report err fail response is', context, ',and retry count is', rety_count

if __name__ == '__main__':
	pic_file_path = ('/home/yueguang/python/verification/UU打码/test_pics/test.png') 
	handler = VerificationHandlerForBaike()
	result = handler.handle('2002', pic_file_path)
	print '结果:', result