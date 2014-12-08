#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python imports
import json
import re
import requests

# Tornado imports
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
from tornado.web import url

from weibo_handler import VerificationHandlerForWeibo
from baike_handler import VerificationHandlerForBaike
from jifeng_handler import VerificationHandlerForJifeng
from image_pre_handler import pre_handle
from get_verification_from_gif import pre_handle_for_jifeng
from char_handler import get_all_char_data
from char_handler_for_jifeng import get_all_char_data_for_jifeng
import time

# Options
define("port", default=9000, help="Server run on the given port", type=int)
define("debug", default=False, type=bool)

IMG_PATH = 'temp/code.png'

class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			url(r'/code/?$', PostFile),
			url(r'/baike_code/?$', PostBaikeFile),
			url(r'/jifeng_code/?$', PostJifengFile),
			url(r'/baike_code_err/?$', BaikeErr),
		]
		settings = dict(
			debug=options.debug,
			xsrf_cookies=False,
			cookie_secret="nzjxcjasaddsduuqwheazmu293nsadhaslzkci9023nsadnua9sdads/Vo=",
		)
		tornado.web.Application.__init__(self, handlers, **settings)
		self.weibo_handler = VerificationHandlerForWeibo()
		self.baike_handler = VerificationHandlerForBaike()
		self.jifeng_handler = VerificationHandlerForJifeng()

class BaseHandler(tornado.web.RequestHandler):
	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", '*')

	def pool(self):
		return self.application.pool

	def weibo_handler(self):
		return self.application.weibo_handler

	def baike_handler(self):
		return self.application.baike_handler

	def jifeng_handler(self):
		return self.application.jifeng_handler

class PostFile(BaseHandler):
	def get(self):
		pass

	def post(self):
		code = '0'
		print self.request.files
		try:
			fileObj = open(IMG_PATH, 'wb')
			fileObj.write(self.request.files['code.png'][0]['body'])
			fileObj.flush()
			fileObj.close()
			image = pre_handle(IMG_PATH)
			if get_all_char_data(image, 'code', False):
				code = self.weibo_handler().get_verification()
				print '验证码:', code
		except Exception as e:
			print 'err:',e
		self.write(code)
		self.flush()
		self.finish()

class PostBaikeFile(BaseHandler):
	def get(self):
		pass

	def post(self):
		code_type = self.get_argument("type")
		code = '0'
		try:
			fileObj = open(IMG_PATH, 'wb')
			fileObj.write(self.request.files['code.png'][0]['body'])
			fileObj.flush()
			fileObj.close()
			code = self.baike_handler().handle(code_type, IMG_PATH)
			print '验证码:', code
		except Exception as e:
			print 'err:',e
		self.write(code)
		self.flush()
		self.finish()

class PostJifengFile(BaseHandler):
	def get(self):
		pass

	def post(self):
		code = '0'
		print self.request.files
		try:
			fileObj = open(IMG_PATH, 'wb')
			fileObj.write(self.request.files['code.png'][0]['body'])
			fileObj.flush()
			fileObj.close()
			image = pre_handle_for_jifeng(IMG_PATH)
			if get_all_char_data_for_jifeng(image, 'code', False):
				code = self.jifeng_handler().get_verification()
				print '验证码:', code
		except Exception as e:
			print 'err:',e
		self.write(code)
		self.flush()
		self.finish()

class BaikeErr(BaseHandler):
	def get(self):
		pass

	def post(self):
		code_id = self.get_argument("err_id")
		print 'Err code id', code_id
		code = self.baike_handler().report_err(code_id)

if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
