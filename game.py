import pygame, sys
import numpy as np

pygame.init()

# window settings
width = 600
height = width
title = 'Tic Tac Toe'

# background settings
bg_color = (28, 170, 156)

# line settings
line_color = (23, 145, 135)
line_width = 15

# board settings
board_row = board_col = 3
square_size = width // board_row

# circle settings
circle_color = (239, 231, 200)
circle_radius = square_size // 3
circle_width = 15

# cross settings
cross_color = (66, 66, 66)
cross_width = 25
space = square_size // 4

# starting player -> 1 = O, 2 = X
player = 2

# is the game over?
is_game_over = False

# create window
screen = pygame.display.set_mode((width, height))

# set the title of the window
pygame.display.set_caption(title)

# set the background color
screen.fill(bg_color)

# create the console board to make manipulating the actual game board easier
board = np.zeros((board_row, board_col))

# drawing the separators
def draw_separators():
    # horizontal lines
    pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
    pygame.draw.line(screen, line_color, (0, 2 * square_size), (width, 2 * square_size), line_width)

    # vertical lines
    pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
    pygame.draw.line(screen, line_color, (2 * square_size, 0), (2 * square_size, height), line_width)

# draw shapes
def draw_shapes():
    for row in range(board_row):
        for col in range(board_col):
            if board[row][col] == 1:
                pygame.draw.circle(screen, circle_color, (int(col * square_size + square_size / 2), int(row * square_size + square_size / 2)), circle_radius, circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, cross_color, (col * square_size + space, row * square_size + square_size - space), (col * square_size + square_size - space, row * square_size + space), cross_width)
                pygame.draw.line(screen, cross_color, (col * square_size + space, row * square_size + space), (col * square_size + square_size - space, row * square_size + square_size - space), cross_width)

# place the shape down in a specific tile
def place_shape(row, col, player):
    board[row][col] = player

# check if the tile is empty
def is_tile_empty(row, col):
    return board[row][col] == 0

# check if the board is full
def is_board_full():
    for row in range(board_row):
        for col in range(board_col):
            if board[row][col] == 0:
                return False
    return True

# check for win for a specific player
def check_win(player):
    # check for vertical match
    for col in range(board_col):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            draw_vertical_line(col, player)
            return True

    # check for horizontal match
    for row in range(board_row):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            draw_horizontal_line(row, player)
            return True

    # check for ascending diagonal match
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        draw_ascending_line(player)
        return True

    # check for descending diagonal match
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        draw_descending_line(player)
        return True

    # no match
    return False

# draw vertical line
def draw_vertical_line(col, player):
    xPos = col * square_size + square_size / 2
    color = circle_color if player == 1 else cross_color

    # draw the line
    pygame.draw.line(screen, color, (xPos, 15), (xPos, height - 15), 15)

# draw horizontal line
def draw_horizontal_line(row, player):
    yPos = row * square_size + square_size / 2
    color = circle_color if player == 1 else cross_color

    # draw the line 
    pygame.draw.line(screen, color, (15, yPos), (width - 15, yPos), 15)

# draw diagonal lines
def draw_ascending_line(player):
    color = circle_color if player == 1 else cross_color

    # draw the line 
    pygame.draw.line(screen, color, (15, height - 15), (width - 15, 15), 15)

def draw_descending_line(player):
    color = circle_color if player == 1 else cross_color

    # draw the line 
    pygame.draw.line(screen, color, (15, 15), (width - 15, height - 15), 15)

# restart the game
def restart():
    screen.fill(bg_color)
    draw_separators()
    for row in range(board_row):
        for col in range(board_col):
            board[row][col] = 0

draw_separators()

while True:
    for event in pygame.event.get():
        # if player exited the game
        if event.type == pygame.QUIT:
            sys.exit()

        # if player clicked the mouse
        if event.type == pygame.MOUSEBUTTONDOWN and not is_game_over:
            # get mouse position
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            # parse mouse position to check which tile is clicked
            row_tile = mouseY // square_size 
            col_tile = mouseX // square_size

            # check if the tile is empty and place the shape of the player
            if is_tile_empty(row_tile, col_tile):
                place_shape(row_tile, col_tile, player)
                is_game_over = check_win(player) or is_board_full()
                player = player % 2 + 1

                # draw the shapes onto the screen
                draw_shapes()

        # check for restart and only do so when game is over
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and is_game_over:
                restart()
                is_game_over = False
                player = 2

    # update the screen
    pygame.display.update()
