from imageFolding import kernelHorizontalSobel
import torch
from torch.nn.functional import conv2d
import cv2
from matplotlib import pyplot as plt

def main():
    img = cv2.imread('image.png')
    imgTensor = torch.tensor(img, dtype=torch.float)
    imgTensor = imgTensor.permute(2, 0, 1).unsqueeze(0)

    kernel = [[kernelHorizontalSobel, kernelHorizontalSobel, kernelHorizontalSobel]]
    kernel = torch.tensor(kernel, dtype=torch.float)

    imgConvVer = conv2d(imgTensor, kernel)
    imgConvVer = imgConvVer.permute(0, 2, 3, 1)

    plt.imshow(torch.abs(imgConvVer[0, :, :, 0]))
    plt.show()


if __name__ == '__main__':
    main()