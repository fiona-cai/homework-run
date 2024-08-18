import animation
import cv2
import logging_config
import logging
import mediapipe as mp
import numpy as np
import lights
import time
import random

light_port = lights.get_port()

cur_frame = 0

vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

logging_config.setup_logging()

pose_detector = mp.solutions.pose.Pose(static_image_mode=True)

def get_player_topic():
    screen = np.zeros((480, 720, 3), dtype=np.uint8)
    cv2.putText(screen, 'Enter your topic:', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    user_input = ''
    input_active = True
    
    while input_active:
        screen = cv2.putText(screen, user_input, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('Input Screen', screen)
        
        key = cv2.waitKey(1)
        
        # Handle key presses
        if key == ord('\r'):
            input_active = False
        elif key >= 32 and key <= 126:
            user_input += chr(key)
    
    cv2.destroyWindow('Input Screen')
    return user_input


class Obstacle:
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
object_locations = [
    # move left and right
    [144, 380],
    [288, 380],
    [432, 380],
    # duck
    [133, 200],
    [288, 200],
    [432, 200],
]

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

lives = 3
game_over = False
first_load = True
topic = ""

start_time = time.time()

while(True):
    if first_load:
        first_load = False
        get_player_topic()


    if game_over:
        frame = np.zeros((480, 720, 3), dtype=np.uint8)
        frame = cv2.putText(frame, "GAME OVER", (180, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 4)
        frame = cv2.putText(frame, "Press 'q' to quit", (180, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

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

        
        left_knee_pt = results.pose_landmarks.landmark[26].y
        left_knee_relative = int(results.pose_landmarks.landmark[26].y * frame.shape[0]) # left knee point relative to the frame of the camera

        if left_knee_pt >= 0 and left_knee_pt <= 1: # ensures that it's in the frame
            left_knee_to_head_ratio = abs((head_point[1] - left_knee_relative) / distance)
            left_knee_to_head_ratio *= 1000 # scale it up for more precise accuracy
            knee_to_head_ratios.append(left_knee_to_head_ratio)

            logging.info(f"THE LEFT KNEE TO HEAD RATIO IS {left_knee_to_head_ratio}")

            if len(knee_to_head_ratios) > num_frames:
                knee_to_head_ratios.pop(0)

            if len(knee_to_head_ratios) == num_frames:
                ratio_change = knee_to_head_ratios[-1] - knee_to_head_ratios[0]
                logging.info(f"Ratio change over {num_frames} frames: {ratio_change}")
                
                if ratio_change > threshold:
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
    if len(obstacles) == 0:
        obstacles.append(Obstacle(random.choice(object_locations), [10, 10], random.choice(["hourglass", "phone", "instagram"])))
    else:
        for obs in obstacles:

            frame = obs.func(cur_frame, frame, position=(obs.position[0], obs.position[1]), size=(obs.size[0], obs.size[1]))
            obs.inc()
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    if obs.collide([x, y]):
                        print("COLLISION DETECTED")
                        lives -= 1
                        if lives == 2:
                            lights.left_off(light_port)
                        elif lives == 1:
                            lights.middle_off(light_port)
                        elif lives <= 0:
                            lights.right_off(light_port)
                            logging.info("GAME OVER")
                            game_over = True
                            break


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
