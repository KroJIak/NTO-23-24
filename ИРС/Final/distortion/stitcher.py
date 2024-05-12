import cv2

mode = cv2.STITCHER_PANORAMA
img1 = cv2.imread('../Camera_0.png')
img2 = cv2.imread('../Camera_1.png')
#img1 = cv2.rotate(img1, cv2.ROTATE_90_CLOCKWISE)
#img2 = cv2.rotate(img2, cv2.ROTATE_90_CLOCKWISE)
#img2 = img2[:, img2.shape[1]//15:]

'''images1 = []
for j in range(0, img1.shape[1], step):
    images1.append(img1[:, max(0, j-step//2):min(j+step, img1.shape[1]-1), :])
    cv2.imshow('Image', img1[:, max(0, j-step//2):min(j+step, img1.shape[1]-1), :])
    cv2.waitKey(10000)'''



def main():
    stitcher = cv2.Stitcher().create(mode)

    cv2.imshow('Image1', img1)
    cv2.imshow('Image2', img2)
    cv2.waitKey(10000)
    status, pano = stitcher.stitch([img1, img2])
    pano = cv2.rotate(pano, cv2.ROTATE_90_CLOCKWISE)

    while cv2.waitKey(1) != 27:
        cv2.imshow("Result", pano)

cv2.SIFT().create()
if __name__ == "__main__":
    main()
