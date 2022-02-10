import pygame
import random
from enum import Enum


# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

pygame.font.init()

# global variables
WIDTH = 300
HEIGHT = 720
BLOCK_SIZE = 30 # Used for drawing later in the program
PLAY_AREA_START = 120 # Combined with BLOCK_SIZE, this allows for blocks for
                      # graphics above the play area.

SPEED = 20 # Sets game speed.

################################################################################
################################################################################

# This class uses Enum to predefine constants for directions later in the program
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

################################################################################
################################################################################

class Piece():

    # Shapes stored as Arrays, 0s represent empty space, anything else represents
    # a block.
    pieces = [
        [[1, 1, 0],
         [0, 1, 1]], # Z

        [[0, 2, 2],
         [2, 2, 0]], # S

        [[3],
         [3],
         [3],
         [3]],        # I

        [[4, 4],
         [4, 4]],     # O

        [[5, 0, 0],
         [5, 5, 5]],  # J

        [[0, 0, 6],
         [6, 6, 6]],  # L

        [[0, 7, 0],
         [7, 7, 7]]  # T
    ]

    piece_colours = [
        (255, 255, 106),
        (255, 255, 0),
        (147, 88, 254),
        (54, 175, 144),
        (255, 0, 0),
        (102, 217, 238),
        (254, 151, 32),
        (0, 0, 255)
    ]
    
    # When creating a piece object, a random piece identifer 0 - 6 is created.
    # This value is then used to index the pieces array such that a random
    # piece may be chosen.
    # Due to the design of the piece_colours array, this means that the same index
    # can be used to ensure the pieces' colours remain consistent.
    def __init__(self, piece_id=random.randint(0, 6)):
        self.piece = Piece.pieces[piece_id]
        self.colour = Piece.piece_colours[piece_id]
        self.x = 5
        self.y = (PLAY_AREA_START - 1)
        self.piece_id = piece_id

    # The function inverts the number of rows and columns by assigning them to
    # new variables, and then creating each new row based on the information of
    # the existing piece.
    def rotate(self):
        piece = self.piece
        # Checks to ensure the piece is not an O piece, as the O piece has
        # no rotations.
        if self.piece_id != 3:
            # Rotates once for clockwise rotation.
            num_rows = num_cols_new = len(piece)
            num_rows_new = len(piece[0])
            rotated_piece = []

            for i in range(0, num_rows_new):
                new_row = [0] * num_cols_new
                for j in range(0, num_cols_new):
                    new_row[j] = piece[(num_rows-1) - j][i]
                rotated_piece.append(new_row)
            if noRotations == 3:
                piece = rotated_piece
        else:
            return self.piece

        return rotated_piece

################################################################################
################################################################################

