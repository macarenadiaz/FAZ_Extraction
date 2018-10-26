# -*- encoding: utf-8 -*-
import cv2
import drawfaz as draw
import numpy as np
from skimage.morphology import skeletonize
from util import *


def detectFAZ(imOCTorig, mm, prof, precision):
	"""
	Function that extract and measure the FAZ with a OCT-A image as input.

	inputs:
		- imOCTorig: original OCT-A image (input image)
		- mm: millimeters of the input image (3 or 6 mm)
		- prof: deep or superficial image (1 or 0)
		- precision: a value between 0 and 1 to select the precision of the method
	"""
	size = imOCTorig.shape
	imOCT = np.zeros((size[0],size[1]),np.float64)
	if (len(size) > 2):
		imOCT[:,:] = imOCTorig[:,:,0] / float(imOCTorig.max())
	else:
		imOCT[:,:] = imOCTorig / float(imOCTorig.max())

	# tophat
	ss = ((size[0]/80)*2-mm+3)
	ss = ss*2-1
	imOCT = morph('tophat',imOCT,ss)

	# canny edge detector
	edges, imClosed = edges_extraction (imOCT,prof,mm,precision)

	im = imClosed.copy()
	# mask of the FAZ
	fazMask = find_mask(im,prof,mm)

	# select the highest candidate
	image = fazMask.copy()
	image1 = cv2.convertScaleAbs(image) 
	_,contours, h = cv2.findContours(image1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cogidos = []
	cnt,cogidos = higest_contour (contours, cogidos)
	m = cv2.contourArea(cnt)
	fazAreainMM = m*(mm*mm)/(size[0]*size[1])

	im = np.zeros((size[0],size[1]), np.uint8)
	cv2.drawContours(im, [cnt], 0, (255,255,255), -1)
	im = im[:]/255
	
	# make region growing
	
	reg = region_growing(imOCT, im*1.0, fazAreainMM, prof, 4, precision)

	reg = morph ('open', reg, 3)
	reg = morph ('closed', reg, 3)
	image1 = cv2.convertScaleAbs(reg) 
	_, contours, h = cv2.findContours(image1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cogidos = []
	cnt,cogidos = higest_contour (contours, cogidos)

	m = cv2.contourArea(cnt)
	fazAreainMM = m*(mm*mm)/(size[0]*size[1])

	octLabel = np.zeros((size[0],size[1],3))
	octLabel[:,:,0] = imOCT*(1-(reg*0.5)) + reg*0.5
	octLabel[:,:,1] = imOCT*(1-(reg*0.3)) + reg*0.35
	octLabel[:,:,2] = imOCT*(1-reg)
	im = reg[:]
	faz =  im[:]

	fazAreainUM = fazAreainMM * 1000
	fazAreainUM = float("{0:.2f}".format(fazAreainUM))
	M = cv2.moments(cnt)
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	imOCT_area = draw.draw_in_image(imOCTorig, fazAreainUM, cnt, (50,50))
	im_cnt = draw.draw_in_image(imOCTorig, 0, cnt, None)

	return faz, fazAreainMM, cnt
