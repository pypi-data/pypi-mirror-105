#!/usr/bin/env python
# encoding=utf-8
import os
from PIL import Image
def generateImg():
    print("Enter image path: ")
    imgName = input()    
    if imgName[-1] == ' ':
        imgName = imgName[:-1]
    img = Image.open(imgName)
    strArray = imgName.split('.', 1)
    imgPrefix = strArray[0]
    if imgName.endswith('jpg'):
        newImgName =imgPrefix  + '.png'
        img.save(newImgName)
    else:
        newImgName = imgName
    img = Image.open(newImgName)
    img = img.convert('RGBA')  
    pixel_data = img.load()
    width, height = img.size 
    for h in range(height):
        for w in range(width):
            pixel = pixel_data[w, h]
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            a = pixel[3]
            if r > 220 and g > 220 and b > 220 and a > 220:
                pixel_data[w, h] = (255, 255, 255, 0)
    img.save(newImgName) 
    
    fileTwo = imgPrefix+"@2x.png"
    fileThree = imgPrefix+"@3x.png"
    img = Image.open(newImgName)
    img = img.resize((120,120),Image.ANTIALIAS);
    img.save(fileTwo) 
    img = Image.open(newImgName)
    img  = img.resize((180,180),Image.ANTIALIAS);
    img.save(fileThree) 