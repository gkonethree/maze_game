import pygame
from button import Button
from settings import Settings

set=Settings()
class Levels():
    def __init__(self):
        self.act=False
        self.back=False
        self.level=0 #stores the level which has been clicked
        pass

    #drawing the level screen with buttons to select the level
    def lvl_screen(self,win):

        bg_img=pygame.transform.scale(pygame.image.load('images/entry.jpg'),(set.win_width,set.win_height))
        win.blit(bg_img,(0,0))
        #making level 1,2,3 buttons

        lv1_img=pygame.transform.scale(pygame.image.load('images/1.png'),(150,150))
        lv1_but=Button(300,350,lv1_img)
        lv1_but.draw(win)
        if lv1_but.action:
            self.act=True
            self.level=1
        
        lv2_img=pygame.transform.scale(pygame.image.load('images/2.png'),(150,150))
        lv2_but=Button(510,350,lv2_img)
        lv2_but.draw(win)
        if lv2_but.action:
            self.act=True
            self.level=2

        lv3_img=pygame.transform.scale(pygame.image.load('images/3.png'),(150,150))
        lv3_but=Button(720,350,lv3_img)
        lv3_but.draw(win)
        if lv3_but.action:
            self.act=True
            self.level=3

        back_img=pygame.transform.scale(pygame.image.load('images/back.png'),(100,100))
        back_but=Button(20,20,back_img)
        back_but.draw(win)
        if back_but.action:
            self.back=True
            


        