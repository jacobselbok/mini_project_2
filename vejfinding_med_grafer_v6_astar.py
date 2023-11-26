import pygame
import random
from collections import deque
from heapq import heappush, heappop

class Grid:
    def __init__(self, size, cluster_size):
        self.size = size
        self.cluster_size = cluster_size
        self.grid = self.create_block_cluster()

    def make_empty_grid(self):
        grid = []
        for y in range(self.size[1]):
            grid.append([])
            for x in range(self.size[0]):
                if y == 0 or y == self.size[1] - 1:
                    grid[-1].append(1)
                else:
                    if x == 0 or x == self.size[0] - 1:
                        grid[-1].append(1)
                    else:
                        grid[-1].append(0)
        return grid   
    
    def start_stop_point(self):
        grid = self.make_empty_grid()
        grid[2][2] = 2
        grid[self.size[0] - 3][self.size[1] - 3] = 3
        return grid

    def create_block_cluster(self):
        grid = self.start_stop_point()

        # Make a random amount (between 4 and 6) of cluster centers
        for _ in range(random.randrange(4, 7)):
            center_x = random.randrange(self.cluster_size + 3, self.size[0] - self.cluster_size - 2) 
            center_y = random.randrange(self.cluster_size + 3, self.size[1] - self.cluster_size - 2)

            for y in range(center_y - self.cluster_size, center_y + self.cluster_size):
                for x in range(center_x - self.cluster_size, center_x + self.cluster_size):
                    distance_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                    probability = random.gauss(0, distance_to_center)  

                    if distance_to_center <= self.cluster_size and -2.5 < distance_to_center < 2.5:
                        grid[y][x] = 1
                    elif distance_to_center <= self.cluster_size and -2 < probability < 2:
                        grid[y][x] = 1
        return grid

    def draw_map(self, screen):
        block_size = 10
        for y, row in enumerate(self.grid):
            for x, value in enumerate(row):
                if value == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (x*block_size, y * block_size, block_size, block_size))
                elif value == 2:
                    pygame.draw.rect(screen, (255, 0, 0), (x*block_size, y * block_size, block_size, block_size))
                elif value == 3:
                    pygame.draw.rect(screen, (0, 255, 0), (x*block_size, y * block_size, block_size, block_size))

    def astar_search(self, start, goal):
        open_set = [(0, start)]  # Priority queue, each element is a tuple (f_score, position)
        came_from = {}  # Dictionary to store the parent of each position
        g_score = {start: 0}  # Dictionary to store the cost from start to each position

        while open_set:
            _, current = heappop(open_set)

            if current == goal:
                return self.construct_path(start, goal, came_from)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1  # Assuming uniform cost for simplicity

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

        return None  # No path found

    def heuristic(self, a, b):
        # Simple Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


    def get_neighbors(self, pos):
        x, y = pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(x, y) for x, y in neighbors if 0 <= x < self.size[0] and 0 <= y < self.size[1] and self.grid[y][x] != 1]

    def construct_path(self, start, goal, parent_dict):
        path = [goal]
        current = goal

        while current != start:
            current = parent_dict.get(current)
            if current is None:
                return None  # No valid path
            path.append(current)

        return path[::-1]



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
    pygame.display.set_caption("Breadth-First Search on Grid")
    grid_size = [screen_size[0] // 10, screen_size[1] // 10]
    cluster_size = 20

    grid = Grid(grid_size, cluster_size)
    start = (2, 2)  # Example start position
    goal = (grid_size[0] - 3, grid_size[1] - 3)  # Example goal position
        
    running = True
    while running:
        running = open_close(running)
        screen.fill((255, 255, 255))

        # Draw the grid and path
        grid.draw_map(screen)
        path = grid.astar_search(start, goal)
        if path:
            for pos in path:
                pygame.draw.rect(screen, (255, 0, 0), (pos[0] * 10, pos[1] * 10, 10, 10))

        pygame.display.flip()

if __name__ == "__main__":
    main()