#!/usr/bin/python
# -*- coding:utf-8 -*-

try:
	from PIL import Image, ImageDraw
except ImportError:
	import Image, ImageDraw
import random
import time

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def is_this(self, x, y):
		if self.x ==  x and self.y == y:
			return True
		else:
			return False

class Char(object):
	def __init__(self, image, start_x, start_y, color, index):
		self.image = image
		self.index = index
		self.start_x = start_x
		self.start_y = start_y
		self.width = 0
		self.height = 0
		self.points = []
		self.point_hash = {}
		self.search_point(start_x, start_y, color, False)
		self.init_size()
		self.check_space()

	def search_point(self, x, y, char_color, is_debug):
		self.add_point(x, y, is_debug)
		for point in self.points:
			if (point.y - 1) > 0:  #上
				color = self.image.getpixel((point.x, point.y - 1))
				if color == char_color:
					self.add_point(point.x, point.y - 1, is_debug)

			if (point.x + 1) < self.image.size[0] and (point.y - 1) > 0: #右上
				color = self.image.getpixel((point.x + 1 , point.y - 1))
				if color == char_color:
					self.add_point(point.x + 1 , point.y - 1, is_debug)

			if (point.x + 1) < self.image.size[0]:#右
				color = self.image.getpixel((point.x + 1, point.y))
				if color == char_color:
					self.add_point(point.x + 1, point.y, is_debug)

			if (point.x + 1) < self.image.size[0] and (point.y + 1) < self.image.size[1]:#右下
				color = self.image.getpixel((point.x + 1 , point.y + 1))
				if color == char_color:
					self.add_point(point.x + 1 , point.y + 1, is_debug)

			if (point.y + 1) < self.image.size[1]:#下
				color = self.image.getpixel((point.x , point.y + 1))
				if color == char_color:
					self.add_point(point.x , point.y + 1, is_debug)

			if (point.x - 1) > 0 and (point.y + 1) < self.image.size[1]:#左下
				color = self.image.getpixel((point.x - 1 , point.y + 1))
				if color == char_color:
					self.add_point(point.x - 1 , point.y + 1, is_debug)

			if (point.x - 1) > 0:#左
				color = self.image.getpixel((point.x - 1, point.y))
				if color == char_color:
					self.add_point(point.x - 1, point.y, is_debug)

			if  (point.x - 1) > 0 and (point.y - 1) > 0:  #左上
				color = self.image.getpixel((point.x - 1, point.y - 1))
				if color == char_color:
					self.add_point(point.x - 1, point.y - 1, is_debug)

	def check_space(self):
		for point in self.points:
			if (point.y - 1) > 0:  #上
				if self.is_in(point.x, point.y - 1):
					continue
				elif self.check_arround(point.x, point.y - 1):
					self.add_point(point.x, point.y - 1)
			if (point.x + 1) < self.image.size[0] and (point.y - 1) > 0: #右上
				if self.is_in(point.x + 1 , point.y - 1):
					continue
				elif self.check_arround(point.x + 1 , point.y - 1):
					self.add_point(point.x + 1 , point.y - 1)
			if (point.x + 1) < self.image.size[0]:#右
				if self.is_in(point.x + 1, point.y):
					continue
				elif self.check_arround(point.x + 1, point.y):
					self.add_point(point.x + 1, point.y)
			if (point.x + 1) < self.image.size[0] and (point.y + 1) < self.image.size[1]:#右下
				if self.is_in(point.x + 1 , point.y + 1):
					continue
				elif self.check_arround(point.x + 1 , point.y + 1):
					self.add_point(point.x + 1 , point.y + 1)
			if (point.y + 1) < self.image.size[1]:#下
				if self.is_in(point.x , point.y + 1):
					continue
				elif self.check_arround(point.x , point.y + 1):
					self.add_point(point.x , point.y + 1)
			if (point.x - 1) > 0 and (point.y + 1) < self.image.size[1]:#左下
				if self.is_in(point.x - 1 , point.y + 1):
					continue
				elif self.check_arround(point.x - 1 , point.y + 1):
					self.add_point(point.x - 1 , point.y + 1)
			if (point.x - 1) > 0:#左
				if self.is_in(point.x - 1, point.y):
					continue
				elif self.check_arround(point.x - 1, point.y):
					self.add_point(point.x - 1, point.y)
			if  (point.x - 1) > 0 and (point.y - 1) > 0:  #左上
				if self.is_in(point.x - 1, point.y - 1):
					continue
				elif self.check_arround(point.x - 1, point.y - 1):
					self.add_point(point.x - 1, point.y - 1)

	def check_arround(self, x, y):
		sum_count = 0
		if (y - 1) > 0:  #上
			if self.is_in(x, y - 1):
				sum_count += 1
		if (x + 1) < self.image.size[0] and (y - 1) > 0: #右上
			if self.is_in(x + 1 , y - 1):
				sum_count += 1
		if (x + 1) < self.image.size[0]:#右
			if self.is_in(x + 1, y):
				sum_count += 1
		if (x + 1) < self.image.size[0] and (y + 1) < self.image.size[1]:#右下
			if self.is_in(x + 1 , y + 1):
				sum_count += 1
		if (y + 1) < self.image.size[1]:#下
			if self.is_in(x , y + 1):
				sum_count += 1
		if (x - 1) > 0 and (y + 1) < self.image.size[1]:#左下
			if self.is_in(x - 1 , y + 1):
				sum_count += 1
		if (x - 1) > 0:#左
			if self.is_in(x - 1, y):
				sum_count += 1
		if  (x - 1) > 0 and (y - 1) > 0:  #左上
			if self.is_in(x - 1, y - 1):
				sum_count += 1
		if sum_count >= 6:
			return True
		else:
			return False

	def add_point(self, x, y, is_debug = False):
		is_in = False
		point_hash = str(x) + '|' + str(y)
		if self.point_hash.get(point_hash, 0) == 1:
			if is_debug:
				print 'point is in ', x, y
			is_in = True
		if not is_in:
			if is_debug:
				print 'add point ', x, y
			self.points.append(Point(x, y))
			self.point_hash[point_hash] = 1
		return is_in
		
	def is_in(self, x, y):
		is_in = False
		point_hash = str(x) + '|' + str(y)
		if self.point_hash.get(point_hash, 0) == 1:
			is_in = True
		return is_in

	def init_size(self):
		min_x = 0
		min_y = 0
		max_x = 0
		max_y = 0
		is_first = True
		for point in self.points:
			if is_first:
				is_first = False
				min_x = point.x
				min_y = point.y
				max_x = point.x
				max_y = point.y
			else:
				if point.x < min_x:
					min_x = point.x
				if point.x > max_x:
					max_x = point.x
				if point.y < min_y:
					min_y = point.y
				if point.y > max_y:
					max_y = point.y
		self.width = max_x - min_x
		self.height = max_y - min_y

	def get_size(self):
		return len(self.points)

	def get_points(self):
		return self.points

	def get_width(self):
		return self.width

	def get_height(self):
		return self.height

