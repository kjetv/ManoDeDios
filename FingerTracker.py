import cv2
import imutils
import numpy as np
from enum import Enum

#Global variables
BACKGROUND = None

# Updates and displayes the finger positions
def FingerTracker():
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE,0.75) # 0.25 turns off, 0.75 turns on
    
    HandPerimiterTop, HandPerimiterRight, HandPerimiterBottom, HandPerimiterLeft = 10, 350, 350, 650

    aWeight = 0.5
    num_frames = 0

    while(True):
        (grabbed, mainFrame) = camera.read()
        mainFrame = imutils.resize(mainFrame, width=700)
        mainFrame = cv2.flip(mainFrame, 1)
        (height, width) = mainFrame.shape[:2]

        HandRegion = mainFrame[HandPerimiterTop:HandPerimiterBottom, HandPerimiterRight:HandPerimiterLeft]
        HandRegion = cv2.cvtColor(HandRegion, cv2.COLOR_BGR2GRAY)
        HandRegion = cv2.GaussianBlur(HandRegion, (5, 5), 0)
        cv2.rectangle(mainFrame, (HandPerimiterLeft, HandPerimiterTop), (HandPerimiterRight, HandPerimiterBottom), (0,255,0), 2)

        if num_frames < 30:
            backgroundAveraging(HandRegion, aWeight)
            num_frames += 1
        else:
            hand = segment(HandRegion)
            if hand is not None:
                (thresholded, segmented, center, radius) = hand
                cv2.imshow("Thesholded", thresholded)
                center = (center[0]+HandPerimiterRight,center[1]+HandPerimiterTop)
                cv2.drawContours(mainFrame, [segmented + (HandPerimiterRight, HandPerimiterTop)], -1, (0, 0, 255))
                cv2.circle(mainFrame, center, radius, (255,0,0), 2)
        
        cv2.imshow("Video Feed", mainFrame)

        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


# ---------------------------Local functions-------------------------------------------

# Find the running average over the background or initialize it 
def backgroundAveraging(image, aWeight):
    global BACKGROUND
    if BACKGROUND is None:
        BACKGROUND = image.copy().astype("float")
        return
    cv2.accumulateWeighted(image, BACKGROUND, aWeight)

# Segment the region of hand in the image
def segment(image, threshold=12):
    global BACKGROUND
    # find the absolute difference between background and current mainFrame
    diff = cv2.absdiff(BACKGROUND.astype("uint8"), image)

    # threshold the diff image so that we get the foreground
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

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
    _,cnts,_ = cv2.findContours(thresholded.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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

