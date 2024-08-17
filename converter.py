import cv2
import os

def extract_frames(video_path, output_folder, frames_per_second, duration):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    fps = int(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = fps // frames_per_second

    # Calculate the starting frame for the last 'duration' seconds
    start_frame = total_frames - (duration * fps)
    if start_frame < 0:
        start_frame = 0

    count = 0
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    success, image = video.read()
    while success:
        if count % frame_interval == 0:
            frame_id = count // frame_interval
            cv2.imwrite(f"sprites/instagram/frame_{frame_id}.png", image)
        success, image = video.read()
        count += 1

    video.release()

# Example usage
video_path = 'sprites/instagram/instagram.mp4'
output_folder = 'output_frames'
frames_per_second = 4
duration = 10  # Last 10 seconds
extract_frames(video_path, output_folder, frames_per_second, duration)
