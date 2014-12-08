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
	def __init__(self, image, start_x, start_y, index):
		self.image = image
		self.start_x = start_x
		self.start_y = start_y
		self.index = index

		self.points = []

		self.search_next_point(start_x, start_y, False)

	def search_next_point(self, x, y, is_debug):
		color = self.image.getpixel((x, y))
		if color == 0 and not self.add_point(x, y, is_debug):
			if (y - 1) > 0:  #上
				self.search_next_point(x, y - 1, is_debug)

			if (x + 1) < self.image.size[0] and (y - 1) > 0: #右上
				self.search_next_point(x + 1 , y - 1, is_debug)

			if (x + 1) < self.image.size[0]:#右
				self.search_next_point(x + 1, y, is_debug)

			if (x + 1) < self.image.size[0] and (y + 1) < self.image.size[1]:#右下
				self.search_next_point(x + 1 , y + 1, is_debug)

			if (y + 1) < self.image.size[1]:#下
				self.search_next_point(x , y + 1, is_debug)

			if (x - 1) > 0 and (y + 1) < self.image.size[1]:#左下
				self.search_next_point(x - 1 , y + 1, is_debug)

			if (x - 1) > 0:#左
				self.search_next_point(x - 1, y, is_debug)

			if  (x - 1) > 0 and (y - 1) > 0:  #左上
				self.search_next_point(x - 1, y - 1, is_debug)

	def add_point(self, x, y, is_debug):
		is_in = False
		for point in self.points:
			if point.is_this(x, y):
				if is_debug:
					print 'point is in ', x, y
				is_in = True
				break
		if not is_in:
			if is_debug:
				print 'add point ', x, y
			self.points.append(Point(x, y))
		return is_in
		
	def is_in(self, x, y):
		is_in = False
		for point in self.points:
			if point.is_this(x, y):
				is_in = True
				break
		return is_in

	def get_size(self):
		return len(self.points)

	def get_points(self):
		return self.points

def get_all_char_data(image, code, is_train):
	starttime = time.time()
	chars = {}
	index = 0
	for x in xrange (image.size[0]):
		for y in xrange (image.size[1]):
			color = image.getpixel((x ,y))
			if color == 0:
				is_in_char = False
				for char, size in chars.items():
					if char.is_in(x,y):
						is_in_char = True
						break
				if not is_in_char:
					temp_char = Char(image, x, y, index)
					chars[temp_char] = temp_char.get_size()
					index += 1

	

	count = 0
	max_size = 0
	for char, size  in chars.items():
	 	if size >5:
	 		count += 1

	if count < 4:
		endtime = time.time()
		print '图像' + code + '有字符连在一起，切分失败，字符处理失败！耗时:', (endtime - starttime)
		return False
	else:
		dict= sorted(chars.iteritems(), key=lambda d:d[1], reverse = True)
		useful_chars = {}
		for i in xrange(4):
			useful_chars[dict[i][0].index] = dict[i][0]

		index = 0
		dict= sorted(useful_chars.iteritems(), key=lambda d:d[0])
		for i in xrange(4):
			draw_char(dict[i][1], code, index, is_train)
			index += 1

		endtime = time.time()
		print '字符处理完成！耗时%fs.'%(endtime - starttime)
		return True

def draw_char(char, code, index, is_train):
	if is_train:
		path = 'train/' + code[index] + "_" + code + "_" + str(random.randint(0, 10000000)) + '.txt'
	else:
		path = 'temp/' + code[index] + "_" + code + '.txt'
	f = open(path,"w")
	start_x = 100
	start_y = 100
	end_x = 0
	end_y = 0
	for point in char.get_points():
		if point.x < start_x:
			start_x = point.x

		if point.y < start_y:
			start_y = point.y

		if point.x > end_x:
			end_x = point.x

		if point.y > end_y:
			end_y = point.y

	inx = Image.new('RGBA', (end_x - start_x,  end_y - start_y), (255, 255, 255)).convert('L')
	draw = ImageDraw.Draw(inx)

	for point in char.get_points():
		draw.point((point.x - start_x, point.y - start_y), 0)

	inx = inx.resize((32,32))
	for x in xrange(0,32):
		for y in xrange(0,32):
			g = inx.getpixel((y,x))
			if g < 136:
				f.write('1')
			else:
				f.write('0')
		f.write('\n')

if __name__ == '__main__':
	image = Image.open('a544.png')
	get_all_char_data(image, 'a544', True)