import os
import pygame
import tkinter as tk
from tkinter import *

# Initialize Pygame and Tkinter
root = tk.Tk()
embed = tk.Frame(root, width=500, height=500)  # creates embed frame for pygame window
embed.grid(columnspan=1, rowspan=1)  # Adds grid
embed.pack(side=LEFT)  # packs window to the left
buttonwin = tk.Frame(root, width=75, height=500)
buttonwin.pack(side=LEFT)

# Set environment variables for Pygame
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

# Initialize Pygame display
pygame.display.init()
screen = pygame.display.set_mode((500, 500))
screen.fill(pygame.Color(255, 255, 255))  # Fill the screen with white
pygame.display.update()

def draw():
    pygame.draw.circle(screen, (0, 0, 0), (250, 250), 125)  # Draw a black circle
    pygame.display.update()  # Update the display

button1 = Button(buttonwin, text='Draw', command=draw)  # Button to trigger drawing
button1.pack(side=LEFT)

def run_pygame():
    while True:
        for event in pygame.event.get():  # Handle Pygame events
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit Pygame if the window is closed
                root.quit()  # Quit Tkinter as well
        root.update()  # Update Tkinter
        pygame.display.update()  # Update Pygame display

# Start the Pygame loop
run_pygame()
