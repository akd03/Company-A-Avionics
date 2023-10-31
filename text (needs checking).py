import pygame
import time

class Texts():
    def __init__(self, contents, x, y, font, colour):
        #creating the text object
        text_object = font.render(contents, 1, colour)
        #creating a rectangle from the object for pygame to place
        self.rectangle = text_object.get_rect()
        self.rectangle.topleft = (x, y)

    def display(self, surface):
        surface.blit(self.cbject, (self.rectangle.x, self.rectangle.y))