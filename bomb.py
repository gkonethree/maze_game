import pygame 
from settings import Settings
set=Settings()

class Bomb():
    #initializing bomb with x,y coorinates
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.taken=False

    #drawing bomb on screen
    def draw(self,win):
        bomb_img=pygame.transform.scale(pygame.image.load('images/bomb.png'),(set.TILE_SIZE,set.TILE_SIZE))
        if (not self.taken):
            win.blit(bomb_img,(self.x,self.y))