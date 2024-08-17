import cv2
import numpy as np

# Load the background image
background = cv2.imread('background.png')

# Check if the background image was loaded successfully
if background is None:
    raise FileNotFoundError("Background image not found or could not be loaded.")

# Get dimensions of the background image
bg_height, bg_width = background.shape[:2]

# Open the video file
cap = cv2.VideoCapture('IMG_9422.mp4')

# Check if the video was opened successfully
if not cap.isOpened():
    raise FileNotFoundError("Video file not found or could not be loaded.")

# Get the frame rate of the video
fps = cap.get(cv2.CAP_PROP_FPS)

# Get the dimensions of the video frames
ov_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
ov_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Calculate the position to center the overlay on the background
x_offset = (bg_width - ov_width) // 2
y_offset = (bg_height - ov_height) // 2

# Create a VideoWriter object to save the combined video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('combined.mp4', fourcc, fps, (bg_width, bg_height))

while True:
    ret, overlay = cap.read()
    if not ret:
        break

    # Create a copy of the background to overlay the image
    result = background.copy()

    # Check if the overlay has an alpha channel
    if overlay.shape[2] == 4:
        # Overlay the image with alpha channel
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
    else:
        # Overlay the image without alpha channel
        result[y_offset:y_offset + ov_height, x_offset:x_offset + ov_width] = overlay

    # Write the frame to the output video
    out.write(result)

# Release the video capture and writer objects
cap.release()
out.release()
cv2.destroyAllWindows()
