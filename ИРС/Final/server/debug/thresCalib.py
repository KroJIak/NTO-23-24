from cv2 import createTrackbar, getTrackbarPos
import cv2
from camera import Camera
import numpy as np

def nothing(*arg): pass

def showImage(img, winName='Image'):
    while cv2.waitKey(1) != 27: cv2.imshow(winName, img)

def getUndistortedImage(img, mtx, dist):
    h, w = img.shape[:2]
    newCameraMtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    dst = cv2.undistort(img, mtx, dist, None, newCameraMtx)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

def rotateImage(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def getFullScene(leftImg, rightImg):
    k = 0.8035
    rightImg = cv2.resize(rightImg, (int(rightImg.shape[1] * k), int(rightImg.shape[0] * k)))
    offsetCenter = -40
    leftImg = leftImg[68 + offsetCenter:]
    rightImg = rightImg[:-150 + offsetCenter, 9:861]
    resImg = np.concatenate((rightImg, leftImg), axis=0)
    resImg = rotateImage(resImg, 1.2)
    resImg = resImg[37:-37, 208:-93]
    resImg = cv2.rotate(resImg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return resImg

def createBars():
    cv2.namedWindow('buttons')
    createTrackbar('blockSize', 'buttons', 3, 255, nothing)
    createTrackbar('C', 'buttons', 0, 255, nothing)
    createTrackbar('sizeBlur', 'buttons', 1, 15, nothing)

def getBars():
    blockSize = getTrackbarPos('blockSize', 'buttons')
    C = getTrackbarPos('C', 'buttons')
    sizeBlur = getTrackbarPos('sizeBlur', 'buttons')
    blockSize = max(3, blockSize // 2 * 2 + 1)
    sizeBlur = max(1, sizeBlur)
    return blockSize, C, sizeBlur

def getBinaryImage(img, blockSize, C, sizeBlur):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBinary = cv2.adaptiveThreshold(imgGray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, blockSize, C)
    imgBinary = cv2.blur(imgBinary, (sizeBlur, sizeBlur))
    return imgBinary

matrix1=[[951.6447409, 0., 601.28670737],
       [0., 952.68412683, 464.89843992],
       [0., 0., 1.]]
distortion1=[[-0.45733346, 0.2497311, -0.00263185, -0.00254355, -0.07533089]]
matrix2=[[920.91593381, 0., 647.37763074],
       [0., 921.31953503, 401.63905933],
       [0., 0., 1.]]
distortion2=[[-0.30131843, 0.11964215, 0.00164663, -0.00087653, -0.02382259]]

class cammm:
    def read(self):
        return cv2.imread('Camera.png')

def main():
    camera = cammm()
    createBars()
    cap1 = cv2.VideoCapture('http://student:nto2024@10.128.73.31/mjpg/video.mjpg')
    cap2 = cv2.VideoCapture('http://student:nto2024@10.128.73.38/mjpg/video.mjpg')
    while True:
        _, m1 = cap1.read()
        _, m2 = cap2.read()
        img = getFullScene(getUndistortedImage(m2, matrix2, distortion2), getUndistortedImage(m1, matrix1, distortion1))
        showImage(img)
        blockSize, C, sizeBlur = getBars()
        imgBinary = getBinaryImage(img, blockSize, C, sizeBlur)
        imgCross = cv2.bitwise_and(img, img, mask=imgBinary)
        imgBinary = cv2.cvtColor(imgBinary, cv2.COLOR_GRAY2BGR)
        imgShow = np.concatenate((img, imgBinary, imgCross), axis=1)
        cv2.imshow('Calib', imgShow)
        if cv2.waitKey(1) == 27: break
    img = camera.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    showImage(imgGray)
    print(f'blockSize={blockSize}, C={C}, sizeBlur={sizeBlur}')
    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()