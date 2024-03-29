import numpy as np
import argparse
import cv2
import datetime
import sys

class Image_Processing:

    def __init__(self, image_name, CAMX, CAMY):

        self.cX = CAMX/2
        self.cY = CAMY/2
        
        self.image_name = image_name
        image = cv2.imread(image_name)
        image = self.equalize_hist(image)
        
        # FInding binary regions of red
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, (0,50,20), (5,255,255))
        mask2 = cv2.inRange(hsv, (175,50,20), (180,255,255))
        mask = cv2.bitwise_or(mask1, mask2 ) # Important

        kernel = np.ones((5,5),np.uint8)
        mask = cv2.erode(mask,kernel,iterations = 1)

        # Find the biggest red region
        (cnts, _) = cv2.findContours(mask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        try:
            for cnt in cnts:
                if cv2.contourArea(cnt)<CAMX/5: # Don't count the noise
                    pass
                else:
                    c = max(cnts, key = cv2.contourArea)
                    res = np.mean(c, axis=0)
                    res = res[0]
                    self.cX = int(round(res[0]))
                    self.cY = int(round(res[1]))
        except : # Empty one
            self.cX = CAMX/2
            self.cY = CAMY/2
        
    # Equalizing the histogramm
    def equalize_hist(self, img):
        img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
        img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        return img

    def coord(self):
        return self.cX, self.cY
