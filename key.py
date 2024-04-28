import pygame 
from settings import Settings
set=Settings()

class Key():
    #initializing key class with x,y coordinates
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.taken=False
    def draw(self,win):
        coin_img=pygame.transform.scale(pygame.image.load('images/key.png'),(set.TILE_SIZE,set.TILE_SIZE))
        if (not self.taken):
            win.blit(coin_img,(self.x,self.y))