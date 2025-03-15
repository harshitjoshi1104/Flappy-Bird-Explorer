# Flappy Bird Explorer

Flappy Bird Explorer is a Python implementation of the classic Flappy Bird game. This project aims to provide an educational and fun experience by allowing users to explore and modify the game's code.

## Features

- Flappy Bird gameplay
- Simple and easy-to-understand codebase
- Customizable game mechanics

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/harshitjoshi1104/Flappy-Bird-Explorer.git

The main.py file is the main script for a Flappy Bird game simulation using the Windows Explorer. Here is an explanation of the key components and functionality:

## Imports and Global Variables:
- Various Python modules are imported, such as win32com.client, pyautogui, and keyboard, which are used for Windows automation, GUI interactions, and keyboard event handling.
Global variables are defined for the game configuration, such as the number of rows and columns (MAX_COL_COUNT, MAX_ROW_COUNT), time frames, and icon paths.

## Game Initialization:
The game_init function initializes the game by creating shortcut files (.lnk) that represent game elements (e.g., flappy bird, pipes) in the specified directory with appropriate icons.

## File Coloring:
The color_text_file function changes the icon of a specific shortcut file to represent different game elements (green for pipes, white for empty space, and flappy bird icon).

## Pipe Management:
Functions like set_pipe, reset_pipe_column, MovePipe, and Create_Pipes handle the creation, movement, and resetting of pipes in the game grid.

## Flappy Bird Movement:
The move_flappy_bird function handles the movement of the flappy bird based on keyboard inputs (W, A, S, D keys).
The create_flappy_bird_instance function initializes the flappy bird and listens for keyboard events to move it.

## Game Loop:
The main function initializes the game, starts threads for moving pipes and handling flappy bird movements, and continuously creates pipes at regular intervals until the game exits.
The script uses threading to manage concurrent tasks, such as moving pipes and handling user inputs, ensuring smooth gameplay. The game runs in a specified directory, with shortcut files representing the game elements.
