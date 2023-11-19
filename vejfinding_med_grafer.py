import pygame


def main():
    pygame.init() 
    screen_size = (800,800)
    screen = pygame.display.set_mode(screen_size)
    


    
    running = True
    while running:
        running = open_close(running)
        screen.fill((255, 255, 255))
        



def open_close(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running


if __name__ == "__main__":
    main()