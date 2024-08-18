![png](https://github.com/user-attachments/assets/3ba2aad5-a99d-4fb4-b832-f5a43f10b94a)

# Homework Run

Homework Run is an augmented reality game that challenges players to stay active while avoiding obstacles and answering trivia questions. Using their body movements, players control their in-game character, dodging giant cellphones, hourglasses, and Instagram icons. If they collide with an obstacle, they must answer a true-false question on a topic of their choice. The game tracks the player's speed and detects when they're running, making it a fun and engaging way to stay active.

## Inspiration

With the oncoming Subway Surfers brainrot of the new generation, the goldfish attention span, and inability to touch grass, we developed a game that forces the new generation (and us) to stay active in the only way we know: Subway Surfers.

As students, school can be hard. We were inspired by our struggles and decided to make it student-themed!

## How We Built It

We used a combination of computer vision and machine learning technologies to bring Homework Run to life. Here's a breakdown of our tech stack:

- **OpenCV**: Captured and processed video frames from the player's webcam, detecting their body movements and tracking their speed.
- **MediaPipe**: Detected the player's pose and movements, allowing us to track their running speed and detect collisions with obstacles.
- **OpenAI's GPT-3.5**: Generated true-false questions on a topic of the player's choice, adding an educational element to the game.
- **Arduino and PySerial**: Controlled LED lights that provide feedback to the player, and communicated with the Arduino board.

## Gameplay Mechanics

1. The game starts by asking the player to input a topic of their choice.
2. The player's webcam feed is used to detect their body movements, which control their in-game character.
3. Obstacles such as giant cellphones, hourglasses, and Instagram icons are generated randomly on the screen, and the player must dodge them by moving left, right, or ducking.
4. If the player collides with an obstacle, they must answer a true-false question on their chosen topic.
5. The game tracks the player's speed and detects when they're running, making it a fun and engaging way to stay active.
6. The game ends when the player's lives run out, and they can restart by pressing 'q'.

## Technical Details

- **MediaPipe**: Used to detect the player's pose and movements, allowing us to track their running speed and detect collisions with obstacles.
- **OpenCV**: Processed the video frames from the player's webcam and detected their body movements.
- **OpenAI's GPT-3.5**: Generated true-false questions on a topic of the player's choice.
- **Arduino and PySerial**: Controlled LED lights that provide feedback to the player, and communicated with the Arduino board.

## Challenges We Ran Into

- Procrastinating by wandering a mall for 5 hours.
- Trouble detecting whether the player was running.
- Working with MediaPipe was challenging; we learned a lot about human anatomy.

## Accomplishments That We're Proud Of

- Created 3D images and rendered them in our app.
- Finished making the game in less than a day.

## What We Learned

- How to use MediaPipe and OpenCV.

## What's Next for Homework Run

- Adding sound to the game.
- Printing a nicer hardware case.
- More accurate detection for running.
- Better UI.

## Installation

To get started with Homework Run, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/homework-run.git
    cd homework-run
    ```

2. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the game**:
    ```bash
    python main.py
    ```

## Contributing

We welcome contributions! Please read our Contributing Guidelines for more details.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
