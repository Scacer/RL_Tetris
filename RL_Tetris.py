import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# global variables
BLOCK_SIZE = 30 # used for drawing later in the program

class Tetris():

    #shapes in arrays, 0s represent empty space
    pieces = [
        [[1, 1, 0],
         [0, 1, 1]], # Z

        [[0, 2, 2]
         [2, 2, 0]], # S

        [[3],
         [3],
         [3],
         [3]]        # I

        [[4, 4],
         [4, 4]]     # O

        [[5, 0, 0],
         [5, 5, 5]]  # J

        [[0, 0, 6],
         [6, 6, 6]]  # L

        [[0, 7, 0],
         [7, 7, 7]]  # T
    ]

    piece_colors = [
        (255, 255, 255),
        (255, 255, 0),
        (147, 88, 254),
        (54, 175, 144),
        (255, 0, 0),
        (102, 217, 238),
        (254, 151, 32),
        (0, 0, 255)
    ]
        
    def __init__(self, height=20, width=10, block_size=20):
        pass

    def reset(self):
        pass

    def rotate_piece(self, piece):
        num_rows = num_cols_new = len(piece)
        num_rows_new = len(piece[0])
        rotated_piece = []

        for i in num_rows_new:
            new_row = [0] * num_cols_new
            

    def step(self):

        #1. Check Move input

        #2. Check piece has been placed

        #2.2 Spawn New Piece

        #3 Check for Line Clears

        #3.2 Clear Lines

        #4 Check for game over
        pass
