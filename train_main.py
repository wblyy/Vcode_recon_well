#!/usr/bin/python
# -*- coding:utf-8 -*-

try:
	from PIL import Image
except ImportError:
	import Image

import os
from image_pre_handler import pre_handle
from char_handler import get_all_char_data
from char_handler_for_jifeng import get_all_char_data_for_jifeng

#提取训练数据
if __name__ == '__main__':
	# path = "train_image/"
	# sum = 0
	# for image_file in os.listdir(path):
	# 	code = image_file.split('.')[0]
	# 	image = pre_handle(path + image_file)
	# 	get_all_char_data(image, code, True)
	# 	sum += 1
	path = "jifeng_train_image/"
	sum = 0
	for image_file in os.listdir(path):
		code = image_file.split('.')[0]
		image = Image.open(path + image_file)
		get_all_char_data_for_jifeng(image, code, True)
		sum += 1
		
