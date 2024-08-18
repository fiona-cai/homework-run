import cv2
import numpy as np
import os

path = "./sprites/instagram"

slice_off = 0

files = os.listdir(path)
for file in files:
    if file.split(".")[-1] != "png":
        continue
    img = cv2.imread(f"{path}/{file}", cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    new_array = []
    for y in range(slice_off, img.shape[0] - slice_off):
        new_line = []
        for x in range(slice_off, img.shape[1] - slice_off):
            if img[y, x, 0] == 0 and img[y, x, 1] == 0 and img[y, x, 2] == 0:
                img[y, x, 3] = 0
            new_line.append(img[y, x])
        new_array.append(new_line)
    cv2.imwrite(f"{path}/{file}", np.array(new_array))
