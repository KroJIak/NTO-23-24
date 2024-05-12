from random import randint
import cv2 as cv
import numpy as np
img2 = np.zeros((720, 1280, 1))
img2 = cv.imread('rwadsdfewfwf.png' , cv.IMREAD_GRAYSCALE)
arr = []
n = int(input("кол-во кругов - "))
for i in range(n):
    cv.circle(img2,(randint(20  , img2.shape[1]-20),randint(20, img2.shape[0]-20)), 3, (255,255,255), -1)
_,thresh2 = cv.threshold(img2,127,255,cv.THRESH_BINARY)
contours, _ = cv.findContours(thresh2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
a = 0
arr =[]
for cnt in contours :
    arr.append(cv.contourArea(cnt))
area = min(arr)
print(arr)
print(area)
for cnt in contours :
    if cv.contourArea(cnt) > area:
        d = cv.contourArea(cnt)/area
        if d % 1 >= 0.5 :
            d = int(d) + 1 
        else :
            d = int(d)
        a+=d
    else :
        a+=1
    a = n
print(len(contours) , a)
while True:
    cv.imshow("dasd" , thresh2)
    cv.imshow("dasd12" , img2)


    if cv.waitKey(0) == 27:
        break