import cv2
import imutils
import numpy as np


#Global variables
bg = NONE
#Function - To find the running average over the background
def run_avg(image, aWeight):
	global bn
	#initialize background
	if bg is None:
		bg = image.copy()astype("float")
		return
	#Compute weighted average, accumulate it and update it
	cv2.accumulateWeighted(image, bg, aWeight)
