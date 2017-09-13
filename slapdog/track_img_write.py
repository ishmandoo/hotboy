import cv2
import numpy as np
import os

cap = cv2.VideoCapture(0)

def draw_circle(frame,x,y):
    cv2.circle(frame,(x,y),20,(255,0,0),2)
    #print frame[x,y]
#maxsGoodDir = "../photos/run1/"
#files = os.listdir(maxsGoodDir)

#print files
#for f in files:
while True:
    # Take each frame
    _, frame = cap.read()
    #frame = cv2.imread(maxsGoodDir + f, cv2.IMREAD_COLOR)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of color in HSV
    #lower_blue = np.array([50,50,50])
    #upper_blue = np.array([70,255,255])


    x = np.arange(frame.shape[1])
    y = np.arange(frame.shape[0])
    xv, yv = np.meshgrid(x, y, sparse=False)


    #currently set for orange frisbee
    lower_color = np.array([25,0,180])
    upper_color = np.array([65,255,255])
    # Threshold the HSV image to get only desired colors
    mask = cv2.inRange(hsv, lower_color, upper_color)

    N = np.sum(mask)
    if N >= 5 :
        xavg = np.sum( mask * xv) / N
        yavg = np.sum( mask * yv) / N
        print "x:" + str(xavg) + " y: " + str(yavg)
        draw_circle(frame, int(xavg), int(yavg))

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    cv2.imwrite("current_img.jpg",frame)

    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('res',frame)
    k = cv2.waitKey(1000) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
