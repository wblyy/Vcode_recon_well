#!/usr/bin/python
# -*- coding:utf-8 -*-

from image_pre_handler import pre_handle
from char_handler import get_all_char_data
import verification_handler

def process(image_dir):
	image = pre_handle(image_dir)
	get_all_char_data(image, 'code', False)
	print verification_handler.fun3()

#用来本地验证
if __name__ == '__main__':
	path = "testpic/"
	process(path + 'code.png')
