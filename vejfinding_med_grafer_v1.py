import pygame
from copy import deepcopy
import random


def main():
    pygame.init() 
    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("A* map")
    size = [screen_size[0] // 10, screen_size[1] // 10]

    grid = make_grid(size)
    for x in range(0, size[0], 2):
        split_pos = random.randrange(1, size[1]-1)
        grid = grid_line(grid, (x, 0), (x, split_pos-2))
        grid = grid_line(grid, (x, split_pos+2), (x, size[1]-1))




    running = True
    while running:
        running = open_close(running)
        screen.fill((255, 255, 255))

        draw_grid(grid, screen)

        pygame.display.flip()

def make_grid(size):
    grid = []
    for y in range(size[1]):
        grid.append([])
        for x in range(size[0]):
            if y == 0 or y == size[1] - 1:
                grid[-1].append(1)
            else:
                if x == 0 or x == size[0] - 1:
                    grid[-1].append(1)
                else:
                    grid[-1].append(0)
    return grid      

def grid_line(grid, start_coord, end_coord):
    assert(start_coord[0] == end_coord[0] or start_coord[1] == end_coord[1])
    grid = deepcopy(grid)
    if start_coord[1] == end_coord[1]:
        for x in range(start_coord[0], end_coord[0]+1):
            grid[start_coord[1]][x] = 1
    else:
        for y in range(start_coord[1], end_coord[1]+1):
            grid[y][start_coord[0]] = 1
    return grid

def draw_grid(grid, screen):
    block_size = 10
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == 1:
                pygame.draw.rect(screen, (0, 0, 0), (x*block_size, y * block_size, block_size, block_size))



def open_close(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
    return running


if __name__ == "__main__":
    main()