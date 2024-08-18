![png](https://github.com/user-attachments/assets/3ba2aad5-a99d-4fb4-b832-f5a43f10b94a)
Homework Run is an augmented reality game that challenges players to stay active while avoiding obstacles and answering trivia questions. Using their body movements, players control their in-game character, dodging giant cellphones, hourglasses, and Instagram icons. If they collide with an obstacle, they must answer a true-false question on a topic of their choice. The game tracks the player's speed and detects when they're running, making it a fun and engaging way to stay active.

## Inspiration
With the oncoming Subway Surfers brainrot of the new generation, the goldfish attention span, and inability to touch grass, we developed a game that forces the new generation (and us) to stay active in the only way we know: Subway Surfers. 

As students, school can be hard. We were inspired by our struggles and decided to make it student themed!

## How we built it
We used a combination of computer vision and machine learning technologies to bring Homework Run to life. Here's a breakdown of our tech stack:

OpenCV: 
We used OpenCV to capture and process video frames from the player's webcam, detecting their body movements and tracking their speed.

MediaPipe: 
We leveraged MediaPipe to detect the player's pose and movements, allowing us to track their running speed and detect collisions with obstacles.

OpenAI's GPT-3.5:
We used OpenAI's GPT-3.5 language model to generate true-false questions on a topic of the player's choice, adding an educational element to the game.

Arduino and PySerial:
We used Arduino to control LED lights that provide feedback to the player, and PySerial to communicate with the Arduino board.

## Gameplay Mechanics

The game starts by asking the player to input a topic of their choice.
The player's webcam feed is used to detect their body movements, which control their in-game character.
Obstacles such as giant cellphones, hourglasses, and Instagram icons are generated randomly on the screen, and the player must dodge them by moving left, right, or ducking.
If the player collides with an obstacle, they must answer a true-false question on their chosen topic.
The game tracks the player's speed and detects when they're running, making it a fun and engaging way to stay active.
The game ends when the player's lives run out, and they can restart by pressing 'q'.


## Technical Details

We used the MediaPipe pose detection model to detect the player's pose and movements, which allows us to track their running speed and detect collisions with obstacles.
We used OpenCV to process the video frames from the player's webcam and detect their body movements.
We used OpenAI's GPT-3.5 language model to generate true-false questions on a topic of the player's choice.
We used Arduino to control LED lights that provide feedback to the player, and PySerial to communicate with the Arduino board.

## Challenges we ran into
Procrastinating by wandering a mall for 5 hours. Also had some trouble detecting whether the player was running. Working with mediapipe was also hard - learned a lot about human anatomy.

## Accomplishments that we're proud of
We made 3D images and we were able to render it in our app! We're also proud to have finished making the game in less than a day.

## What we learned
How to use mediapipe and opencv

## What's next for Homework Run
- Adding sound to the game
- Printing a nicer hardware case
- More accurate detection for running
- Better UI

