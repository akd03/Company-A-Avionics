import pygame
import time

class Buttons():
    def __init__(self, filename, x, y, scale):
        #loading the image
        self.image = pygame.image.load(filename).convert_alpha()
        #getting the width and height of each image to scale it
        width = self.image.get_width()
        height = self.image.get_height()
        #scaling the image to a custom amount specified in the object
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        #creating a rectangle from the image for pygame to place
        self.rectangle = self.image.get_rect()
        self.rectangle.topleft = (x, y)
        self.clicked = False

    def display(self, surface):
        action = False
        
        #finding the position of the mouse
        mouse_position = pygame.mouse.get_pos()
        #checking if the button is moused over 
        if self.rectangle.collidepoint(mouse_position):
            #and if it is left [0] clicked
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                #preventing multiple responses from a singular click by temporarily disabling the input
                self.clicked = True
                action = True
                time.sleep(0.1)
                self.clicked = False
                
        surface.blit(self.image, (self.rectangle.x, self.rectangle.y))

        #returning the button action outside of the class 
        return action
