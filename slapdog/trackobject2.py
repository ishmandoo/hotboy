import cv2
import numpy as np

cap = cv2.VideoCapture(0)


# mouse callback function
def draw_circle(event,x,y,flags,param):
    global frame
    if event == cv2.EVENT_LBUTTONDOWN:
        #cv2.circle(img,(x,y),100,(255,0,0),-1)
        #print frame[x,y]
        print "yo"

# Create a black image, a window and bind the function to window
#img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('mask')
cv2.setMouseCallback('mask',draw_circle)

# Take each frame
_, frame = cap.read()

frame = cv2.resize(frame,None,fx=.25, fy=.25, interpolation = cv2.INTER_CUBIC)

print frame.shape

x = np.arange(frame.shape[1])
y = np.arange(frame.shape[0])
xv, yv = np.meshgrid(x, y, sparse=False)

while(1):

    # Take each frame
    _, frame = cap.read()

    frame = cv2.resize(frame,None,fx=.25, fy=.25, interpolation = cv2.INTER_CUBIC)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #hsv = cv2.resize(hsv,None,fx=.25, fy=.25, interpolation = cv2.INTER_CUBIC)
    #small = cv2.pyrDown(hsv)
    # define range of blue color in HSV
    lower_blue = np.array([50,50,50])
    upper_blue = np.array([70,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    N = np.sum(mask)
    if N >= 30 :
        xavg = np.sum( mask * xv) / N
        yavg = np.sum( mask * yv) / N
        print "x:" + str(xavg) + " y: " + str(yavg)
    #cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    #cv2.imshow('res',mask)
    k = cv2.waitKey(100) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
