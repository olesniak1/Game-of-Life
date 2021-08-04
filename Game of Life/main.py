import numpy as np
import pygame
import random

RED = (138, 27, 59)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 10
HEIGHT = 10
MARGIN = 1
background = (212, 10, 100)
ROWS = 0
speed = 0

pygame.display.set_caption('Game of Life')
timer = pygame.time.Clock()


def grid_init():
    grid = np.zeros((ROWS, COLS))
    for x in range(ROWS):
        for y in range(COLS):
            if random.randint(0, 6) == 1:
                grid[x][y] = 1
    return grid


def neighbours(current_row, current_col, grid):
    neighbours_alive = 0
    for z in range(-1, 2):
        for c in range(-1, 2):
            if not (z == 0 and c == 0):
                index_row = (current_row + z)
                index_col = (current_col + c)
                if index_row > ROWS - 1:
                    pass
                elif index_col > ROWS - 1:
                    pass
                elif index_row < 0:
                    pass
                elif index_col < 0:
                    pass
                else:
                    neighbours_alive += grid[index_row][index_col]
    return neighbours_alive


def update(rows, cols, old, new):
    for row in range(rows):
        for col in range(cols):
            life = neighbours(row, col, old)
            if old[row][col] == 0 and life == 3:
                new[row][col] = 1
            elif old[row][col] == 1 and (life < 2):
                new[row][col] = 0
            elif old[row][col] == 1 and (life > 3):
                new[row][col] = 0
            else:
                new[row][col] = old[row][col]


def draw_board(grid):
    for ROW in range(ROWS):
        for COL in range(COLS):
            if grid[ROW][COL] == 1:
                color = BLACK
            else:
                color = WHITE
            pygame.draw.rect(window, color, [(MARGIN + WIDTH) * COL + MARGIN,
                                             (MARGIN + HEIGHT) * ROW + MARGIN, WIDTH, HEIGHT])


while (ROWS < 15) or (ROWS > 70):
    ROWS = int(input("Podaj rozmiar okna (15-70): "))

COLS = ROWS
while (speed < 1) or (speed > 30):
    speed = int(input("Podaj predkosc gry (1-30): "))

running = False
running_click = False

game_mode = 0
while game_mode not in [1, 2]:
    game_mode = int(input("Podaj tryb gry \n 1 - losowo wygenerowana plansza \n 2 - wlasny wybor komorek: "))

if game_mode == 1:
    window = pygame.display.set_mode(
        (WIDTH * ROWS + (ROWS + 1) * MARGIN, HEIGHT * COLS + (COLS + 1) * MARGIN))
    current_grid = grid_init()
    next_grid = current_grid.copy()
    window.fill(background)
    pygame.display.flip()
    running = True

elif game_mode == 2:
    window = pygame.display.set_mode(
        (WIDTH * ROWS + (ROWS + 1) * MARGIN + 60 + ROWS, HEIGHT * COLS + (COLS + 1) * MARGIN))
    window.fill(background)
    pygame.display.flip()
    pygame.draw.rect(window, RED, [WIDTH * ROWS + (ROWS + 1) * MARGIN + 5,
                                   (HEIGHT * COLS + (COLS + 1) * MARGIN) // 6, 50 + ROWS, 25 + ROWS])
    pygame.font.init()
    myfont = pygame.font.SysFont('Arial', 29)
    txt = myfont.render("start", False, (0, 0, 0))
    window.blit(txt, [WIDTH * ROWS + (ROWS + 1) * MARGIN + 40, (HEIGHT * COLS + (COLS + 1) * MARGIN) // 5])
    grid = np.zeros((ROWS, COLS))
    running_click = True

while running_click:
    position = pygame.mouse.get_pos()
    draw_board(grid)
    pygame.display.update()
    timer.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_click = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if position[0] <= WIDTH * ROWS + (ROWS + 1) * MARGIN:
                column = position[0] // (WIDTH + MARGIN)
                row = position[1] // (HEIGHT + MARGIN)
                grid[row][column] = 1
            elif (WIDTH * ROWS + (ROWS + 1) * MARGIN + 5 <= position[0] <= WIDTH * ROWS + (
                    ROWS + 1) * MARGIN + 55 + ROWS):
                current_grid = grid
                next_grid = current_grid.copy()
                running_click = False
                running = True

while running:
    draw_board(current_grid)
    update(ROWS, COLS, current_grid, next_grid)
    current_grid = next_grid.copy()
    next_grid = current_grid.copy()
    pygame.display.update()
    timer.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
