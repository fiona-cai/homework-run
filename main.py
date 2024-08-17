import animation
import cv2
import logging_config
import logging
import mediapipe as mp
import lights
import time

light_port = lights.get_port()

cur_frame = 0

vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

logging_config.setup_logging()

pose_detector = mp.solutions.pose.Pose(static_image_mode=True)

time.sleep(2) # wait for the lights to connect

connections = [
    (16, 14),
    (14, 12),
    (12, 11),
    (12, 24),
    (24, 23),
    (11, 23),
    (11, 13),
    (13, 15),
    (24, 26),
    (26, 28),
    (23, 25),
    (25, 27)
]

lights.left_on(light_port)
lights.middle_on(light_port)
lights.right_on(light_port)

prev_left_knee_pt = None

while(True): 
    # Capture the video frame by frame 
    ret, frame = vid.read()
    
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    
    results = pose_detector.process(frame)
    print(results.pose_landmarks)
    
    if results.pose_landmarks:
        x_diff = int(results.pose_landmarks.landmark[7].x * frame.shape[1]) - int(results.pose_landmarks.landmark[8].x * frame.shape[1])
        y_diff = int(results.pose_landmarks.landmark[7].y * frame.shape[0]) - int(results.pose_landmarks.landmark[8].y * frame.shape[0])
        square = x_diff ** 2 + y_diff ** 2
        distance = int(square ** 0.5) # distance between 7 and 8, diameter of the circle
        head_point = (int(results.pose_landmarks.landmark[0].x * frame.shape[1]), int(results.pose_landmarks.landmark[0].y * frame.shape[0])) # 0
        cv2.circle(frame, head_point, distance, (0, 255, 0), 3)

        # logging.info(f"The point for 26 is: {results.pose_landmarks.landmark[26].y}")
        # logging.info(f"The head distance is is {head_point}")

        # use this point to detect whether or not the player is running, amplitude has to be relative to head distance
        left_knee_relative = int(results.pose_landmarks.landmark[26].y * frame.shape[0])
        logging.info(f"THE LEFT KNEE RELATIVE IS {left_knee_relative}")

        amplitude = abs((head_point[1] - left_knee_relative) / distance)
        # logging.info(f"headpoint {head_point[1]} - left knee relative {left_knee_relative}")
        # logging.info(f"THE DISTANCE IS {distance}")
        # logging.info(f"THE AMPLITUDE IS {amplitude}")


        for connection in connections:
            start_idx, end_idx = connection
            start_landmark = results.pose_landmarks.landmark[start_idx]
            end_landmark = results.pose_landmarks.landmark[end_idx]
            start_point = (int(start_landmark.x * frame.shape[1]), int(start_landmark.y * frame.shape[0]))
            end_point = (int(end_landmark.x * frame.shape[1]), int(end_landmark.y * frame.shape[0]))
            cv2.circle(frame, start_point, 5, (0, 0, 255), -1)
            cv2.circle(frame, end_point, 5, (0, 0, 255), -1)
            cv2.line(frame, start_point, end_point, (255, 0, 0), 2)

    # obstacle test scuffed code
    frame = animation.phone(cur_frame, frame, position=(0, 0), size=(150, 300))

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    cur_frame += 1

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
lights.close(light_port)
