import cv2
import numpy as np


def drawCircle(frame,x,y):
    cv2.circle(frame,(x,y),20,(255,0,0),2)

def findTarget(frame, show_img=False):
    """Finds the frisbee target in an image

    Identifies the frisbee in the image and returns the pixel location as a tuple

    Args:
        img: An opencv color image

    Returns:
        Either a tuple with the x and y pixel location in the image or None, if no frisbee is found

    """


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    x = np.arange(frame.shape[1])
    y = np.arange(frame.shape[0])
    xv, yv = np.meshgrid(x, y, sparse=False)

    # Color requirements, with lower and upper bounds for Hue, Saturation, and Vibrance
    # Currently set for the orange frisbee on grass from the PI camera
    lower_color = np.array([25,0,180])
    upper_color = np.array([65,255,255])

    # Threshold the HSV image to get only desired colors
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Find the number of pixels meeting the color requirements
    # If it meets the threashold, find the average position
    N = np.sum(mask)
    if N >= 5:
        xavg = np.sum( mask * xv) / N
        yavg = np.sum( mask * yv) / N
        print "x:" + str(xavg) + " y: " + str(yavg)
        draw_circle(frame, int(xavg), int(yavg))
        return (avgx, avgy)

    return None
