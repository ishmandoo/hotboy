import cv2
import numpy as np

def nothing(x):
    pass

color = np.array([100,0,245])

def use_color(event,x,y,flags,param):
    global hsv, color,frame
    if event == cv2.EVENT_LBUTTONDOWN:

        mycolor = np.uint8([[cv2.pyrDown(frame)[y,x]]])
        print mycolor
        color = cv2.cvtColor(mycolor, cv2.COLOR_BGR2HSV)
        print "yo"
        print color

cap = cv2.VideoCapture(0)
cv2.namedWindow('image')
cv2.createTrackbar('H','image',10,127,nothing)
cv2.createTrackbar('S','image',30,127,nothing)
cv2.createTrackbar('V','image',100,127,nothing)
cv2.createTrackbar('Erode','image',1,10,nothing)
cv2.createTrackbar('Dilate','image',4,10,nothing)
cv2.setMouseCallback('image',use_color)


while(1):

    # Take each frame
    h = cv2.getTrackbarPos('H','image')
    s = cv2.getTrackbarPos('S','image')
    v = cv2.getTrackbarPos('V','image')


    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_color = color - np.array([h, s, v])
    upper_color = color + np.array([h, s, v])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((5,5),np.uint8)
    erode = cv2.getTrackbarPos('Erode','image')
    dilate = cv2.getTrackbarPos('Dilate','image')

    erosion = cv2.erode(mask,kernel,iterations = erode)
    dilation = cv2.dilate(erosion,kernel,iterations = dilate)
    if dilate > erode:
        finalmask = cv2.erode(dilation,kernel,iterations = dilate - erode)
    elif  dilate < erode:
        finalmask = cv2.dilate(dilation,kernel,iterations = erode - dilate)
    else:
        finalmask = dilation

    #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    cv2.imshow('mask',cv2.pyrDown(finalmask))

    contours,hierarchy= cv2.findContours(finalmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        maxarea = 0
        maxcnt = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > maxarea:
                maxarea = area
                maxcnt = cnt
        cv2.drawContours(frame, [maxcnt], -1, (0,0,255), 3)
        '''
        # draw rotated rectangle
        rect = cv2.minAreaRect(maxcnt)
        box = cv2.cv.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(img,[box],0,(0,255,0),2)
        '''
        x,y,w,h = cv2.boundingRect(maxcnt)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    #edges = cv2.Canny(gray,minval,maxval)
    cv2.imshow('image',cv2.pyrDown(frame))
    #cv2.imshow('mask',cv2.pyrDown(finalmask))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
