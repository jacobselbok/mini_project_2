import pygame
import random
from heapq import heappush, heappop

class Program: 
    def __init__(self, size, cluster_size, start, goal):
        self.size = size
        self.cluster_size = cluster_size
        self.start = start
        self.goal = goal
        self.grid = self.start_goal_point() # Runs the "start_goal_point" method if "self.grid" is called

    def make_grid(self): # Actually makes the initial grid
        grid = [] # Makes an empty list
        for y in range(self.size[1]): # Making the rows in the grid
            grid.append([]) # Adds a list in the empty list, making a list in a list
            for x in range(self.size[0]): # Making the colums in the grid
                if y == 0 or y == self.size[1] - 1: # Adds a boarder at the top and bottom
                    grid[-1].append(1) 
                elif x == 0 or x == self.size[0] - 1: # Adds a boarder at both sides
                    grid[-1].append(1)
                else:
                    grid[-1].append(0) # Fills out the rest of the grid
        return grid 

    def create_block_cluster(self): # Makes clusters and adds them to the grid
        grid = self.make_grid() # Makes a grid by running the "make_grid" method

        for _ in range(random.randrange(5, 8)): # Makes a random amount (between 5 and 7) of cluster centers
            center_x = random.randrange(self.cluster_size + 3, self.size[0] - self.cluster_size - 2) # Adds random starting point for the clusters
            center_y = random.randrange(self.cluster_size + 3, self.size[1] - self.cluster_size - 2)

            for y in range(center_y - self.cluster_size, center_y + self.cluster_size): # Makes sure the cluster is within the grid
                for x in range(center_x - self.cluster_size, center_x + self.cluster_size): 
                    distance_to_center = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5 # Uses the euclidean distance to find distance to the center of the cluster
                    probability = random.gauss(0, distance_to_center) # The further from the center, the higher the chance of a high "probability"

                    if distance_to_center <= self.cluster_size and -2.5 < distance_to_center < 2.5: # Adds a solid center
                        grid[y][x] = 1
                    elif distance_to_center <= self.cluster_size and -2 < probability < 2: # Adds tiles randomly in a circle around the center
                        grid[y][x] = 1
        return grid

    def start_goal_point(self): # Draws the "start" and "goal" at the end
        grid = self.create_block_cluster() # Makes a grid by running the "create_block_cluster" method

        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if x == self.start[0] and y == self.start[1]: # Adds the start point
                    grid[y][x] = 2
                elif x == self.goal[0] and y == self.goal[1]: # Adds the goal point
                    grid[y][x] = 3
        return grid

    def draw_map(self, screen): # Draws the final map
        tile = 10 # Size of each tile
        for y, row in enumerate(self.grid): # Makes a grid by running the "start_stop_point" method
            for x, value in enumerate(row):
                if value == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (x * tile, y * tile, tile, tile)) # Adds the blocking tiles
                elif value == 2:
                    pygame.draw.rect(screen, (0, 255, 255), (x * tile, y * tile, tile, tile)) # Adds the start tile
                elif value == 3:
                    pygame.draw.rect(screen, (0, 255, 0), (x * tile, y * tile, tile, tile)) # Adds the goal tile

    def astar_search(self, start, goal):
        open_set = [(0, start)] # Adds a priority queue, each element is a tuple (f_score, position)
        came_from = {} # Adds a dictionary to store the parent of each position
        g_score = {start: 0} # Adds a dictionary to store the cost from start to each position

        while open_set: # Loops continues until "open_set" is empty, so no more paths
            _, current = heappop(open_set) # Pops (removes) position with the lowest f_score

            if current == goal: # Returns path if the goal has been reached
                return self.construct_path(start, goal, came_from)

            for neighbor in self.get_neighbors(current): # Loops over the neightbors of current position
                tentative_g_score = g_score[current] + 1 # Setting a uniform cost for each position

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]: # Adds new neighbor and remove higher g_score
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal) # Calculates f_score with "Manhattan distance heuristic"
                    heappush(open_set, (f_score, neighbor)) # Adds position to the queue
                    came_from[neighbor] = current 
        return None # There wasn't a valid path

    def heuristic(self, a, b): # a = neighbor, b = goal
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) # Uses the "Manhattan distance heuristic"

    def get_neighbors(self, pos): # pos = current position
        x, y = pos
        neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)] # Finds pos in south, north, east and west for current position
        return [(x, y) for x, y in neighbors if 0 <= x < self.size[0] and 0 <= y < self.size[1] and self.grid[y][x] != 1] # Returns neightbors if they aren't a blocking tile

    def construct_path(self, start, goal, parent_dict):
        path = [goal] 
        current = goal # Starts from goal and goes backwards

        while current != start: # Continues until path is done
            current = parent_dict.get(current) # Retrieves parent position for the current position
            if current is None: # Returns "None" if there are no valid paths
                return None 
            path.append(current) # Appends backwards to form a path

        return path[::-1] # Reverses the list so it's from start to goal

def open_close(running):
    for event in pygame.event.get(): # Checks for event
        if event.type == pygame.QUIT: # Checks if event is the screen getting closed
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: # Checks if event is the ESC getting pushed
            running = False
    return running # Main loop continues if neither event happened

def main():
    pygame.init() 
    screen_size = (800, 800)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("A*")
    grid_size = [screen_size[0] // 10, screen_size[1] // 10] # Making a 80 X 80 grid
    cluster_size = 20

    new_map = True
    running = True
    while running:
        running = open_close(running) # Checks if the screen gets closed or if ESC has been pushed
        screen.fill((255, 255, 255)) # White background

        while new_map == True or path == None: # Makes the grid and path. It loops if path can't be found, until it finds a valid path
            start = (random.randrange(5, grid_size[0]//2), random.randrange(5, grid_size[1]//2))
            goal = (random.randrange(grid_size[0]//2 + 1, grid_size[0] - 6), random.randrange(grid_size[1]//2 + 1, grid_size[1] - 6))
            grid = Program(grid_size, cluster_size, start, goal)
            path = grid.astar_search(start, goal) # Returns a path or None
            new_map = False # If path is found, then loop ends

        grid.draw_map(screen) # Draws the grid and cluster

        for pos in path:
            pygame.draw.rect(screen, (255, 0, 0), (pos[0] * 10 + 2, pos[1] * 10 + 2, 6, 6)) # Draws the path

        pygame.display.flip() # Displays the screen

if __name__ == "__main__": # Checks if this program is the main program
    main()