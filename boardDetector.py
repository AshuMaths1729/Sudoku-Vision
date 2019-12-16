import getopt
import sys
import cv2 as cv
import numpy as np
import digitRecog
import solver

def detector():
	padding = 5

	def preprocessImg(image):
		gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
		ret,thresh = cv.threshold(gray,128,255,cv.THRESH_BINARY)
		outerBox = cv.bitwise_not(thresh)
		return outerBox

	def n10():
		img = np.zeros((50, 50, 3), np.uint8)*255
		img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
		roi = img[:,:]
		return roi

	def getRoi(box):
		_, contours, _ = cv.findContours(box, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
		for cnt in contours:
			[x,y,w,h] = cv.boundingRect(cnt)
			if(h > 15 and w > 5 and x > padding/2 and y > padding/2):
				roi = box[y:y+h,x:x+w]
				roi = cv.resize(roi,(50,50))
				roir = cv.rectangle(np.copy(box),(x,y),(x+w,y+h),(255,0,0),1)
				return roi
		return n10()

	def getBox(img, i, j): 
		height, width, channels = image.shape
		cellW = width // 9
		cellH = height // 9
		box = img[cellH*i + padding:cellH*(i+1) - padding, cellW*j + padding:cellW*(j+1) - padding]
		return box

	image = cv.imread('output.jpg')
	outerBox = preprocessImg(image)
	imgBoard = np.empty((0, 2500))
	for i in range(0, 9):
		for j in range(0, 9):
			box = getBox(outerBox, i,j)
			roi = getRoi(box)
			imgBoard = np.append(imgBoard, [roi.ravel()], axis=0)

	board = digitRecog.recogBoard(imgBoard)
	board = np.reshape(board, (-1, 9 if len(board) > 9 else len(board)))
	board = np.vectorize(lambda t: 0 if t == 10 else t)(board)
	#print("Fed Puzzle:\n",board)

	#find solution depend on board
	resBoard = np.copy(board)
	if(solver.solveSDKBoard(resBoard) == True):
		return resBoard
	else:
		return -1
"""
res = detector()
print("\nSolved Puzzle:\n",res.astype(int))
"""