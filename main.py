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
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
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

# List to store last num_frames ratios
knee_to_head_ratios = []
num_frames = 8 # may need to do more testing here
threshold = 2000

while(True): 
    # Capture the video frame by frame 
    ret, frame = vid.read()
    
    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)
    
    results = pose_detector.process(frame)
    # print(results.pose_landmarks)
    
    if results.pose_landmarks:
        x_diff = int(results.pose_landmarks.landmark[7].x * frame.shape[1]) - int(results.pose_landmarks.landmark[8].x * frame.shape[1])
        y_diff = int(results.pose_landmarks.landmark[7].y * frame.shape[0]) - int(results.pose_landmarks.landmark[8].y * frame.shape[0])
        square = x_diff ** 2 + y_diff ** 2
        distance = int(square ** 0.5) # distance between 7 and 8, diameter of the circle
        head_point = (int(results.pose_landmarks.landmark[0].x * frame.shape[1]), int(results.pose_landmarks.landmark[0].y * frame.shape[0])) # 0
        cv2.circle(frame, head_point, distance, (0, 255, 0), 3)

        
        # use this point to detect whether or not the player is running, amplitude has to be relative to head distance
        # logging.info(results.pose_landmarks.landmark[26])
        left_knee_pt = results.pose_landmarks.landmark[26].y
        left_knee_relative = int(results.pose_landmarks.landmark[26].y * frame.shape[0]) # left knee point relative to the frame of the camera

        if left_knee_pt >= 0 and left_knee_pt <= 1: # ensures that it's in the frame
            left_knee_to_head_ratio = abs((head_point[1] - left_knee_relative) / distance)
            left_knee_to_head_ratio *= 1000 # scale it up for more precise accuracy
            knee_to_head_ratios.append(left_knee_to_head_ratio)

            # logging.info(f"Calulation: head_point: {head_point[1]} - left_knee_relative: {left_knee_relative} then divided by distance is {distance}")
            logging.info(f"THE LEFT KNEE TO HEAD RATIO IS {left_knee_to_head_ratio}")

            if len(knee_to_head_ratios) > num_frames:
                knee_to_head_ratios.pop(0)

            if len(knee_to_head_ratios) == num_frames:
                ratio_change = knee_to_head_ratios[-1] - knee_to_head_ratios[0]
                logging.info(f"Ratio change over {num_frames} frames: {ratio_change}")
                
                # Decide if the movement indicates running
                if ratio_change > threshold:  # Define an appropriate threshold
                    logging.info("Running detected!")
                else:
                    logging.info("No significant running detected.")
                
            logging.info(f"Current ratio: {left_knee_to_head_ratio}")


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
    frame = animation.insta(cur_frame, frame, position=(0, 0), size=(150, 200))

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    cur_frame += 1

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
lights.close(light_port)
