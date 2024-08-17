import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Webcam Controlled Game with 3D Sprites")

# Set up the camera
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Load the character image
character = pygame.image.load('character.png')
character_rect = character.get_rect()
character_rect.center = (width // 2, height - 50)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Function to draw a 3D cube (as an obstacle)
def draw_cube():
    vertices = [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
    ]

    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    ]

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Capture frame from webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally
    frame = cv2.flip(frame, 1)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect movement (simple thresholding for demonstration)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Calculate the center of mass of the white areas
    moments = cv2.moments(thresh)
    if moments['m00'] != 0:
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        # Map the center of mass to the game window
        character_rect.centerx = int(cx * width / frame.shape[1])

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Draw the character (2D sprite)
    window.blit(character, character_rect)

    # Draw the 3D obstacle
    glPushMatrix()
    glTranslatef(0, 0, -5)
    draw_cube()
    glPopMatrix()

    # Update the display
    pygame.display.flip()
    pygame.time.wait(10)

# Release the webcam and close the game window
cap.release()
pygame.quit()