class Tetris():
        
    def __init__(self):

        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.fall_speed = 0.3
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):

        # Initialises the grid, making it entirely empty
        self.locked_positions = {}
        self.grid = self._create_grid()

        self._draw_window()

        self.change_piece = False
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.fall_time = 0
        self.direction = None

    def step(self):
        
        # Recreates the grid each step in case new "blocks" in the grid are locked
        self.grid = self._create_grid(self.locked_positions)

        #1. Check Move input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction == Direction.DOWN

        self._move() # moves the piece
        
        self.shape_pos = self._shape_reformat()
        print(self.shape_pos)

        # Adds the the colours for blocks to the grid for the shape as it enters the screen
        for i in range(len(self.shape_pos)):
            x, y, = self.shape_pos[i]
            # If a part of the shape is above the screen, it will not be drawn.
            if y > -1:
                self.grid[y][x] = self.current_piece.colour

        # Adds location and colour data to the locked_positions array for use in grid creation
        if self.change_piece:
            for pos in self.shape_pos:
                p = (pos[0], pos[1])
                self.locked_positions[p] = self.current_piece.colour
            # Changes over the pieces
            self.current_piece = next_piece
            self.next_piece = Piece()

        if _is_gameOver():
            reset()

        # get_rawtime() gets the time elapsed since the last clock tick, giving us a CPU relative
        # measurement in order to determine fps.
        self.fall_time += clock.get_rawtime()
        self._draw_window()
        self.clock.tick(SPEED)

        self._is_pieceDrop()

    # create_grid takes a dictionary as an argument which will be used for
    # identifying which blocks should not be changed when drawing each frame
    def _create_grid(self, locked_pos = {}):

        # Creates 20 Sublists of 10 Colours for drawing the rows for tetris
        grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                # j represents the column, and i represents the row
                # this loop ensures that if a value in the grid has already
                # been marked as locked in locked_pos, the empty space will
                # be overridden, and the correct grid data will be written.
                if (j, i) in locked_pos:
                    locked_value = locked_pos[(j, i)]
                    grid[i][j] = locked_value
        print(grid)
        return grid

    def _draw_grid(self):

        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                # In order this line, sets the X co-ordinate, sets the Y co-ordinate
                # sets the rectangle width, sets the rectangle height, sets the
                # fill to full.
                pygame.draw.rect(self.display, self.grid[i][j], ((0 + j * BLOCK_SIZE), (PLAY_AREA_START + i * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE), 0)
        # Draws the playable area Border
        pygame.draw.rect(self.display, (211,211,211), (0, PLAY_AREA_START, 300, 600), 4)
        self._draw_gridLines()
        pygame.display.update()

    def _draw_window(self):

        self.display.fill((0, 0, 0))
        # Creates a label to display the title of 'Tetris'
        pygame.font.init()
        font = pygame.font.SysFont('fixedsys', 30)
        label = font.render('tetris', 1, (255, 255, 255))

        self._draw_grid()

        # Places the label at the correct position.
        self.display.blit(label, ((WIDTH / 2) -  (label.get_width() / 2), (PLAY_AREA_START / 4) - (label.get_height() / 2)))
        
        # Updates the pygame window with the newly drawn frame.
        pygame.display.update()

    def _draw_gridLines(self):
        x = 0
        y = PLAY_AREA_START

        for i in range(len(self.grid)):
            # Draws the Horizontal grid lines.
            pygame.draw.line(self.display, (128, 128, 128), (x, y + i * BLOCK_SIZE), (x + WIDTH, y + i * BLOCK_SIZE))
            for j in range(len(self.grid[i])):
                #Draws the Vertical grid lines.
                pygame.draw.line(self.display, (128, 128, 128), (x + j * BLOCK_SIZE, y), (x + j * BLOCK_SIZE, y + 600))


    def _move(self):
        direction = self.direction
        # Ensures the movement is valid, if so the piece will move into its
        # new position.
        if direction == Direction.RIGHT:
            self.current_piece.x += 1
            if not(self._valid_space()):
                self.current_piece.x -= 1
        elif direction == Direction.LEFT:
            self.current_piece.x -= 1
            if not(self._valid_space()):
                self.current_piece.x += 1
        elif direction == Direction.DOWN:
            self.current_piece.y += 1
            if not(self._valid_space()):
                self.current_piece.y -= 1
        elif direction == Direction.UP:
            self.current_piece.rotate()
            if not(self._valid_space()):
                for i in range(0, 3):
                    self.current_piece.rotate()

    def _shape_reformat(self):
        positions = []
        shape = self.current_piece.piece

        #Creates a list containing the co-ordinates for which the shape exists.
        for i, line in enumerate(shape):
            row = list(line)
            for j, column in enumerate(row):
                if column != 0:
                    positions.append((self.current_piece.x + j, self.current_piece.y + i))

        # As it currently exists, the array contains co-ordinates relative to their
        # own data structure, not the grid. The loop below fixes this.
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    def _valid_space(self):
        shape = self.current_shape.piece
        grid = self.grid

        # Creates a 2-Dimensional list representing the grid's accepted (empty) positions.
        valid_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
        # Converts the 2-Dimensional array into a 1D array for easy reading.
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = self._shape_reformat()

        # Checks to ensure the piece is within bounds of the grid
        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    def _is_gameOver(self, positions):

        for pos in positions:
            x, y = pos
            if y < 1:
                return True

        return False

    def _is_pieceDrop(self):
        # Checks each tick to see if enough time has elapsed for the current piece to drop
        if self.fall_time / 1000 > self.fall_speed:
            # Resets fall_time so that the next drop  can be calculated
            fall_time = 0
            self.current_piece.y += 1
            # Prevents downward movement from occuring if it causes the piece to
            # move into an invalid space.
            if not(self._valid_space()) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                # Will indicate on the next step() iteration that the piece needs to be
                # locked in place and the next one needs to be spawned.
                self.change_piece = True
        
    def _is_gameOver(self):
        pass

    def _clear_rows(self):
        pass

    def _draw_shape(self):
        pass
        
        
    
        
                
if __name__ == '__main__':
    game = Tetris()
    while True:
        game.step()
        

    #game loop
    
