import pygame
from image_new2 import Images

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((640, 480))
    gray = pygame.Color('gray15')
    
    dial_background = Images("Artificial Horizon Background.png", 320, 240, 1)
    outer_ring = Images("Artificial Horizon OR.png", 320, 240, 1)
    inner_ring = Images("Artificial Horizon IR.png", 320, 240, 1)
    dial_border = Images("Dial Border.png", 320, 240, 1)

    angle = 0
    x = 0
    y = 0
    inner_ring.display(screen)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        angle = 45

        x = 0 #always set to zero for this dial
        y = 20 #climb, descent 
        inner_ring.rotate(angle)
        outer_ring.rotate(angle)
        
        screen.fill(gray)
        inner_ring.move(screen, x, y)
        dial_border.display(screen)
        outer_ring.display(screen)
        dial_background.display(screen)
        


        pygame.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()