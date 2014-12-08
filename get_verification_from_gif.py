#!/usr/bin/python
# -*- coding:utf-8 -*-

import os  
from PIL import Image,ImageSequence 
   
   
''''' 
I searched high and low for solutions to the "extract animated GIF frames in Python" 
problem, and after much trial and error came up with the following solution based 
on several partial examples around the web (mostly Stack Overflow). 
  
There are two pitfalls that aren't often mentioned when dealing with animated GIFs - 
firstly that some files feature per-frame local palettes while some have one global 
palette for all frames, and secondly that some GIFs replace the entire image with 
each new frame ('full' mode in the code below), and some only update a specific 
region ('partial'). 
  
This code deals with both those cases by examining the palette and redraw 
instructions of each frame. In the latter case this requires a preliminary (usually 
partial) iteration of the frames before processing, since the redraw mode needs to 
be consistently applied across all frames. I found a couple of examples of 
partial-mode GIFs containing the occasional full-frame redraw, which would result 
in bad renders of those frames if the mode assessment was only done on a 
single-frame basis. 
  
Nov 2012 
'''  
   
   
def analyseImage(path):  
    ''''' 
    Pre-process pass over the image to determine the mode (full or additive). 
    Necessary as assessing single frames isn't reliable. Need to know the mode  
    before processing all frames. 
    '''  
    im = Image.open(path)  
    results = {  
        'size': im.size,  
        'mode': 'full',  
    }  
    try:  
        while True:  
            if im.tile:  
                tile = im.tile[0]  
                update_region = tile[1]  
                update_region_dimensions = update_region[2:]  
                if update_region_dimensions != im.size:  
                    results['mode'] = 'partial'  
                    break  
            im.seek(im.tell() + 1)  
    except EOFError:  
        pass  
    return results  
   
   
def processImage(path, frame_index, out_file):  
    ''''' 
    Iterate the GIF, extracting each frame. 
    '''  
    mode = analyseImage(path)['mode']  
      
    im = Image.open(path)  
   
    i = 0  
    p = im.getpalette()  
    last_frame = im.convert('RGBA')  
      
    try:  
        while True:  
            if i == frame_index:
                print "saving %s (%s) frame %d, %s %s" % (path, mode, i, im.size, im.tile)  
                  
                ''''' 
                If the GIF uses local colour tables, each frame will have its own palette. 
                If not, we need to apply the global palette to the new frame. 
                '''  
                if not im.getpalette():  
                    im.putpalette(p)  
                  
                new_frame = Image.new('RGBA', im.size)  
                  
                ''''' 
                Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image? 
                If so, we need to construct the new frame by pasting it on top of the preceding frames. 
                '''  
                if mode == 'partial':  
                    new_frame.paste(last_frame)  
                  
                new_frame.paste(im, (0,0), im.convert('RGBA'))  
                new_frame.save(out_file, 'PNG')  
       
                last_frame = new_frame

            i += 1  
            im.seek(im.tell() + 1)  
    except EOFError:  
        pass  
    return image.open(out_file)


def get_verification_frame(path):
    im = Image.open(path)
    frame_index = 0
    frame_duration = 0
    for i, frame in enumerate(ImageSequence.Iterator(im)):
        if frame.info['duration'] > frame_duration:
            frame_duration = frame.info['duration']
            frame_index = i
    print frame_index, frame_duration 
    return frame_index

def pre_handle_for_jifeng(path):
    frame_index = get_verification_frame(file_path) 
    name = gif_file.split('.')[0]
    out_file =  out_path + name + '.png'
    return processImage(file_path, frame_index, out_file)

#提取训练数据
if __name__ == '__main__':
    path = "jifeng_train_gif/"
    out_path = "jifeng_train_image/"
    sum = 0
    for gif_file in os.listdir(path):
        file_path = path + gif_file
        frame_index = get_verification_frame(file_path) 
        name = gif_file.split('.')[0]
        out_file =  out_path + name + '.png'
        processImage(file_path, frame_index, out_file)
