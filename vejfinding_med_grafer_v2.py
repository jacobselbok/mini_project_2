import pygame
from copy import deepcopy
import random

def make_empty_grid(grid_size):
    grid = []
    for y in range(grid_size[1]):
        grid.append([])
        for x in range(grid_size[0]):
            if y == 0 or y == grid_size[1] - 1:
                grid[-1].append(1)
            else:
                if x == 0 or x == grid_size[0] - 1:
                    grid[-1].append(1)
                else:
                    grid[-1].append(0)
    return grid      

def create_block_cluster(grid_size, cluster_size):
    grid = make_empty_grid(grid_size)

    # Make a random amount (between 4 and 6 since 7 isn't included) of cluster centers
    for _ in range(random.randrange(4, 7)):
        center_x = random.randrange(cluster_size + 3, grid_size[0] - cluster_size - 2) 
        center_y = random.randrange(cluster_size + 3, grid_size[1] - cluster_size - 2)

        for y in range(center_y - cluster_size, center_y + cluster_size):
            for x in range(center_x - cluster_size, center_x + cluster_size):
                distance_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                probability = random.gauss(0, distance_to_center)  

                if distance_to_center <= cluster_size and -2.5 < distance_to_center < 2.5:
                    grid[y][x] = 1
                elif distance_to_center <= cluster_size and -2 < probability < 2:
                    grid[y][x] = 1

    return grid

def draw_grid(screen, grid):
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

def main():
    pygame.init() 
    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("A* map")
    grid_size = [screen_size[0] // 10, screen_size[1] // 10]
    cluster_size = 20

    grid = create_block_cluster(grid_size, cluster_size)

    running = True
    while running:
        running = open_close(running)
        screen.fill((255, 255, 255))

        draw_grid(screen, grid)

        pygame.display.flip()

if __name__ == "__main__":
    main()