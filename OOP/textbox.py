import pygame

class TextBoxes():
    def __init__(self, contents, allowedcharacters, maxinputlen, active, x, y, w, h):
        #creating a rectangle for pygame
        self.rectangle = pygame.Rect(x,y,w,h)
        #setting contents to variables
        self.active = active
        self.contents = contents
        self.allowedcharacters = allowedcharacters
        self.maxinputlen = maxinputlen

    def checkactive(self, event):
        #checking to see if the textbox is selected by checking the collide point
        if self.rectangle.collidepoint(event.pos):
            self.active = True
        else:
            self.active = False

    def updatecontents(self, event):
        #updating the contents of the textbox
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.contents = self.contents[0:-1]
            elif len(self.contents) >= self.maxinputlen:
                self.contents = self.contents
            elif event.unicode in self.allowedcharacters:
                self.contents += event.unicode

    def display(self, screen, font):
        #changing the outline colour based on if the textbox is active or not
        if self.active:
            textbox_colour = (0,0,0)
        else:
            textbox_colour = (255,255,255)
        pygame.draw.rect(screen, textbox_colour, self.rectangle, 2)

        #displaying the textbox
        textbox_surface = font.render(self.contents, True, (255,255,255))
        screen.blit(textbox_surface, (self.rectangle.x + 5, self.rectangle.y))
