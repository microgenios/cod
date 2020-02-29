#!/usr/bin/python
import sys
import cv2
import numpy as np

input_file = sys.argv[1]  # Load and display an image -- 'forest.jpg'
img = cv2.imread(input_file)
cv2.imshow("Original", img)
h, w = img.shape[:2]  # Cropping an image
start_row, end_row = int(0.21 * h), int(0.73 * h)
start_col, end_col = int(0.37 * w), int(0.92 * w)
img_cropped = img[start_row:end_row, start_col:end_col]
cv2.imshow("Cropped", img_cropped)
scaling_factor = 1.3  # Resizing an image
img_scaled = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_LINEAR)
cv2.imshow("Uniform resizing", img_scaled)
img_scaled = cv2.resize(img, (250, 400), interpolation=cv2.INTER_AREA)
cv2.imshow("Skewed resizing", img_scaled)
output_file = input_file[:-4] + "_cropped.jpg"  # Save an image
cv2.imwrite(output_file, img_cropped)
cv2.waitKey()