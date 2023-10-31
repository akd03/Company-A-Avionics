import pygame
import time

class Texts():
    def __init__(self, contents, font, colour, x, y):
        #creating the text object
        self.text_object = font.render(contents, 1, colour)
        #creating a rectangle from the object for pygame to place
        self.rectangle = self.text_object.get_rect(center=(x,y))

    def display(self, surface):
        surface.blit(self.text_object, (self.rectangle.x, self.rectangle.y))

# Example font
#fontname = pygame.font.Font(None, fontsize) gives default font
#fontname = pygame.font.Font(filename, fontsize)

# Example object
#text = Texts("Contents", font, (255, 255, 255), screen, x, y)
