#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import operator
from numpy import *
import time

class VerificationHandlerForWeibo(object):
	def __init__(self):
		super(VerificationHandlerForWeibo, self).__init__()
		self.data = []
		self.label = []
		starttime = time.time()
		self.load_train_data()
		endtime = time.time()
		print '微博训练数据加载完成，耗时%fs.'%(endtime - starttime)

	def load_train_data(self):
		path = 'train/'
		sum = 0
		for file in os.listdir(path):
			f = open(path + file)
			self.label.append(file[0])
			d = []
			sum += 1
			for i in f.readlines():
				a = [int(x) for x in i.strip()]
				d.extend(a)
			self.data.append(d)

	def solve(self, d):
		data = array(self.data)
		size = data.shape[0]
		k = 4
		diff = tile(d,(size,1)) - data
		diff = diff ** 2
		distance = diff.sum(axis = 1)
		distance = distance ** 0.5
		datasort = distance.argsort()
		classcount = {}
		for i in range(k):
			vol = self.label[datasort[i]]
			classcount[vol] = classcount.get(vol,0) + 1 + (k - i) * 0.05
		sortcount = sorted(classcount.iteritems(),key = operator.itemgetter(1),reverse = True)
		return sortcount[0][0]
		
	def get_verification(self):
		path = 'temp/'
		first_code = ''
		sec_code = ''
		th_code = ''
		fou_code = ''
		for dir in os.listdir(path):
			if dir.endswith('.txt'):
				if dir[0] == 'c':
					f = open(path + dir)
					d = []
					for i in f.readlines():
						a = [int(x) for x in i.strip()]
						d.extend(a)
					first_code = self.solve(d)
				elif dir[0] == 'o':
					f = open(path + dir)
					d = []
					for i in f.readlines():
						a = [int(x) for x in i.strip()]
						d.extend(a)
					sec_code = self.solve(d)
				elif dir[0] == 'd':
					f = open(path + dir)
					d = []
					for i in f.readlines():
						a = [int(x) for x in i.strip()]
						d.extend(a)
					th_code = self.solve(d)
				elif dir[0] == 'e':
					f = open(path + dir)
					d = []
					for i in f.readlines():
						a = [int(x) for x in i.strip()]
						d.extend(a)
					fou_code = self.solve(d)
		return first_code + sec_code + th_code + fou_code;

def fun3():
	starttime = time.time()
	verificationHandlerForWeibo = VerificationHandlerForWeibo()
	verificationHandlerForWeibo.load_train_data()
	endtime = time.time()
	code = verificationHandlerForWeibo.get_verification()
	print '字符匹配完成, 耗时%fs.'%(endtime - starttime)
	return code
	

