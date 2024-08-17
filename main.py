import animation
import cv2
import logging_config
import logging
import mediapipe as mp
import lights
import time
import random

light_port = lights.get_port()

cur_frame = 0

vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

logging_config.setup_logging()

pose_detector = mp.solutions.pose.Pose(static_image_mode=True)

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

start_time = time.time()

while(True): 
    # Capture the video frame by frame
    cur_time = time.time()
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
                        # lights.left_off(light_port)
                        # lights.middle_off(light_port)
                        # lights.right_off(light_port)
                        # lights.all_on(light_port)
                        # time.sleep(1)
                        # lights.all_off(light_port)
                        obstacles.remove(obs)
                        break
        if obs.size[0] > 200 or obs.size[1] > 200:
            obstacles.remove(obs)
    
    frame = cv2.putText(frame, f"Time Elapsed: {round(cur_time - start_time, 2)}s", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    cur_frame += 1

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
# close serial port
lights.close(light_port)
