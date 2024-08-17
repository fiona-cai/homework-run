import cv2

# Load the images
background = cv2.imread('background.png')
overlay = cv2.imread('overlay.png')

# Get dimensions of the background image
bg_height, bg_width = background.shape[:2]  # Corrected this line

# Resize the overlay image to fit within the background image
overlay_resized = cv2.resize(overlay, (bg_width, bg_height))

# Create a mask of the overlay image
overlay_gray = cv2.cvtColor(overlay_resized, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(overlay_gray, 1, 255, cv2.THRESH_BINARY)

# Invert the mask
mask_inv = cv2.bitwise_not(mask)

# Black-out the area of overlay in the background
bg_part = cv2.bitwise_and(background, background, mask=mask_inv)

# Take only region of overlay from overlay image
overlay_part = cv2.bitwise_and(overlay_resized, overlay_resized, mask=mask)

# Add the overlay part to the background part
result = cv2.add(bg_part, overlay_part)

# Save the result
cv2.imwrite('result.png', result)

# Display the result
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
