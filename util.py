# -*- encoding: utf-8 -*-
import cv2
import numpy as np


def canny (im,t1,t2,gamma):
	"""
	This function simplifies the use
	of canny edge detector

	inputs:
		- im: OCT-A image
		- t1 and t2:  thresholds of canny edge detector
		- gamma: gamma parameter to canny edge detector
	"""
	im2 = im.copy()
	edges = cv2.GaussianBlur(im2, (15,15),gamma)
	edges = cv2.normalize(edges,edges,0,255,cv2.NORM_MINMAX)
	edges = cv2.Canny(np.uint8(edges),t1,t2)
	return edges

def morph (op,im,eesize):
	"""
	This function return the application of the
	morphological operator that we select

	inputs:
		- op: morphological operator 
			+ 'closed'
			+ 'open'
			+ 'tophat'
			+ 'dilate'
			+ 'erode'
		- im: input image
		- eesize: half size of the estructural element  

	"""
	if (op == 'closed'):
		imClosed = im.copy()
		se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(eesize,eesize))
		imClosed = cv2.morphologyEx(imClosed, cv2.MORPH_CLOSE, se)
		return imClosed
	elif (op == 'open'):
		imOpen = im.copy()
		se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(eesize,eesize))
		imOpen = cv2.morphologyEx(imOpen, cv2.MORPH_OPEN, se)
		return imOpen
	elif (op == 'tophat'):
		th = im.copy()
		se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(eesize,eesize))
		th = cv2.morphologyEx(th, cv2.MORPH_TOPHAT, se)
		return th
	elif (op == 'dilate'):
		dil = im.copy()
		se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(eesize,eesize))
		dil = cv2.dilate((dil *1.0).astype(np.float32),se)
		return dil
	elif (op == 'erode'):
		er = im.copy()
		se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(eesize,eesize))
		er = cv2.erode((er *1.0).astype(np.float32),se)
		return er

def media(img):
	"""
	This function calculates the average value
	of the pixel of the input image.

	input:
		- image
	"""
	size = img.shape
	sume = 0
	dim = size[0]*size[1]
	for i in range(size[0]):
		for j in range(size[1]):
			sume += img[i,j]
	return sume/dim

def edges_extraction (im,prof,mm,precision):
	"""
	This function is used to extract the edges of
	the OCT-A image

	inputs:
		- im: input image to detect the edges
		- prof: deep of the image (1 or 0)
		- mm: millimeters of the image (3 or 6)
		- pecision: a value between 0 and 1 to select the precision of the method
	"""
	size = im.shape
	if prof:
		# canny
		m = media(im)
		m = m*255
		edges = canny(im,0,m+m*0.2*precision,2)
		# closed
		ss = max(((size[0]/100)-3),3)
		ss = ss*2
		imClosed = morph('closed',edges,ss)

	else:
		# canny
		m = media(im)
		m = m*255
		if mm == 6:
			edges = canny(im,0,m+m*0.8*precision,1.9)
		edges = canny(im,0,m+m*0.3*precision,1.9)
		# closed
		ss = (size[0]/100)-3
		if ss<3:
			ss =3
		ss = ss*2
		imClosed = morph('closed',edges,ss)
	im = imClosed.copy()
	return edges, im



def find_mask(im,prof,mm):
	"""
	This function is used to select the correct mask to
	identify the correct FAZ in de OCT-A image

	inputs:
		- im: input image to detect the edges
		- prof: deep of the image (1 or 0)
		- mm: millimeters of the image (3 or 6)
	"""
	thresh = 45
	size = im.shape
	fazMask = np.zeros((size[0],size[1]))
	for i in range(size[0]):
		for j in range(size[1]):
			if im[i,j] < thresh:
				fazMask[i,j] = 1

	if mm == 6:
		fazMask1 = morph('open', fazMask, 5)
		fazMask1 = morph('closed', fazMask1, 5)
		fazMask1 = morph('open', fazMask, 5)
	else:
		fazMask1 = morph('open', fazMask,10)
		fazMask1 = morph('closed', fazMask1, 10)
		fazMask1 = morph('open', fazMask, 10)

	aux = np.zeros((size[0],size[1]))
	aux[:,:] = 0
	x = size[0]/4
	y = size[1]/4

	for i in range(x,size[0]-x):
		for j in range(y,size[1]-y):
			aux[i,j]=fazMask1[i,j]

	fazMask = aux[:]
	return fazMask.copy()

