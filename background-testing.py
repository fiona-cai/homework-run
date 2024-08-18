import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose and Selfie Segmentation
pose_detector = mp.solutions.pose.Pose(static_image_mode=True)
selfie_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

# Video capture
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = vid.read()
    if not ret:
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Process the frame for pose detection
    results = pose_detector.process(frame)

    # Process the frame for segmentation
    seg_results = selfie_segmentation.process(frame)

    # Create a mask where the person is segmented
    mask = seg_results.segmentation_mask > 0.1
    mask = mask.astype(np.uint8) * 255

    # Create a black background
    black_background = np.zeros_like(frame)

    # Combine the person with the black background
    person_with_black_bg = cv2.bitwise_and(frame, frame, mask=mask)
    black_bg_with_person = cv2.bitwise_or(black_background, person_with_black_bg)

    # Display the result
    cv2.imshow('frame', black_bg_with_person)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
vid.release()
cv2.destroyAllWindows()