def get_all_char_data_for_jifeng(image, code, is_train):
	starttime = time.time()
	chars = []
	index = 0
	y = image.size[1]/2
	for x in xrange (image.size[0]):
		color = image.getpixel((x ,y))
		if color != (255, 255, 255):
			is_in_char = False
			for char in chars:
				if char.is_in(x,y):
					is_in_char = True
					break
			if not is_in_char:
				chars.append(Char(image, x, y, color, index))
				index += 1
	endtime = time.time()
	print '字符处理完成！耗时%fs.'%(endtime - starttime)
	result_chars = []
	for i in xrange(0, len(chars)):
		if chars[i].width > 10 and chars[i].height > 10 and len(chars[i].points) > 110:
			result_chars.append(chars[i])
	if len(result_chars) == 4:
		for i in xrange(0, len(result_chars)):
			draw_char(result_chars[i], code, i, is_train)
	else:
		print '预处理出问题'

def draw_char(char, code, index, is_train):
	if is_train:
		path = 'jifeng_train/' + code[index] + "_" + code + "_" + str(random.randint(0, 10000000)) + '.txt'
	else:
		path = 'jifeng_temp/' + code[index] + "_" + code + '.txt'
	f = open(path,"w")
	need_cut_y = 0
	need_cut_x = 0
	im = Image.new('RGB', (char.width, char.height), (255,255,255))
	dr = ImageDraw.Draw(im)
	is_first_point = True
	for point in char.points:
		if is_first_point:
			need_cut_y = point.y
			need_cut_x = point.x
			is_first_point = False
		else:
			if point.y < need_cut_y:
				need_cut_y = point.y 
			if point.x < need_cut_x:
				need_cut_x = point.x
	for point in char.points:
		dr.point((point.x - need_cut_x, point.y - need_cut_y), fill = (0, 0, 0))

	f = open(path,"w")
	im = im.resize((58,80))
	for y in xrange(0,80):
		for x in xrange(0,58):
			g = im.getpixel((x,y))
			if g[0] == 0:
				f.write('1')
			else:
				f.write('0')
		f.write('\n')
	f.close()
	#number_match_handler = NumberMatchHandler()
	# music_img = str(index) + '_' + str(len(char.points)) + '.png'
	# im.save(music_img)
	#return number_match_handler.solve(d)

if __name__ == '__main__':
	image = Image.open('1C7S.png')
	get_all_char_data_for_jifeng(image, '2fes', True) 
