from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from math import sqrt

### SET THE FOLLOWING TO MATCH REQUIRMENTS

useCamera = False # use a webcam or attached camera
saveVideo = True # save the edited video
drawTrail = True # draw a trail behind the object
resizeVideo = True # resize the video (if saveVideo = True, this must match the width in outputDims)
video = "img/single_daphnia.MOV" # title of input video (required if useCamera = False) 
outputName = "output/vector_single_daphnia.avi" # name of output video (required if saveVideo = True)
outputDims = (640, 360) # resolution of output video (best to match that of input, required if saveVideo = True)
maxTrail = 6000 # maximum points to draw in the trail (required if drawTrail = True)
videoWidth = 640 # width for video resizing (required if resizeVideo = True)
savePos = False
#single_daphnia
hsvLow = (0, 46, 93) # the lower HSV colourspace bounds of the object
hsvHigh = (112, 255, 255) # the upper HSV colourspace bounds of the object
#hsvLow = (0, 34, 64) # the lower HSV colourspace bounds of the object
#hsvHigh = (57, 255, 141) # the upper HSV colourspace bounds of the object


###############################################

ap = argparse.ArgumentParser()
pts = deque(maxlen=maxTrail)

if savePos:
    f = open("positions.txt", "w")

if saveVideo:
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(outputName, fourcc, 20.0, outputDims)

if useCamera:
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(video)

t0 = -1
while True:
    (grabbed, frame) = camera.read()

    if not useCamera and not grabbed:
        break
    
    h, w = frame.shape[:2]
    if resizeVideo:
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
        #cv2.circle(frame, (int(x), int(y)), int(radius*0.75),(124, 252, 0), 2)
        cv2.circle(frame, center, 1, (0, 0, 255), -1)
    
    if radius > 5:
        pts.appendleft(center)
        t = camera.get(0)/1000.0
        if savePos:
            f.write("{} {} {}\n".format(center[0], h - center[1], t))
        if len(pts) > 1:
            dx = pts[0][0] - pts[1][0]
            dy = pts[0][1] - pts[1][1]
            dt = t - t0
            s = sqrt(dx*dx + dy*dy)/dt
            sx = dx/dt
            sy = dy/dt
            l = int(s/3)
            lx = int(sx/3)
            ly = int(sy/3)
            if s > 60:
                cv2.line(frame, center, (center[0] + lx, center[1] + ly), (255, 0, 255), 2)
                cv2.line(frame, center, (center[0] + lx, center[1]), (0, 0, 255), 2)
                cv2.line(frame, center, (center[0], center[1] + ly), (255, 0, 0), 2)
        t0 = t     
	
        if drawTrail:
            for i in xrange(1, len(pts)):
                if pts[i - 1] is None or pts[i] is None:
                    continue
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 1)
    
    cv2.imshow("Vectors", frame)
    
    if saveVideo:
        out.write(frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("q"):
        break

if savePos:
    f.close()

camera.release()
if saveVideo:
    out.release()
cv2.destroyAllWindows()