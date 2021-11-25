import numpy as np
import cv2
from collections import deque
import os, sys
import cPickle
import gzip
from PIL import Image


def draw(pts):
	img=np.zeros((640,1000), np.uint8)
	for i in np.arange(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue
		else:
			cv2.line(img,pts[i-1], pts[i] , (255,255,255),  13)
	while True:
		cv2.imshow('spell',img)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("p"):
			break	
# Coordinates of non-black pixels.
	coords = np.argwhere(img>0)
# Bounding box of non-black pixels.
	x0, y0 = coords.min(axis=0)-50
	x1, y1 = coords.max(axis=0)+50   # slices are exclusive at the top
# Get the contents of the bounding box.
	img = img[x0:x1, y0:y1]
	img = Image.fromarray(img)
	img = img.resize((28,28), Image.ANTIALIAS)
	a = np.array(img)
	while True:
		cv2.imshow('spell2',a)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("p"):
			break

	b = [np.reshape(a, (784, 1))]
	b=np.asarray(b)
	print type(b)
	c = [1]
	d=zip(b,c)
	
	return d

			
	
	
