import pygame
from image import Images

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))
    gray = pygame.Color('gray15')
    
    dial_background = Images("Dial Background.png", 320, 240, 1)
    compass_dial = Images("Compass Dial.png", 320, 240, 1)
    plane = Images("Compass Plane.png", 320, 240, 1)

    angle = 0

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        angle += 2
        compass_dial.rotate(angle)
        
        screen.fill(gray)
        dial_background.display(screen)
        compass_dial.display(screen)
        plane.display(screen)

        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
