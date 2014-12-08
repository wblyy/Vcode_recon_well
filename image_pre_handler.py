#!/usr/bin/python
# -*- coding:utf-8 -*-

try:
	from PIL import Image, ImageDraw
except ImportError:
	import Image, ImageDraw
import time

#二值化
def twopi(img):
	img = img.convert("RGBA")
	pixdata = img.load()
	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixdata[x,y][0] < 90:
				pixdata[x,y] = (0,0,0,255)
	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixdata[x,y][1] < 136:
				pixdata[x,y] = (0,0,0,125)
	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixdata[x,y][2] > 0:
				pixdata[x,y]= (255,255,255,255)
	return img

def get(image,x,y,G,N):
	L = image.getpixel((x,y))
	if L > G:
		L = True
	else:
		L = False
	nearDots = 0
	if L == (image.getpixel((x - 1,y - 1)) > G):
		nearDots += 1
	if L == (image.getpixel((x - 1,y)) > G):
		nearDots += 1
	if L == (image.getpixel((x - 1,y + 1)) > G):
		nearDots += 1
	if L == (image.getpixel((x,y + 1)) > G):
		nearDots += 1
	if L == (image.getpixel((x,y - 1)) > G):
		nearDots += 1
	if L == (image.getpixel((x + 1,y + 1)) > G):
		nearDots += 1
	if L == (image.getpixel((x + 1,y)) > G):
		nearDots += 1
	if L == (image.getpixel((x + 1,y - 1)) > G):
		nearDots += 1;
	if nearDots < N:
		return image.getpixel((x,y - 1))
	return None

#降噪
def clearNoise(image,G,N,Z):
	draw = ImageDraw.Draw(image)
	for i in xrange(0,Z):
		for x in xrange(1,image.size[0] - 1):
			for y in xrange(1,image.size[1] - 1):
				color = get(image,x,y,G,N)
				if color != None:
					draw.point((x,y),color)

def pre_handle(image_dir):
	start_time = time.time()
	image = Image.open(image_dir)
	image = image.convert("L")
	image = twopi(image).convert("L")
	clearNoise(image,100,1,6)
	end_time = time.time()
	print '验证码预处理完成，耗时%fs.'%(end_time - start_time)
	return image

if __name__ == '__main__':
	pre_handle('test_train/2a47.png')
