# -*- encoding: utf-8 -*-
import cv2
import numpy as np
import math as mt
import matplotlib
from matplotlib import pyplot as plt


"""
Auxiliar functions to draw results in the inputs images.
"""

def draw_in_image(img,area,cnt,posicion):
	im = img.copy()
	cv2.drawContours(im, [cnt], 0, (0,255,0), 1)
	if area != 0:
		text = str(area)+' um2'
		font = cv2.FONT_HERSHEY_SIMPLEX
		im = draw_text(im,text,posicion)
	return im

def draw_text(img,text,position):
	x = position[0] - 40
	y = position[1]
	im = img.copy()
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.rectangle(im,(x,y-10),(x+70,y+5),(255,255,255),-1)
	cv2.putText(im,text,(x,y), font, 0.4,(0,0,0),1)
	return im

def __draw(im,title):
	plt.imshow(im,cmap = 'gray')
	plt.title(title), plt.xticks([]), plt.yticks([])
	plt.show()

def draw_image(im):
	plt.imshow(im,cmap = 'gray')
	plt.show()

def draw_image(im,title,subplot):
	if subplot:
		num = len(im)
		num2 = len(title)
		sr = mt.sqrt(num)
		if (int(sr) == sr):
			filas = int(sr)
			columnas = int(sr)
		elif num <= 3:
			filas = 1
			columnas = 3
		elif num <= 10:
			filas = 2
			columnas = num/2 +1
		elif num <= 20:
			filas = 4
			if num%4 == 0:
				columnas = num/4
			else:
				columnas = 5
		elif num <= 30:
			filas = 5
			columnas = 6
		elif num <= 40:
			filas = 5
			columnas = 8
		elif num <= 50:
			filas = 8
			columnas = 8
		else:
			if num%10 == 0:
				filas = num/10
			else:
				filas = num/10 + 1
			columnas = 10

		i = 0
		for imagen in im:
			plt.subplot(filas,columnas,i+1),plt.imshow(imagen,cmap='gray')
			plt.title(title[i]), plt.xticks([]), plt.yticks([])
			i += 1

	else:
		__draw(im,title)
	plt.show()