def higest_contour (contours,cogidos):
	"""
	This function returns the higest contour in a list
	of contours

	inputs:
		- contours: list of contours
		- cogidos: number of elements that where taken
	"""
	s = len(contours)
	sizes = np.zeros(s)
	minisizes = np.zeros(s)
	for i in range(s):
		sizes[i] = cv2.contourArea(contours[i])
	if len(sizes) == 0:
		return None,None
	sord = sorted(sizes)
	m = sord[len(sizes)-len(cogidos)-1]

	for i in range(len(contours)):
		if sizes[i] == m:
			mayor = i 
			cogidos.append(i)
	cnt = contours[mayor]
	return cnt,cogidos


def expand(elemento,reg,imOr,th,precision,conn):
	"""
	Auxiliar function to the region growing approach
	given a region and a pixel (of the contour) expand it 
	until stop criterion is reach

	inputs:
		- elemento:	pixel
		- reg: region that we want to segemnt
		- imOr: the image where we make the region growing
		- th: threshold
		- precision: a value between 0 and 1 to select the precision of the method
		- conn: connectivity (4 or 8)
	"""
	reg1 = reg.copy()
	y = elemento[0,0]
	x = elemento[0,1]
	if conn == 8:
		coor = [[x-1,y-1],[x-1,y],[x-1,y+1],[x,y-1],[x,y+1],[x+1,y-1],[x+1,y],[x+1,y+1]]
	else:
		coor = [[x-1,y],[x,y-1],[x,y+1],[x+1,y]]
	for elemento in coor:
		x = elemento[0]
		y = elemento[1]
		if (x<reg.shape[0]) and (y<reg.shape[1]) and (x>0) and (y>0) and (imOr[x,y] < th + 0.05*precision) and (reg[x,y] != 1):
			reg1[x,y] = 1

	return reg1

def contar (im,value):
	"""
	This function count the number of pixels that 
	have the value "value" in the image "im"

	inputs:
		- im: input image 
		- value: pixel value that we want to count in the image
	"""
	cont = 0
	for i in range(im.shape[0]):
		for j in range(im.shape[1]):
			if im[i,j] == value:
				cont += 1
	return cont

def region_growing(imOr,reg,area,prof,conn,precision):
	"""
	Implementation of a region growing approach where the
	pixels could be deleted of the region if they don't
	satisfy the stop criterion

	inputs:
		- imOr: original image
		- reg: initial region
		- area: area of the region
		- prof: deep of the image (1 or 0)
		- conn: connectivity (4 or 8)
		- precision: a value between 0 and 1 to select the precision of the method
	"""
	if prof:
		if area > 0.085:
			reg1 = morph('erode',reg,25)
			if reg1.max() == 1.0:
				reg = reg1
			else:
				reg1 = morph('erode',reg,15)
				if reg1.max() == 1.0:
					reg = reg1
	else:
		if area > 0.15:
			reg1 = morph('erode',reg,15)
			if reg1.max() == 1.0:
				reg = reg1

	elementos = contar (reg,1)
	seguir = True
	while seguir:
		reg = cv2.convertScaleAbs(reg)
		_,contours, h = cv2.findContours(reg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		reg[reg != 0] = 1
		media_region = sum(imOr[reg==1])/max(cv2.contourArea(contours[0]),0.001)

		for elemento in contours[0]:
			if prof:
				reg = expand(elemento,reg,imOr,media_region,precision/2,conn)
			else:
				reg = expand(elemento,reg,imOr,media_region,precision,conn)
		elementos_nuevo = contar (reg,1)
		if elementos == elementos_nuevo:
			seguir = False
		elementos = elementos_nuevo
	se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	reg = cv2.dilate(reg.astype(np.float32),se,iterations = 3)
	se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
	reg = cv2.erode(reg.astype(np.float32),se,iterations = 2)

	return reg