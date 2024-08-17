import cv2
import os

path = "./sprites/instagram"

files = os.listdir(path)
for file in files:
    if file.split(".")[-1] != "png":
        continue
    img = cv2.imread(f"{path}/{file}", cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            if img[y, x, 0] == 0 and img[y, x, 1] == 0 and img[y, x, 2] == 0:
                img[y, x, 3] = 0
    cv2.imwrite(f"{path}/{file}", img)
