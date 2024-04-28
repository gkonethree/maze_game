import pygame

class Button():
    # initializing button class with x,y coordinates and image
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.action = False

    # drawing the button and checking for clicks
    def draw(self, win):
        pos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()[0]  # Check if left mouse button is clicked

        # Check if left mouse button is clicked and the button is not already clicked
        if clicked and not self.action:
            if self.rect.collidepoint(pos):
                self.action = True
        # If left mouse button is released, reset action to False
        elif not clicked:
            self.action = False

        win.blit(self.image, (self.rect.x, self.rect.y))


