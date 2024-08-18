import animation
import cv2
import logging_config
import logging
import mediapipe as mp
import time
import random
import numpy as np
import lights


light_port = lights.get_port()


cur_frame = 0

vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

logging_config.setup_logging()

pose_detector = mp.solutions.pose.Pose(static_image_mode=True)
selfie_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

class obstacle:
    def __init__(self, position, size, kind):
        self.position = position
        self.size = size
        self.kind = kind
        self.func = animation.instagram if kind == "instagram" else animation.phone if kind == "phone" else animation.hourglass
    
    def inc(self):
        self.position[0] -= 1
        self.position[1] -= 1
        self.size[0] += 2
        self.size[1] += 2
    
    def collide(self, point):
        if self.size[0] < 70 and self.size[1] < 70:
            return False
        if point[0] >= self.position[0] and point[0] <= self.position[0] + self.size[0] and point[1] >= self.position[1] and point[1] <= self.position[1] + self.size[1]:
            return True
        return False

obstacles = []

# time.sleep(2) 

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

knee_to_head_ratios = []
num_frames = 8
threshold = 1800

start_time = time.time()

while(True): 
    cur_time = time.time()
    ret, frame = vid.read()
    frame = cv2.flip(frame, 1)
    
    results = pose_detector.process(frame)
    seg_results = selfie_segmentation.process(frame)

    mask = seg_results.segmentation_mask >= 0.001
    mask = mask.astype(np.uint8) * 255

    black_background = np.zeros_like(frame)
    person_with_black_bg = cv2.bitwise_and(frame, frame, mask=mask)
    frame = cv2.bitwise_or(black_background, person_with_black_bg)
    
    if results.pose_landmarks:
        x_diff = int(results.pose_landmarks.landmark[7].x * frame.shape[1]) - int(results.pose_landmarks.landmark[8].x * frame.shape[1])
        y_diff = int(results.pose_landmarks.landmark[7].y * frame.shape[0]) - int(results.pose_landmarks.landmark[8].y * frame.shape[0])
        square = x_diff ** 2 + y_diff ** 2
        distance = int(square ** 0.5)
        head_point = (int(results.pose_landmarks.landmark[0].x * frame.shape[1]), int(results.pose_landmarks.landmark[0].y * frame.shape[0]))
        cv2.circle(frame, head_point, distance, (0, 255, 0), 3)

        left_knee_pt = results.pose_landmarks.landmark[26].y
        left_knee_relative = int(results.pose_landmarks.landmark[26].y * frame.shape[0])

        if left_knee_pt >= 0 and left_knee_pt <= 1:
            left_knee_to_head_ratio = abs((head_point[1] - left_knee_relative) / distance)
            left_knee_to_head_ratio *= 1000
            knee_to_head_ratios.append(left_knee_to_head_ratio)

            if len(knee_to_head_ratios) > num_frames:
                knee_to_head_ratios.pop(0)

            if len(knee_to_head_ratios) == num_frames:
                ratio_change = knee_to_head_ratios[-1] - knee_to_head_ratios[0]
                time_elapsed = cur_time - start_time
                speed = abs(left_knee_to_head_ratio / time_elapsed)
                logging.info(f"Speed: {speed} units/s")
                
                if speed > threshold:
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

    if len(obstacles) == 0:
        obstacles.append(obstacle([random.randint(0, 640), random.randint(0, 480)], [10, 10], random.choice(["hourglass", "phone", "instagram"])))
    else:
        for obs in obstacles:
            frame = obs.func(cur_frame, frame, position=(obs.position[0], obs.position[1]), size=(obs.size[0], obs.size[1]))
            obs.inc()
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    if obs.collide([x, y]):
                        print("COLLISION DETECTED")
                        obstacles.remove(obs)
                        break
        if obs.size[0] > 200 or obs.size[1] > 200:
            obstacles.remove(obs)
    
    frame = cv2.putText(frame, f"Time Elapsed: {round(cur_time - start_time, 2)}s", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cur_frame += 1

vid.release() 
cv2.destroyAllWindows() 

