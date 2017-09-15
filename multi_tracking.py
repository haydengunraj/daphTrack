from collections import deque
import numpy as np
import argparse
import imutils
import cv2

### SET THE FOLLOWING TO MATCH REQUIRMENTS

useCamera = False # use a webcam or attached camera
saveVideo = True # save the edited video
resizeVideo = True # resize the video (if saveVideo = True, this must match the width in outputDims)
video = "img/copepods.mov" # title of input video (required if useCamera = False) 
outputName = "output/test.avi" # name of output video (required if saveVideo = True)
outputDims = (640, 360) # resolution of output video (best to match that of input, required if saveVideo = True)
videoWidth = 640 # width for video resizing (required if resizeVideo = True)
hsvLower = (0, 51, 57) # the lower HSV colourspace bounds of the object
hsvUpper = (48, 229, 181) # the upper HSV colourspace bounds of the object


###############################################

if saveVideo:
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(outputName, fourcc, 20.0, outputDims)

if useCamera:
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(video)

while True:
    (grabbed, frame) = camera.read()

    if not useCamera and not grabbed:
        break
    
    if resizeVideo:
        h, w = frame.shape[:2]
        frame = cv2.resize(frame, (videoWidth, int(float(videoWidth)/w*h)))
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, hsvLower, hsvUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 4 and radius < 20:
                cv2.circle(frame, (int(x), int(y)), int(radius*1.5),(0, 255, 255), 2)
                cv2.circle(frame, center, 2, (0, 0, 255), -1)
 
	cv2.imshow("Frame", frame)
	
    if saveVideo:
        out.write(frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
		break

camera.release()
if saveVideo:
    out.release()
cv2.destroyAllWindows()