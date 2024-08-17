import cv2

FRAMES = {
    "hourglass": 32,
    "phone": 49
}

def phone(cur_frame_num, frame, position=(0, 0), size=(640, 480)):
    num = cur_frame_num % FRAMES["hourglass"]
    img = cv2.imread(f"./sprites/phone/frame_{num}.png", cv2.IMREAD_UNCHANGED)
    return animate(img, frame, position, size)

def hourglass(cur_frame_num, frame, position=(0, 0), size=(640, 480)):
    num = cur_frame_num % FRAMES["hourglass"]
    img = cv2.imread(f"./sprites/hourglass/Iridescent Hourglass@1-1249x585 ({num}).png", cv2.IMREAD_UNCHANGED)
    
    return animate(img, frame, position, size)

def animate(img, frame, position, size):
    img = cv2.resize(img, size)
    bg_height, bg_width = frame.shape[:2]
    ov_height, ov_width = img.shape[:2]

    # Calculate the position to center the overlay on the background
    x_offset = position[0]
    y_offset = position[1]

    for y in range(ov_height):
        for x in range(ov_width):
            overlay_color = img[y, x, :3]  # first three elements are color (RGB)
            overlay_alpha = img[y, x, 3] / 255  # 4th element is the alpha channel, convert from 0-255 to 0.0-1.0

            # get the color from the background image
            background_color = frame[y + y_offset, x + x_offset]

            # combine the background color and the overlay color weighted by alpha
            composite_color = background_color * (1 - overlay_alpha) + overlay_color * overlay_alpha

            # update the result image in place
            frame[y + y_offset, x + x_offset] = composite_color
    return frame
