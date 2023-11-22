class Texts():
    def __init__(self, contents, font, colour, x, y):
        #creating the text object
        self.text_object = font.render(contents, 1, colour)
        #creating a rectangle from the object for pygame to place
        self.rectangle = self.text_object.get_rect(center=(x,y))

    def display(self, surface):
        surface.blit(self.text_object, (self.rectangle.x, self.rectangle.y))

    def move(self, surface, x, y):
        #getting the position of the image
        self.position = self.rectangle
        #updating and drawing the new image
        self.position = self.position.move(x, y)
        surface.blit(self.text_object, self.position)