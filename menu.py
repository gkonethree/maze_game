import pygame
from button import Button
from settings import Settings

set=Settings()

class Menu():
    def __init__(self) -> None:
        pass

    #making the menu screen 
    def open_menu(self,win):
        
        bg_img=pygame.transform.scale(pygame.image.load('images/entry.jpg'),(set.win_width,set.win_height))
        win.blit(bg_img,(0,0))
        #adding the play button
        play_but_img=pygame.transform.scale(pygame.image.load('images/start.png'),(200,90))
        play_but=Button(500,200,play_but_img)
        play_but.draw(win)

        #adding the high score button
        hs_but_img=pygame.transform.scale(pygame.image.load('images/hs.png'),(300,200))
        hs_but=Button(440,520,hs_but_img)
        hs_but.draw(win)

        #adding the quit button
        quit_but_img=pygame.transform.scale(pygame.image.load('images/quit.png'),(200,90))
        quit_but=Button(500,400,quit_but_img)
        quit_but.draw(win)
        self.playing=play_but.action
        self.q=quit_but.action
        self.hs=hs_but.action

        