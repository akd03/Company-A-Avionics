import pygame

class Images():
    def __init__(self, filename, x, y, scale):
        #loading the image
        self.image = pygame.image.load(filename).convert_alpha()
        #getting the width and height to scale the image
        width = self.image.get_width()
        height = self.image.get_height()
        #snapshotting the original image for rotation        
        self.original_image = self.image
        #creating a rectangle for pygame
        self.rectangle = self.image.get_rect(center=(x, y))
        #scaling the image to a custom amount specified in the object
        self.image = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))

    def rotate(self, angle):
        #rotating the image while keeping its centre
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rectangle = self.image.get_rect(center=self.rectangle.center)

    def move(self, screen, x, y):
        #getting the position of the image
        self.position = self.rectangle
        #erasing the old image
        #screen.blit(screen, self.position, self.position)
        #updating and drawing the new image
        self.position = self.position.move(x, y)
        screen.blit(self.image, self.position)

    def display(self, screen):
        #displaying the image
        screen.blit(self.image, self.rectangle)