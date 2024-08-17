import cv2
import numpy as np

# Load the background and overlay images
background = cv2.imread('background.png')
overlay = cv2.imread('overlay.png', cv2.IMREAD_UNCHANGED)  # IMREAD_UNCHANGED => open image with the alpha channel

# Check if the images were loaded successfully
if background is None:
    raise FileNotFoundError("Background image not found or could not be loaded.")
if overlay is None:
    raise FileNotFoundError("Overlay image not found or could not be loaded.")

# Get dimensions of the background and overlay images
bg_height, bg_width = background.shape[:2]
ov_height, ov_width = overlay.shape[:2]

# Calculate the position to center the overlay on the background
x_offset = (bg_width - ov_width) // 2
y_offset = (bg_height - ov_height) // 2

# Create a copy of the background to overlay the image
result = background.copy()

# Overlay the image
for y in range(ov_height):
    for x in range(ov_width):
        overlay_color = overlay[y, x, :3]  # first three elements are color (RGB)
        overlay_alpha = overlay[y, x, 3] / 255  # 4th element is the alpha channel, convert from 0-255 to 0.0-1.0

        # get the color from the background image
        background_color = background[y + y_offset, x + x_offset]

        # combine the background color and the overlay color weighted by alpha
        composite_color = background_color * (1 - overlay_alpha) + overlay_color * overlay_alpha

        # update the result image in place
        result[y + y_offset, x + x_offset] = composite_color
while 1:
    cv2.imshow('combined', result)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
