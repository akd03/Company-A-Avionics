import pygame

from button import Buttons
from image import Images
from text import Texts
from textbox import TextBoxes

def main():

    clock = pygame.time.Clock()
    monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
    screen = pygame.display.set_mode((1900, 600), pygame.RESIZABLE)
    
    gray = pygame.Color("gray15")
    font = pygame.font.Font(None, 10)

    ####

    textbox = TextBoxes("", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], 12, False, 155, 100, 100, 8)
    text = Texts("Hello world", font, (255, 255, 255), 500, 100)
    image = Images("Compass Dial.png", 300, 300, 0.5)
    button = Buttons("Artificial Horizon IR.png", 700, 100, 0.5)

    ####

    fullscreen = False
    done = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.VIDEORESIZE:
                if not fullscreen:
                    screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen.get_width(), screen.get_height()), pygame.RESIZABLE)

            ####

            if event.type == pygame.MOUSEBUTTONDOWN:
                textbox.checkactive(event)
            if event.type == pygame.KEYDOWN:
                textbox.updatecontents(event)

            ####

        screen.fill(gray)
        
        ####

        image.display(screen)
        button.display(screen)
        text.display(screen)
        textbox.display(screen, font)

        if button.display(screen) == True:
            print("Goodbye world")

        ####

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()   

    