import cv2

while True:
    try:
        img = cv2.imread('../solution/images/Camera_1.png')
        cv2.imshow('Image', img)
    except: pass
    finally:
        if cv2.waitKey(1) == 27: break