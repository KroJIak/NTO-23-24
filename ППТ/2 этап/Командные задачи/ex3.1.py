import cv2
import numpy as np
# Read the image
image = cv2.imread('data/template.png')
# Encode the image as a byte array
success, encoded_image = cv2.imencode('.jpg', image)
byte_array = np.array(encoded_image).tobytes()

print(byte_array)
