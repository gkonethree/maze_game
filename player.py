import pygame
from settings import Settings
set=Settings()
class player():
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = set.TILE_SIZE
        self.left = False
        self.right = False
        self.walkCount = 0
        
        #player moving right images
        self.walkRight = [pygame.transform.scale(pygame.image.load('images/R1.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R2.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R3.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R4.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R5.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R6.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R7.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R8.png'), (self.height, self.width)),
                  pygame.transform.scale(pygame.image.load('images/R9.png'), (self.height, self.width))]

        #player moving left images
        self.walkLeft = [pygame.transform.scale(pygame.image.load('images/L1.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L2.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L3.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L4.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L5.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L6.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L7.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L8.png'), (self.height, self.width)),
                 pygame.transform.scale(pygame.image.load('images/L9.png'), (self.height, self.width))]

        self.char = pygame.transform.scale(pygame.image.load('images/standing.png'), (self.height, self.width))
    
    def draw(self, win):

        #moving the player 
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount +=1
        else:
            win.blit(self.char, (self.x,self.y))