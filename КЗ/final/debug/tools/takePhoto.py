import os

import cv2

def main():
    cap = cv2.VideoCapture(2)
    while True:
        _, img = cap.read()
        cv2.imshow('Camera', img)
        key = cv2.waitKey(1)
        match key:
            case 27: break
            case 32: cv2.imwrite(f"images/{len(os.listdir('images'))}.png", img)
        if cv2.waitKey(1) == 27: break

if __name__ == '__main__':
    main()