import numpy as np
import pygame
import math
import sys

ROWS = 6
COLUMNS = 7

# Load celebratory image
image = pygame.image.load("win.png")

board = np.zeros((ROWS, COLUMNS))

game_over = False
turn = 0

SLOT = 100
width = COLUMNS * SLOT
height = (ROWS + 1) * SLOT + 50  # Added extra space for the text
size = (width, height)

# Setting up colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

OFFSET = 100
RADIUS = int(SLOT / 2 - 5)

# Initialize Pygame
pygame.init()
window = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 Game")
font = pygame.font.SysFont("Comic Sans MS", 33, True)

# Function to get player names
def get_input_text(prompt):
    input_box = pygame.Rect(50, height // 2, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        window.fill((30, 30, 30))
        txt_surface = font.render(prompt + text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        window.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(window, color, input_box, 2)
        pygame.display.flip()
    
    return text

# Get player names from the game window
player1_name = get_input_text("Enter Player 1 name: ")
player2_name = get_input_text("Enter Player 2 name: ")

# Function to draw the game board
def draw_board(board):
    pygame.draw.rect(window, GRAY, (0, 0, width, SLOT))
    for c in range(COLUMNS):
        for r in range(ROWS):
            rect = (c * SLOT, r * SLOT + OFFSET, SLOT, SLOT)
            c1 = (int(c * SLOT + SLOT / 2), int(r * SLOT + OFFSET + SLOT / 2))
            pygame.draw.rect(window, BLUE, rect)
            pygame.draw.circle(window, GRAY, c1, RADIUS)
    for c in range(COLUMNS):
        for r in range(ROWS):
            c2 = (int(c * SLOT + SLOT / 2), height - int(r * SLOT + SLOT / 2) - 50)
            if board[r][c] == 1:
                pygame.draw.circle(window, RED, c2, RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(window, GREEN, c2, RADIUS)

    # Draw player info text
    text = font.render(f"{player1_name}: Red   {player2_name}: Green", True, (255, 255, 255))
    window.blit(text, (10, height - 45))
    
    pygame.display.update()

# Function to check if a move is valid
def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

# Function to drop a piece in the board
def drop_piece(board, col, piece):
    for r in range(ROWS):
        if board[r][col] == 0:
            board[r][col] = piece
            break

# Function to check for a winning move
def is_winning_move(board, piece):
    # Check Horizontal locations for win
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
    # Check vertical locations for win
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
    # Check positively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    # Check negatively sloped diagonals
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False

print(board)
draw_board(board)

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            col = math.floor(posx / SLOT)

            if turn % 2 == 0:
                if col < 0 or col >= COLUMNS:
                    print("Invalid column. Try again.")
                    continue
                if is_valid_location(board, col):
                    drop_piece(board, col, 1)
                    if is_winning_move(board, 1):
                        print(f"Congrats {player1_name}")
                        label = font.render(f"{player1_name} WON!", True, RED)
                        img = pygame.image.load("redfig.png")
                        game_over = True
                else:
                    print("Column is full. Try again.")
                    continue
            else:
                if col < 0 or col >= COLUMNS:
                    print("Invalid column. Try again.")
                    continue
                if is_valid_location(board, col):
                    drop_piece(board, col, 2)
                    if is_winning_move(board, 2):
                        print(f"Congrats {player2_name}")
                        label = font.render(f"{player2_name} WON!", True, (1,50,32))
                        img = pygame.image.load("greenfig.png")
                        game_over = True
                else:
                    print("Column is full. Try again.")
                    continue

            turn += 1
            print(np.flip(board, 0))
            draw_board(board)
    if game_over:
        window.blit(image, (100, 220))
        window.blit(label, (270, 300))
        window.blit(img, (265, 370))
        pygame.display.update()
        pygame.time.wait(5000)
