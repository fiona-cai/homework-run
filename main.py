import animation
import cv2
import logging_config
import logging
import mediapipe as mp
import numpy as np
# import lights
import time
import random
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_quiz(topic):
    prompt = f"Create a true-false question about {topic}. Use this example format - 'Russia is the largest country by area in the world. F\n'"
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant helping a teacher write questions."},
            {"role": "user", "content": prompt}
        ]
    )
    
    quiz = response.choices[0].message.content.strip()
    return quiz


# light_port = lights.get_port()

cur_frame = 0

max_obstacles = 1 # this increases as time goes on
last_addition = time.time()
addition_time = 20

vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

logging_config.setup_logging()

pose_detector = mp.solutions.pose.Pose(static_image_mode=True)
selfie_segmentation = mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=1)

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
    
    def show_quiz_question(frame, flag):
        quiz = generate_quiz(topic)
        question = quiz[:-2]
        answer=quiz[-1]
        
        if answer == "T":
            answer = True
        else:
            answer = False

        quiz_frame = np.zeros((480, 720, 3), dtype=np.uint8)
        quiz_frame[:, :360, :] = (255, 0, 0)  # red for false
        quiz_frame[:, 360:, :] = (0, 0, 255)  # blue for true
        quiz_frame = cv2.putText(quiz_frame, question, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('quiz', quiz_frame)
        cv2.waitKey(3000)  # wait for 1 second
        time.sleep(3)
        while time.time() - start_time < 3:
            results = pose_detector.process(frame)
            if results.pose_landmarks:
                x, y = int(results.pose_landmarks.landmark[0].x * frame.shape[1]), int(results.pose_landmarks.landmark[0].y * frame.shape[0])
                cv2.putText(quiz_frame, f"Time left: {int(3 - (time.time() - start_time))}s", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                cv2.imshow('quiz', quiz_frame)
                if x < 360:
                    answer = False
                else:
                    answer = True
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        if answer == flag:
            quiz_frame = cv2.putText(quiz_frame, "Correct!", (360, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            quiz_frame = cv2.putText(quiz_frame, "Incorrect!", (360, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow('quiz', quiz_frame)
        cv2.waitKey(1000)  # wait for 1 second
        cv2.destroyWindow('quiz')
        

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

# lights.left_on(light_port)
# lights.middle_on(light_port)
# lights.right_on(light_port)

# List to store last num_frames ratios

knee_to_head_ratios = []
num_frames = 4
threshold = 1800

lives = 3
game_over = False
first_load = True
topic = ""

start_time = time.time()

while(True):
    if first_load:
        first_load = False
        topic = get_player_topic()


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
    seg_results = selfie_segmentation.process(frame)
    
    mask = seg_results.segmentation_mask >= 0.001
    mask = mask.astype(np.uint8) * 255

    black_background = np.zeros_like(frame)
    person_with_black_bg = cv2.bitwise_and(frame, frame, mask=mask)
    frame = cv2.bitwise_or(black_background, person_with_black_bg)
    

    # print(results.pose_landmarks)
    
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

            logging.info(f"THE LEFT KNEE TO HEAD RATIO IS {left_knee_to_head_ratio}")

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
    if cur_time - last_addition > addition_time:
        last_addition = cur_time
        max_obstacles += 1

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
                            pass
                            # lights.left_off(light_port)
                        elif lives == 1:
                            pass
                            # lights.middle_off(light_port)
                        elif lives <= 0:
                            pass
                            # lights.right_off(light_port)
                            logging.info("GAME OVER")
                            game_over = True
                            break

                        # Show quiz question
                        flag = True  # hardcoded flag for this question
                        if Obstacle.show_quiz_question(frame, flag):
                            lives += 1
                            if lives == 3:
                                pass
                                # lights.right_on(light_port)
                            elif lives == 2:
                                pass
                                # lights.middle_on(light_port)
                            elif lives == 1:
                                pass
                                # lights.left_on(light_port)

                        obstacles.remove(obs)
                        break
        if obs.size[0] > 200 or obs.size[1] > 200:
            obstacles.remove(obs) # too big
    
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
# lights.close(light_port)
