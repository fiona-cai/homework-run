import cv2
import mediapipe as mp
import lights
import time

light_port = lights.get_port()

vid = cv2.VideoCapture(0) 
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

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
        distance = int(square ** 0.5)
        head_point = (int(results.pose_landmarks.landmark[0].x * frame.shape[1]), int(results.pose_landmarks.landmark[0].y * frame.shape[0]))
        cv2.circle(frame, head_point, distance, (0, 255, 0), 3)
        
        for connection in connections:
            start_idx, end_idx = connection
            start_landmark = results.pose_landmarks.landmark[start_idx]
            end_landmark = results.pose_landmarks.landmark[end_idx]
            start_point = (int(start_landmark.x * frame.shape[1]), int(start_landmark.y * frame.shape[0]))
            end_point = (int(end_landmark.x * frame.shape[1]), int(end_landmark.y * frame.shape[0]))
            cv2.circle(frame, start_point, 5, (0, 0, 255), -1)
            cv2.circle(frame, end_point, 5, (0, 0, 255), -1)
            cv2.line(frame, start_point, end_point, (255, 0, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
lights.close(light_port)
