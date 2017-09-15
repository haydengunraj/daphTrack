from collections import deque
import numpy as np
import argparse
import imutils
import cv2

### SET THE FOLLOWING TO MATCH REQUIRMENTS

useCamera = False # use a webcam or attached camera
saveVideo = True # save the edited video
drawTrail = True # draw a trail behind the object
resizeVideo = True # resize the video (if saveVideo = True, this must match the width in outputDims)
video = "img/tiny_daphnia.MOV" # title of input video (required if useCamera = False) 
outputName = "output/test2.avi" # name of output video (required if saveVideo = True)
outputDims = (640, 426) # resolution of output video (best to match that of input, required if saveVideo = True)
maxTrail = 6000 # maximum points to draw in the trail (required if drawTrail = True)
videoWidth = 640 # width for video resizing (required if resizeVideo = True)
hsvLow = (0, 34, 64) # the lower HSV colourspace bounds of the object
hsvHigh = (57, 255, 141) # the upper HSV colourspace bounds of the object


###############################################

ap = argparse.ArgumentParser()
pts = deque(maxlen=maxTrail)

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
    mask = cv2.inRange(hsv, hsvLow, hsvHigh)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
	
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 255), 2)
        cv2.circle(frame, center, 1, (0, 0, 255), -1)
    
    if radius > 5:
	    pts.appendleft(center)
	
    for i in xrange(1, len(pts)):
		if pts[i - 1] is None or pts[i] is None:
			continue
		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 3)
    
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