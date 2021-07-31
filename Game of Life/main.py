import numpy as np
import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
WIDTH = 10
HEIGHT = 10
MARGIN = 1
background = (212, 10, 100)

ROWS = 0
while (ROWS < 15) or (ROWS > 70):
    ROWS = int(input("Podaj rozmiar okna (15-70): "))
else:
    pass

COLS = ROWS
speed = 0
while (speed < 1) or (speed > 30):
    speed = int(input("Podaj predkosc gry (1-30): "))
else:
    pass


def grid_init():  # losowe generowanie planszy
    grid = np.zeros((ROWS, COLS))
    for x in range(ROWS):
        for y in range(COLS):
            if random.randint(0, 8) == 1:  # szansa na wylosowanie zywej komorki jest duzo mniejsza (1:8)
                grid[x][y] = 1
    return grid


def neighbours(current_row, current_col, grid):  # zliczanie ilosci zywych komorek w poblizu
    neighbours_alive = 0
    for z in range(-1, 2):
        for c in range(-1, 2):
            if not (z == 0 and c == 0):
                index_row = (current_row + z)
                index_col = (current_col + c)
                if (index_row or index_col) > (ROWS - 1) or (index_row or index_col) < 0:
                    neighbours_alive += 0
                else:
                    neighbours_alive += grid[(index_row % ROWS)][(index_col % ROWS)]
    return neighbours_alive


def update(rows, cols, old, new):  # aktualizacja stanu planszy na podstawie ilosci zywych komorek w poblizu
    for row in range(rows):
        for col in range(cols):
            life = neighbours(row, col, old)
            if old[row][col] == 0 and life == 3:  # reproduction
                new[row][col] = 1
            elif old[row][col] == 1 and (life < 2):  # underpopulation
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


window = pygame.display.set_mode(
    (WIDTH * ROWS + (ROWS + 1) * MARGIN, HEIGHT * COLS + (COLS + 1) * MARGIN))  # rozdzielczosc
pygame.display.set_caption('Game of Life')  # tytul
window.fill(background)  # tlo
timer = pygame.time.Clock()  # predkosc gry
pygame.display.flip()  # start

current_grid = grid_init()
next_grid = current_grid.copy()
running = True
while running:
    draw_board(current_grid)
    update(ROWS, COLS, current_grid, next_grid)
    current_grid = next_grid
    next_grid = current_grid
    pygame.display.update()
    timer.tick(speed)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
