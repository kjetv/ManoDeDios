import cv2
import imutils
import numpy as np


#Global variables
BACKGROUND = None

#------------------------------------------------------------------------------
#Function - To find the running average over the background
#------------------------------------------------------------------------------
def run_avg(image, aWeight):
	global BACKGROUND
	#initialize background
	if BACKGROUND is None:
		BACKGROUND = image.copy().astype("float")
		return
	#Compute weighted average, accumulate it and update it
	cv2.accumulateWeighted(image, BACKGROUND, aWeight)

#-------------------------------------------------------------------------------
# Function - To segment the region of hand in the image
#-------------------------------------------------------------------------------
def segment(image, threshold=12):
    global BACKGROUND
    # find the absolute difference between background and current frame
    diff = cv2.absdiff(BACKGROUND.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff,
                                threshold,
                                255,
                                cv2.THRESH_BINARY)[1]

    

    #-------------- My own touch-------------------------------
   
    ## Copy the thresholded image.
    im_floodfill = thresholded.copy()
	 
	# Mask used to flood filling.
	# Notice the size needs to be 2 pixels than the image.
    h, w = thresholded.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
	 
	# Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (0,0), 255);
	 
	# Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
	 
	# Combine the two images to get the foreground.
    thresholded = thresholded | im_floodfill_inv
   
 	#---------------------------------------------------------



    # get the contours in the thresholded image
    _,cnts,_ = cv2.findContours(thresholded.copy(),
                                    cv2.RETR_LIST,
                                    cv2.CHAIN_APPROX_SIMPLE)
    


    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        epsilon = 0.01*cv2.arcLength(segmented,True)
        approx = cv2.approxPolyDP(segmented,epsilon,True)


        cnt = approx
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        out = cv2.linearPolar(thresholded, center, 100, cv2.INTER_LINEAR+cv2.WARP_FILL_OUTLIERS)
        print(radius)
        return (out, approx, center, radius)

#-------------------------------------------------------------------------------
# Main function
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    # initialize weight for running average
    aWeight = 0.5

    # get the reference to the webcam
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE,0.75)
    #camera.set(cv2.CAP_PROP_EXPOSURE, 1.0)
    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 350, 650

    # initialize num of frames
    num_frames = 0

    # keep looping, until interrupted
    while(True):
        # get the current frame
        (grabbed, frame) = camera.read()

        # resize the frame
        frame = imutils.resize(frame, width=700)

        # flip the frame so that it is not the mirror view
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI
        roi = frame[top:bottom, right:left]

        # convert the roi to grayscale and blur it
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        # to get the background, keep looking till a threshold is reached
        # so that our running average model gets calibrated
        if num_frames < 30:
            run_avg(gray, aWeight)
        else:
            # segment the hand region
            hand = segment(gray)

            # check whether hand region is segmented
            if hand is not None:
                # if yes, unpack the thresholded image and
                # segmented region
                (thresholded, segmented, center, radius) = hand

                # draw the segmented region and display the frame
                cen = (center[0]+right,center[1]+top)
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.circle(clone, cen, radius, (255,0,0), 2)
                cv2.imshow("Thesholded", thresholded)

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        # increment the number of frames
        num_frames += 1

        # display the frame with segmented hand
        cv2.imshow("Video Feed", clone)

        # observe the keypress by the user
        keypress = cv2.waitKey(1) & 0xFF

        # if the user pressed "q", then stop looping
        if keypress == ord("q"):
            break

# free up memory
camera.release()
cv2.destroyAllWindows()
